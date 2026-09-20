#!/usr/bin/env python3
"""Install selected, self-contained skills. Preview by default; never overwrite."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def catalog(root: Path) -> dict[str, str]:
    """Load this repository's explicit module catalog."""
    data = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
    skills = data.get("skills")
    if not isinstance(skills, dict) or not all(
        isinstance(k, str) and isinstance(v, str) for k, v in skills.items()
    ):
        raise ValueError("Invalid module catalog")
    return skills


def bundle(root: Path, name: str) -> dict[Path, bytes]:
    """Bundle shared resources so an installed skill has no sibling dependency."""
    skills = catalog(root)
    if name not in skills or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError(f"Unknown skill: {name}")
    source = (root / skills[name]).resolve()
    if not source.is_relative_to(root.resolve()):
        raise ValueError("Skill source escapes repository")
    text = (source / "SKILL.md").read_text(encoding="utf-8")
    for folder in ("references", "scripts", "schemas"):
        text = text.replace(f"../../{folder}/", f"{folder}/")
    payload = {
        Path("SKILL.md"): text.encode("utf-8"),
        Path("LICENSE"): (root / "LICENSE").read_bytes(),
    }
    selections = [
        ("scripts", ".mjs"),
        ("references", ".md"),
        ("schemas", ".json"),
        ("scripts", ".py"),
        ("docs", ".md"),
        ("examples", ".json"),
    ]
    for directory, suffix in selections:
        for path in (root / directory).rglob(f"*{suffix}"):
            if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
                raise ValueError("Do not package resources linked outside the repository")
            payload[path.relative_to(root)] = path.read_bytes()
    payload[Path("scripts/requirements.txt")] = (root / "scripts/requirements.txt").read_bytes()
    payload[Path(".cv-tailor-install.json")] = json.dumps(
        {"skill": name, "source": "schatten007/cv-tailor", "version": "2.0.0"}, indent=2
    ).encode()
    return payload


def install(root: Path, target: Path, names: list[str], *, apply: bool = False) -> list[Path]:
    """Preview or install without modifying existing directories, including Git clones."""
    if not names or len(names) != len(set(names)):
        raise ValueError("Choose at least one skill, without duplicates")
    target = target.expanduser().resolve()
    if target.is_relative_to(root.resolve()):
        raise ValueError("Install outside the source checkout")
    packages = {name: bundle(root, name) for name in names}
    destinations = [target / name for name in names]
    for path in destinations:
        if path.exists() or path.is_symlink():
            raise ValueError(
                f"Target exists: {path}. Preserve/review it before installing; never overwrite a Git checkout."
            )
    if not apply:
        return destinations
    target.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    try:
        for name, files in packages.items():
            destination = target / name
            destination.mkdir()  # exclusive ownership; a race cannot overwrite a user's folder
            created.append(destination)
            for relative, content in files.items():
                path = destination / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open("xb") as stream:
                    stream.write(content)
    except OSError:
        for path in created:
            shutil.rmtree(path)
        raise
    return destinations


def main(argv: list[str] | None = None) -> int:
    """Preview first; require --apply for any writes."""
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--all", action="store_true")
    selection.add_argument("--skills", nargs="+")
    parser.add_argument("--target", type=Path, default=Path.home() / ".config/opencode/skills")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    try:
        names = list(catalog(ROOT)) if args.all else args.skills
        paths = install(ROOT, args.target, names, apply=args.apply)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    print("Installed:" if args.apply else "Preview (add --apply to install):")
    for path in paths:
        print(path)
    if args.apply:
        print("Quit and restart OpenCode to discover the skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
