"""Validate portable records and preserve source-backed profile updates."""

from __future__ import annotations

import copy
import json
import re
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlsplit

from jsonschema import Draft202012Validator, FormatChecker

Json = dict[str, Any]
SCHEMAS = Path(__file__).resolve().parents[2] / "schemas"
KINDS = {"profile", "document", "company-brief", "manifest", "application"}


def read_json(path: Path) -> Json:
    """Read a UTF-8 JSON object, accepting a Windows UTF-8 BOM."""
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return data


def write_json(path: Path, data: Json, *, replace: bool = False) -> None:
    """Write atomically; reject accidental replacement unless explicitly enabled."""
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    if not replace:
        with path.open("x", encoding="utf-8") as stream:
            stream.write(text)
        return
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=path.parent, delete=False
        ) as out:
            temporary = Path(out.name)
            out.write(text)
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def now() -> str:
    """Return an explicit UTC timestamp for local state."""
    return datetime.now(UTC).isoformat()


def safe_id(value: str) -> str:
    """Reject document IDs that could become paths or ambiguous filenames."""
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
        raise ValueError("Use a lowercase hyphen-separated document ID")
    return value


def local_path(root: Path, relative: str) -> Path:
    """Resolve a manifest path inside its workspace, including symlink checks."""
    path = Path(relative)
    if path.is_absolute() or "\\" in relative or re.match(r"^[A-Za-z]:", relative):
        raise ValueError("Manifest paths must be relative POSIX paths")
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root.resolve()) or resolved == root.resolve():
        raise ValueError("Manifest path escapes its workspace")
    return resolved


def public_url(url: str) -> str:
    """Accept vacancy URLs, excluding credentials and obvious authentication state."""
    parts = urlsplit(url)
    local = parts.hostname in {"localhost", "127.0.0.1", "::1"}
    if not parts.hostname or (parts.scheme != "https" and not (parts.scheme == "http" and local)):
        raise ValueError("Use an HTTPS job URL (HTTP is allowed only for local fixtures)")
    forbidden = {"token", "access_token", "id_token", "password", "code", "samlresponse", "session"}
    if (
        parts.username
        or parts.password
        or any(key.lower() in forbidden for key, _ in parse_qsl(parts.query + "&" + parts.fragment))
    ):
        raise ValueError("Record the public vacancy URL, not authentication state")
    return url


def _unique(records: list[Json], label: str) -> set[str]:
    identifiers = [str(item["id"]) for item in records]
    if len(set(identifiers)) != len(identifiers):
        raise ValueError(f"Duplicate {label} IDs")
    return set(identifiers)


def validate(kind: str, data: Json) -> None:
    """Check JSON schema and cross-record evidence references."""
    if kind not in KINDS:
        raise ValueError(f"Unknown record kind: {kind}")
    schema = read_json(SCHEMAS / f"{kind}.schema.json")
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    error = next(validator.iter_errors(data), None)
    if error is not None:
        location = ".".join(map(str, error.absolute_path)) or "root"
        raise ValueError(f"Invalid {kind} at {location}: {error.message}")
    if kind in {"profile", "company-brief"}:
        source_ids = _unique(data["sources"], "source")
        records = data["facts"] if kind == "profile" else data["findings"]
        _unique(records, "fact/finding")
        for record in records:
            citations = set(record["source_ids"])
            for alternative in record.get("alternatives", []):
                citations.update(alternative["source_ids"])
            if not citations <= source_ids:
                raise ValueError(f"Unknown source ID in {record['id']}")
            if kind == "company-brief" and record["status"] != "unknown" and not citations:
                raise ValueError("Facts and inferences need a cited source")
        if kind == "profile":
            fields = [fact["field"] for fact in records]
            if len(fields) != len(set(fields)):
                raise ValueError("Record conflicting values as alternatives to one field")
        else:
            ats = data["ats"]
            if not set(ats["source_ids"]) <= source_ids:
                raise ValueError("Unknown ATS source ID")
            if ats["status"] == "unknown":
                if ats["vendor"] is not None:
                    raise ValueError("Unknown ATS must have vendor null")
            elif not ats["vendor"] or not ats["source_ids"]:
                raise ValueError("An identified ATS needs a vendor and cited evidence")
            for source in data["sources"]:
                public_url(source["url"])
    if kind == "application":
        public_url(data["job"]["url"])
        if data["observation"]:
            public_url(data["observation"]["url"])
            for key in ("company", "reference"):
                if data["observation"][key] != data["job"][key]:
                    raise ValueError("Observed page does not match the target company/job")
        _unique(data["upload_fields"], "upload field")


def merge_profiles(base: Json, incoming: Json) -> Json:
    """Merge facts conservatively, preserving conflicting values and their sources."""
    validate("profile", base)
    validate("profile", incoming)
    result = copy.deepcopy(base)
    sources = {source["id"]: source for source in result["sources"]}
    for source in incoming["sources"]:
        if source["id"] in sources and source != sources[source["id"]]:
            raise ValueError(f"Source ID reused with a different label: {source['id']}")
        sources[source["id"]] = copy.deepcopy(source)
    result["sources"] = list(sources.values())
    facts = {fact["id"]: fact for fact in result["facts"]}
    for new in incoming["facts"]:
        if new["id"] not in facts:
            facts[new["id"]] = copy.deepcopy(new)
            continue
        old = facts[new["id"]]
        if old["field"] != new["field"]:
            raise ValueError(f"Fact ID reused for another field: {new['id']}")
        combined_sources = sorted(set(old["source_ids"]) | set(new["source_ids"]))
        if (
            old["value"] == new["value"]
            and old["status"] != "conflict"
            and new["status"] != "conflict"
        ):
            old["source_ids"] = combined_sources
            if old["status"] != new["status"]:
                old["status"] = "unconfirmed"
            continue
        alternatives: list[Json] = []
        for fact in (old, new):
            for alternative in fact.get(
                "alternatives", [{"value": fact["value"], "source_ids": fact["source_ids"]}]
            ):
                match = next((a for a in alternatives if a["value"] == alternative["value"]), None)
                if match is None:
                    alternatives.append(copy.deepcopy(alternative))
                else:
                    match["source_ids"] = sorted(
                        set(match["source_ids"]) | set(alternative["source_ids"])
                    )
        old["status"] = "conflict"
        old["alternatives"] = alternatives
        old["source_ids"] = combined_sources
    result["facts"] = list(facts.values())
    validate("profile", result)
    return result
