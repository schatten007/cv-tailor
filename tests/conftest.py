"""Synthetic, per-test candidate artifacts; never use real application data."""

from pathlib import Path

import pytest

from careerkit.contracts import Json, read_json
from careerkit.documents import export_document, stage_document

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def document() -> Json:
    return read_json(ROOT / "examples/document.json")


@pytest.fixture
def profile() -> Json:
    return read_json(ROOT / "examples/profile.json")


@pytest.fixture
def brief() -> Json:
    return read_json(ROOT / "examples/company-brief.json")


@pytest.fixture
def workspace(tmp_path: Path, document: Json) -> Path:
    outputs = export_document(document, tmp_path / "cv", "both")
    workspace = tmp_path / "application"
    stage_document(workspace, outputs[1], "cv", "cv", "en")
    return workspace
