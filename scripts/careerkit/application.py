"""Review-only application ledger; never sends requests or controls a browser."""

from __future__ import annotations

import copy
from pathlib import Path

from careerkit.contracts import Json, now, public_url, read_json, safe_id, validate, write_json
from careerkit.documents import private_output, verify_documents

STATE = "application-state.json"
EVENT_KEYS = {
    "plan": {"required_sections", "upload_fields"},
    "select": {"document_ids"},
    "section": {"id", "status", "missing_fields", "unconfirmed_fields", "portal_saved", "evidence"},
    "upload": {"field_id", "document_ids", "evidence"},
    "observe": {"url", "company", "reference", "final_action", "validation_errors", "evidence"},
    "block": {"reason", "detail"},
    "resume": set(),
}


def initialize(
    workspace: Path, company: str, reference: str, url: str, documents: list[str]
) -> Json:
    """Create a new ledger only; never overwrite an existing application."""
    root = private_output(workspace)
    verify_documents(root, documents)
    state: Json = {
        "schema_version": 1,
        "mode": "review-only",
        "phase": "inspecting",
        "job": {"company": company, "reference": reference, "url": public_url(url)},
        "selected_documents": documents,
        "required_sections": [],
        "upload_fields": [],
        "sections": {},
        "uploads": {},
        "observation": None,
        "blocker": None,
        "updated_at": now(),
    }
    validate("application", state)
    write_json(root / STATE, state)
    return state


def load_state(workspace: Path) -> Json:
    """Load and validate a local checkpoint, without assuming remote persistence."""
    state = read_json(workspace / STATE)
    validate("application", state)
    return state


def _check_upload(field: Json, ids: list[str], documents: Json) -> None:
    if set(ids) != set(field["document_ids"]):
        raise ValueError("Observed uploaded documents do not match this field's plan")
    if (field["max_files"] is not None and len(ids) > field["max_files"]) or (
        field["required"] and not ids
    ):
        raise ValueError("Upload field file-count requirement is not met")
    for identifier in ids:
        if identifier not in documents:
            raise ValueError(f"Upload uses an unselected document: {identifier}")
        record = documents[identifier]
        if field["accept"] and Path(record["path"]).suffix.lower() not in field["accept"]:
            raise ValueError(f"Wrong file type for upload field: {identifier}")
        if field["max_bytes"] is not None and record["size_bytes"] > field["max_bytes"]:
            raise ValueError(f"File exceeds upload limit: {identifier}")


def record_event(workspace: Path, event: Json) -> Json:
    """Validate an observed event and checkpoint it; unknown actions are rejected."""
    state = load_state(workspace)
    event_type = event.get("type")
    if not isinstance(event_type, str) or event_type not in EVENT_KEYS:
        raise ValueError("Unknown event; submission is not supported in review-only mode")
    if set(event) != EVENT_KEYS[event_type] | {"type"}:
        raise ValueError(
            f"Expected exactly these {event_type} fields: {sorted(EVENT_KEYS[event_type])}"
        )
    if state["blocker"] and event_type not in {"resume", "observe", "block"}:
        raise ValueError("Resume after the manual handoff before recording more form actions")
    result = copy.deepcopy(state)
    result["updated_at"] = now()
    result["phase"] = "blocked" if state["blocker"] else "filling"
    if event_type == "plan":
        # Validate shape before merging; discovered sections can only accumulate.
        result["required_sections"] = event["required_sections"]
        result["upload_fields"] = event["upload_fields"]
        validate("application", result)
        result["required_sections"] = sorted(
            set(state["required_sections"]) | set(event["required_sections"])
        )
        fields = {field["id"]: field for field in state["upload_fields"]}
        for field in event["upload_fields"]:
            if fields.get(field["id"]) != field:
                result["uploads"].pop(field["id"], None)
            fields[field["id"]] = field
        result["upload_fields"] = list(fields.values())
        result["observation"] = None
    elif event_type == "select":
        result["selected_documents"] = event["document_ids"]
        for upload in result["uploads"].values():
            upload["status"] = "needs-recheck"
        result["observation"] = None
    elif event_type == "section":
        identifier = safe_id(event["id"])
        if identifier not in result["required_sections"]:
            raise ValueError("Record the section in a plan event before verifying it")
        result["sections"][identifier] = {
            key: value for key, value in event.items() if key not in {"type", "id"}
        }
        result["observation"] = None
    elif event_type == "upload":
        identifier = event["field_id"]
        field = next(
            (field for field in result["upload_fields"] if field["id"] == identifier), None
        )
        if field is None:
            raise ValueError("Record the upload field in a plan event first")
        result["uploads"][identifier] = {
            "document_ids": event["document_ids"],
            "hashes": {},
            "status": "verified",
            "evidence": event["evidence"],
        }
        validate("application", result)
        documents = verify_documents(workspace, result["selected_documents"])
        _check_upload(field, event["document_ids"], documents)
        result["uploads"][identifier]["hashes"] = {
            identifier: documents[identifier]["sha256"] for identifier in event["document_ids"]
        }
        result["observation"] = None
    elif event_type == "observe":
        result["observation"] = {key: value for key, value in event.items() if key != "type"}
    elif event_type == "block":
        result["blocker"] = {"reason": event["reason"], "detail": event["detail"]}
        result["phase"] = "blocked"
        result["observation"] = None
    elif event_type == "resume":
        result["blocker"] = None
        result["phase"] = "filling"
        result["observation"] = None
        for section in result["sections"].values():
            section["status"] = "needs-recheck"
        for upload in result["uploads"].values():
            upload["status"] = "needs-recheck"
    validate("application", result)
    verify_documents(workspace, result["selected_documents"])
    write_json(workspace / STATE, result, replace=True)
    return result


def review_issues(workspace: Path, state: Json) -> list[str]:
    """Check recorded completeness and file identity, not live portal correctness."""
    validate("application", state)
    issues: list[str] = []
    if state["blocker"]:
        issues.append(f"Manual handoff: {state['blocker']['reason']}")
    if not state["required_sections"]:
        issues.append("No section inventory has been recorded")
    for identifier in state["required_sections"]:
        section = state["sections"].get(identifier)
        if not section or section["status"] != "verified":
            issues.append(f"Section needs verification: {identifier}")
        elif section["missing_fields"] or section["unconfirmed_fields"]:
            issues.append(f"Missing or unconfirmed answers: {identifier}")
    observation = state["observation"]
    if not observation or observation["final_action"] != "submit_application":
        issues.append("Final application action has not been observed")
    elif observation["validation_errors"]:
        issues.append("Portal still shows validation errors")
    try:
        documents = verify_documents(workspace, state["selected_documents"])
    except (ValueError, OSError) as error:
        issues.append(str(error))
        return issues
    uploaded: set[str] = set()
    for field in state["upload_fields"]:
        upload = state["uploads"].get(field["id"])
        if not upload:
            if field["required"] or field["document_ids"]:
                issues.append(f"Upload not verified: {field['id']}")
            continue
        try:
            _check_upload(field, upload["document_ids"], documents)
            expected = {
                identifier: documents[identifier]["sha256"] for identifier in upload["document_ids"]
            }
            if upload["status"] != "verified" or upload["hashes"] != expected:
                issues.append(f"Upload version needs rechecking: {field['id']}")
            else:
                uploaded.update(upload["document_ids"])
        except ValueError as error:
            issues.append(f"{field['id']}: {error}")
    for identifier in set(state["selected_documents"]) - uploaded:
        issues.append(f"Selected document not verified on portal: {identifier}")
    return issues


def review(workspace: Path) -> Json:
    """Mark ready only after all checks; never submit or mark an application sent."""
    state = load_state(workspace)
    issues = review_issues(workspace, state)
    state["phase"] = "blocked" if state["blocker"] else "filling" if issues else "review-ready"
    state["updated_at"] = now()
    write_json(workspace / STATE, state, replace=True)
    return {
        "ready": not issues,
        "phase": state["phase"],
        "job": state["job"],
        "issues": issues,
        "next_action": (
            "User reviews and submits manually"
            if not issues
            else "Resolve issues and inspect the portal again"
        ),
    }
