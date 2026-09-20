"""Evidence provenance, conflict preservation, and portable contract validation."""

import copy
from pathlib import Path

import pytest

from careerkit.contracts import (
    Json,
    local_path,
    merge_profiles,
    public_url,
    read_json,
    safe_id,
    validate,
    write_json,
)


def test_supplied_examples_validate(profile: Json, document: Json, brief: Json) -> None:
    for kind, data in [("profile", profile), ("document", document), ("company-brief", brief)]:
        validate(kind, data)


def test_profile_merge_preserves_conflict_provenance(profile: Json) -> None:
    before = copy.deepcopy(profile)
    incoming = {
        "schema_version": 1,
        "sources": [{"id": "new-chat", "label": "New statement"}],
        "facts": [
            {
                "id": "name",
                "field": "identity.full_name",
                "value": "Another Example",
                "status": "confirmed",
                "source_ids": ["new-chat"],
            }
        ],
    }
    result = merge_profiles(profile, incoming)
    name = result["facts"][0]
    assert profile == before
    assert name["status"] == "conflict"
    assert name["alternatives"] == [
        {"value": "Alex Example", "source_ids": ["chat-01"]},
        {"value": "Another Example", "source_ids": ["new-chat"]},
    ]
    again = merge_profiles(result, incoming)
    assert again["facts"][0]["alternatives"] == name["alternatives"]
    assert merge_profiles(profile, profile) == profile


def test_merge_adds_evidence_and_does_not_upgrade_uncertainty(profile: Json) -> None:
    incoming = copy.deepcopy(profile)
    incoming["facts"][0]["status"] = "unconfirmed"
    incoming["facts"].append(
        {
            "id": "java",
            "field": "skills.java",
            "value": "Coursework",
            "status": "confirmed",
            "source_ids": ["chat-01"],
        }
    )
    result = merge_profiles(profile, incoming)
    assert result["facts"][0]["status"] == "unconfirmed"
    assert result["facts"][-1]["id"] == "java"


@pytest.mark.parametrize(
    "case",
    [
        "source-reuse",
        "fact-reuse",
        "unknown-source",
        "duplicate-source",
        "duplicate-fact",
        "duplicate-field",
        "invalid-status",
    ],
)
def test_invalid_evidence_is_rejected(profile: Json, case: str) -> None:
    incoming = copy.deepcopy(profile)
    if case == "source-reuse":
        incoming["sources"][0]["label"] = "Different document with reused ID"
    elif case == "fact-reuse":
        incoming["facts"][0]["field"] = "identity.location"
    elif case == "unknown-source":
        incoming["facts"][0]["source_ids"] = ["invented"]
    elif case == "duplicate-source":
        incoming["sources"].append(incoming["sources"][0])
    elif case == "duplicate-fact":
        incoming["facts"].append(incoming["facts"][0])
    elif case == "duplicate-field":
        incoming["facts"][1]["field"] = incoming["facts"][0]["field"]
    else:
        incoming["facts"][0]["status"] = "probably"
    with pytest.raises(ValueError):
        merge_profiles(profile, incoming)


@pytest.mark.parametrize(
    "case",
    [
        "missing-citation",
        "wrong-citation",
        "unknown-vendor",
        "identified-without-evidence",
        "wrong-ats-citation",
        "invalid-date",
    ],
)
def test_company_claims_need_real_references(brief: Json, case: str) -> None:
    if case == "missing-citation":
        brief["findings"][0]["source_ids"] = []
    elif case == "wrong-citation":
        brief["findings"][0]["source_ids"] = ["missing"]
    elif case == "unknown-vendor":
        brief["ats"]["vendor"] = "Guessed from company size"
    elif case == "identified-without-evidence":
        brief["ats"] = {"vendor": "SAP", "status": "likely", "source_ids": []}
    elif case == "wrong-ats-citation":
        brief["ats"]["source_ids"] = ["missing"]
    else:
        brief["researched_at"] = "yesterday"
    with pytest.raises(ValueError):
        validate("company-brief", brief)


def test_identified_ats_can_be_supported(brief: Json) -> None:
    brief["ats"] = {"vendor": "Example ATS", "status": "likely", "source_ids": ["job-42"]}
    validate("company-brief", brief)


@pytest.mark.parametrize(
    "url",
    [
        "file:///etc/passwd",
        "http://example.invalid",
        "https://user:secret@example.invalid",
        "https://example.invalid?access_token=secret",
        "https://example.invalid#id_token=secret",
    ],
)
def test_job_urls_exclude_credentials_and_auth_callbacks(url: str) -> None:
    with pytest.raises(ValueError):
        public_url(url)


def test_urls_support_local_fixtures_and_public_spa_routes() -> None:
    for url in ["http://127.0.0.1:8765/portal.html", "https://example.invalid/#/jobs/42"]:
        assert public_url(url) == url


@pytest.mark.parametrize("relative", ["../secret.pdf", "C:/secret.pdf", "nested\\secret.pdf", "."])
def test_manifest_paths_cannot_escape(tmp_path: Path, relative: str) -> None:
    with pytest.raises(ValueError):
        local_path(tmp_path, relative)
    assert local_path(tmp_path, "documents/cv.pdf") == tmp_path / "documents/cv.pdf"


@pytest.mark.parametrize("value", ["../cv", "A CV", "cv--v2", ""])
def test_document_ids_are_paths_safe(value: str) -> None:
    with pytest.raises(ValueError):
        safe_id(value)


def test_bom_json_and_exclusive_writes(tmp_path: Path) -> None:
    path = tmp_path / "record.json"
    path.write_text('\ufeff{"name":"Müller"}', encoding="utf-8")
    assert read_json(path) == {"name": "Müller"}
    with pytest.raises(FileExistsError):
        write_json(path, {"different": True})
    write_json(path, {"name": "Schröder"}, replace=True)
    assert read_json(path)["name"] == "Schröder"
    path.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="JSON object"):
        read_json(path)
    with pytest.raises(ValueError, match="Unknown record"):
        validate("unknown", {})


def test_atomic_replacement_failure_preserves_existing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "record.json"
    write_json(path, {"original": True})

    def fail_replace(self: Path, target: Path) -> Path:
        raise OSError("simulated filesystem error")

    monkeypatch.setattr(Path, "replace", fail_replace)
    with pytest.raises(OSError):
        write_json(path, {"new": True}, replace=True)
    assert read_json(path) == {"original": True}
    assert list(tmp_path.iterdir()) == [path]
