"""Exercise public commands and installation from an unrelated working directory."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from careerkit.cli import doctor, main
from careerkit.contracts import Json, write_json
from tools import install as installer

ROOT = Path(__file__).resolve().parents[1]


def test_doctor_is_read_only_and_detects_available_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    research = tmp_path / "research"
    research.mkdir()
    (research / "SKILL.md").write_text("synthetic", encoding="utf-8")
    monkeypatch.setattr(importlib.util, "find_spec", lambda name: None)
    report = doctor([tmp_path])
    assert report["research_skill_files"]["research"]
    assert not report["research_skill_files"]["research-deep"]
    assert not any(report["libraries"].values())
    assert report["changes_made"] is False
    assert main(["doctor", "--skills-root", str(tmp_path)]) == 0
    assert doctor()["changes_made"] is False


def test_cli_document_pipeline_and_error_codes(
    tmp_path: Path, document: Json, profile: Json, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "document.json"
    write_json(source, document)
    assert main(["validate", "--kind", "document", "--file", str(source)]) == 0
    assert main(["export", "--input", str(source), "--output", str(tmp_path / "cv")]) == 0
    assert main(["inspect", "--file", str(tmp_path / "cv.pdf")]) == 0
    assert (
        main(
            [
                "merge",
                "--inputs",
                str(tmp_path / "cv.pdf"),
                "--output",
                str(tmp_path / "bundle.pdf"),
            ]
        )
        == 0
    )
    workspace = tmp_path / "app"
    assert (
        main(
            [
                "stage",
                "--workspace",
                str(workspace),
                "--file",
                str(tmp_path / "cv.docx"),
                "--id",
                "cv",
                "--kind",
                "cv",
            ]
        )
        == 0
    )
    capsys.readouterr()  # discard earlier command output before capturing files JSON
    assert main(["files", "--workspace", str(workspace), "--documents", "cv"]) == 0
    records = json.loads(capsys.readouterr().out)
    assert Path(records["cv"]["absolute_path"]).is_file()
    assert len(records["cv"]["sha256"]) == 64
    base = tmp_path / "profile.json"
    write_json(base, profile)
    assert (
        main(
            [
                "profile-merge",
                "--base",
                str(base),
                "--incoming",
                str(base),
                "--output",
                str(tmp_path / "merged-profile.json"),
            ]
        )
        == 0
    )
    assert (
        main(
            [
                "application",
                "init",
                "--workspace",
                str(workspace),
                "--company",
                "Example Employer",
                "--reference",
                "42",
                "--url",
                "https://example.invalid/jobs/42",
                "--documents",
                "cv",
            ]
        )
        == 0
    )
    assert main(["application", "status", "--workspace", str(workspace)]) == 0
    assert main(["application", "review", "--workspace", str(workspace)]) == 2
    event = tmp_path / "event.json"
    write_json(event, {"type": "block", "reason": "mfa", "detail": "Manual handoff"})
    assert (
        main(["application", "record", "--workspace", str(workspace), "--event", str(event)]) == 0
    )
    assert main(["export", "--input", str(source), "--output", str(tmp_path / "cv")]) == 2
    assert main(["inspect", "--file", str(tmp_path / "missing.md")]) == 2
    assert "Error:" in capsys.readouterr().err


def test_preview_creates_nothing(tmp_path: Path) -> None:
    target = tmp_path / "not-created" / "skills"
    assert installer.install(ROOT, target, ["cover-letter"]) == [target / "cover-letter"]
    assert not target.exists()


@pytest.mark.parametrize("name", list(installer.catalog(ROOT)))
def test_standalone_install_has_every_resource(tmp_path: Path, name: str) -> None:
    destination = installer.install(ROOT, tmp_path / "skills", [name], apply=True)[0]
    body = (destination / "SKILL.md").read_text(encoding="utf-8")
    frontmatter = yaml.safe_load(body.split("---", 2)[1])
    assert frontmatter["name"] == destination.name
    assert frontmatter["license"] == "MIT"
    assert "../../references/" not in body
    assert (destination / "references/common.md").is_file()
    assert (destination / "references/application-workflow.md").is_file()
    assert (destination / "schemas/document.schema.json").is_file()
    result = subprocess.run(
        [
            sys.executable,
            str(destination / "scripts/cvtool.py"),
            "validate",
            "--kind",
            "document",
            "--file",
            str(destination / "examples/document.json"),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["valid"]
    # Doctor remains usable even with site-packages (optional dependencies) disabled.
    minimal = subprocess.run(
        [sys.executable, "-S", str(destination / "scripts/cvtool.py"), "doctor"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert minimal.returncode == 0, minimal.stderr
    assert not json.loads(minimal.stdout)["libraries"]["jsonschema"]


def test_missing_dependency_has_actionable_message(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-S",
            str(ROOT / "scripts/cvtool.py"),
            "validate",
            "--kind",
            "document",
            "--file",
            str(ROOT / "examples/document.json"),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert "Missing optional dependency" in result.stderr


def test_installer_refuses_existing_targets_and_invalid_selection(tmp_path: Path) -> None:
    existing = tmp_path / "skills/cover-letter"
    existing.mkdir(parents=True)
    local = existing / "SKILL.md"
    local.write_text("User customization", encoding="utf-8")
    with pytest.raises(ValueError, match="Target exists"):
        installer.install(ROOT, existing.parent, ["cover-letter"], apply=True)
    assert local.read_text() == "User customization"
    for names in ([], ["cover-letter", "cover-letter"], ["does-not-exist"]):
        with pytest.raises(ValueError):
            installer.install(ROOT, tmp_path / "new", names)
    with pytest.raises(ValueError, match="outside"):
        installer.install(ROOT, ROOT / "nested", ["cover-letter"])


def test_bad_catalog_cannot_escape_root(tmp_path: Path) -> None:
    catalog = tmp_path / "catalog.json"
    catalog.write_text('{"skills": []}', encoding="utf-8")
    with pytest.raises(ValueError, match="catalog"):
        installer.catalog(tmp_path)
    catalog.write_text('{"skills": {"escape": "../elsewhere"}}', encoding="utf-8")
    with pytest.raises(ValueError, match="escapes"):
        installer.bundle(tmp_path, "escape")


def test_failed_install_rolls_back_only_new_folders(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "skills"
    target.mkdir()
    unrelated = target / "user-data.txt"
    unrelated.write_text("keep", encoding="utf-8")
    original_open = Path.open

    def failing_open(self: Path, mode: str = "r", *args: object, **kwargs: object):
        if mode == "xb" and self.name == "LICENSE":
            raise OSError("simulated write failure")
        return original_open(self, mode, *args, **kwargs)

    monkeypatch.setattr(Path, "open", failing_open)
    with pytest.raises(OSError):
        installer.install(ROOT, target, ["cover-letter"], apply=True)
    assert unrelated.read_text() == "keep"
    assert not (target / "cover-letter").exists()


def test_installer_cli_preview_apply_and_existing_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(installer, "ROOT", ROOT)
    args = ["--skills", "interview-prep", "--target", str(tmp_path / "skills")]
    assert installer.main(args) == 0
    assert installer.main(args + ["--apply"]) == 0
    assert installer.main(args + ["--apply"]) == 2
