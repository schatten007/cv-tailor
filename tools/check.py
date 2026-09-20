#!/usr/bin/env python3
"""Validate skill frontmatter, bundled references, schemas, and examples."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

if __package__ in (None, ""):  # allow `python tools/check.py` as well as `-m tools.check`
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.install import ROOT, bundle, catalog


def check(root: Path = ROOT) -> list[str]:
    """Return validation errors without modifying any files."""
    errors: list[str] = []
    allowed = {"name", "description", "license", "compatibility", "metadata"}
    for name, directory in catalog(root).items():
        base = root / directory
        text = (base / "SKILL.md").read_text(encoding="utf-8")
        try:
            frontmatter = yaml.safe_load(text.split("---", 2)[1])
            assert isinstance(frontmatter, dict)
            assert set(frontmatter) <= allowed
            assert frontmatter["name"] == name
            assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) and len(name) <= 64
            assert (
                isinstance(frontmatter["description"], str)
                and 1 <= len(frontmatter["description"]) <= 1024
            )
            assert frontmatter["license"] == "MIT"
            assert all(
                isinstance(k, str) and isinstance(v, str)
                for k, v in frontmatter.get("metadata", {}).items()
            )
        except (IndexError, KeyError, AssertionError, yaml.YAMLError) as error:
            errors.append(f"{name}: invalid frontmatter ({error})")
        for relative in re.findall(
            r"`((?:\.\./)*(?:references|scripts|schemas)/[^`\s]+\.(?:md|py|json))`", text
        ):
            if not (base / relative).is_file():
                errors.append(f"{name}: missing reference {relative}")
        package = bundle(root, name)
        for relative in re.findall(
            r"`((?:references|scripts|schemas)/[^`\s]+\.(?:md|py|json))`",
            package[Path("SKILL.md")].decode(),
        ):
            if Path(relative) not in package:
                errors.append(f"{name}: unbundled dependency {relative}")
    for path in (root / "schemas").glob("*.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    return errors


def main() -> int:
    """Print the result for local use or CI."""
    errors = check()
    for error in errors:
        print(error)
    if not errors:
        print(f"Validated {len(catalog(ROOT))} standalone skills, references, and schemas")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
