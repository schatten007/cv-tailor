"""Small command interface for local artifacts; all browser actions stay in MCP."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


def doctor(roots: list[Path] | None = None) -> dict[str, Any]:
    """Report optional dependency/file availability without changing configuration."""
    roots = (
        roots
        if roots is not None
        else [
            Path.home() / ".config/opencode/skills",
            Path.home() / ".agents/skills",
            Path.home() / ".claude/skills",
            Path.cwd() / ".opencode/skills",
        ]
    )
    names = [
        "research",
        "research-deep",
        "research-report",
        "research-add-items",
        "research-add-fields",
    ]
    return {
        "python": sys.version.split()[0],
        "python_supported": sys.version_info >= (3, 11),
        "libraries": {
            name: importlib.util.find_spec(name) is not None
            for name in ("jsonschema", "docx", "reportlab", "pypdf", "yaml")
        },
        "research_skill_files": {
            name: any((root / name / "SKILL.md").is_file() for root in roots) for name in names
        },
        "browser_mcp": "Verify exposed tools in OpenCode; file discovery does not prove tool access",
        "changes_made": False,
    }


def parser() -> argparse.ArgumentParser:
    """Build explicit, noninteractive helper commands."""
    root = argparse.ArgumentParser(
        description="CV Tailor local document and review-only state helpers"
    )
    commands = root.add_subparsers(dest="command", required=True)
    check = commands.add_parser("doctor", help="Check optional dependencies; make no changes")
    check.add_argument("--skills-root", type=Path, action="append")
    verify = commands.add_parser("validate")
    verify.add_argument(
        "--kind",
        required=True,
        choices=["profile", "document", "company-brief", "manifest", "application"],
    )
    verify.add_argument("--file", type=Path, required=True)
    inspect = commands.add_parser("inspect")
    inspect.add_argument("--file", type=Path, required=True)
    export = commands.add_parser("export")
    export.add_argument("--input", type=Path, required=True)
    export.add_argument(
        "--output", type=Path, required=True, help="Output base path, without extension"
    )
    export.add_argument("--format", choices=["pdf", "docx", "both"], default="both")
    export.add_argument(
        "--font", type=Path, help="Optional TrueType font for additional PDF glyphs"
    )
    merge = commands.add_parser("merge")
    merge.add_argument("--inputs", type=Path, nargs="+", required=True)
    merge.add_argument("--output", type=Path, required=True)
    stage = commands.add_parser("stage")
    stage.add_argument("--workspace", type=Path, required=True)
    stage.add_argument("--file", type=Path, required=True)
    stage.add_argument("--id", required=True)
    stage.add_argument("--kind", choices=["cv", "cover-letter", "supporting"], required=True)
    stage.add_argument("--language", default="en")
    stage.add_argument(
        "--replace", action="store_true", help="Select a new version for an existing document ID"
    )
    files = commands.add_parser(
        "files", help="Verify selected files and return local upload records"
    )
    files.add_argument("--workspace", type=Path, required=True)
    files.add_argument("--documents", nargs="+", required=True)
    profiles = commands.add_parser("profile-merge")
    profiles.add_argument("--base", type=Path, required=True)
    profiles.add_argument("--incoming", type=Path, required=True)
    profiles.add_argument("--output", type=Path, required=True)
    application = commands.add_parser("application")
    actions = application.add_subparsers(dest="action", required=True)
    for action in ("init", "record", "status", "review"):
        command = actions.add_parser(action)
        command.add_argument("--workspace", type=Path, required=True)
        if action == "init":
            command.add_argument("--company", required=True)
            command.add_argument("--reference", required=True)
            command.add_argument("--url", required=True)
            command.add_argument("--documents", nargs="*", default=[])
        if action == "record":
            command.add_argument("--event", type=Path, required=True)
    return root


def _run(args: argparse.Namespace) -> tuple[dict[str, Any] | str, int]:
    if args.command == "doctor":
        return doctor(args.skills_root), 0
    # Lazy imports keep doctor and --help usable before optional dependencies exist.
    from careerkit import application, documents
    from careerkit.contracts import merge_profiles, read_json, validate, write_json

    if args.command == "validate":
        validate(args.kind, read_json(args.file))
        return {"valid": True, "kind": args.kind}, 0
    if args.command == "inspect":
        return documents.inspect_text(args.file), 0
    if args.command == "export":
        paths = documents.export_document(
            read_json(args.input), args.output, args.format, args.font
        )
        return {"files": [str(path) for path in paths]}, 0
    if args.command == "merge":
        return {
            "pages": documents.merge_pdfs(args.inputs, args.output),
            "file": str(args.output),
        }, 0
    if args.command == "stage":
        result = documents.stage_document(
            args.workspace, args.file, args.id, args.kind, args.language, replace=args.replace
        )
        return result, 0
    if args.command == "files":
        return documents.verify_documents(args.workspace, args.documents), 0
    if args.command == "profile-merge":
        result = merge_profiles(read_json(args.base), read_json(args.incoming))
        write_json(documents.private_output(args.output), result)
        return {
            "file": str(args.output),
            "conflicts": [fact["id"] for fact in result["facts"] if fact["status"] == "conflict"],
        }, 0
    if args.action == "init":
        result = application.initialize(
            args.workspace, args.company, args.reference, args.url, args.documents
        )
        return result, 0
    if args.action == "record":
        return application.record_event(args.workspace, read_json(args.event)), 0
    if args.action == "review":
        result = application.review(args.workspace)
        return result, 0 if result["ready"] else 2
    state = application.load_state(args.workspace)
    issues = application.review_issues(args.workspace, state)
    return {
        "job": state["job"],
        "mode": state["mode"],
        "recorded_phase": state["phase"],
        "ready": not issues,
        "issues": issues,
        "selected_documents": state["selected_documents"],
    }, 0


def main(argv: list[str] | None = None) -> int:
    """Run a local command and return a meaningful nonzero status on failure."""
    args = parser().parse_args(argv)
    try:
        output, code = _run(args)
    except ModuleNotFoundError as error:
        print(
            f"Missing optional dependency: {error.name}. Install scripts/requirements.txt in a virtual environment.",
            file=sys.stderr,
        )
        return 2
    except (OSError, ValueError, TypeError, KeyError, EOFError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    print(output if isinstance(output, str) else json.dumps(output, indent=2, ensure_ascii=True))
    return code
