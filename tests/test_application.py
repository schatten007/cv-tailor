"""Exercise complete and interrupted review-only application state transitions."""

from pathlib import Path

import pytest

from careerkit.application import initialize, load_state, record_event, review, review_issues
from careerkit.contracts import Json
from careerkit.documents import export_document, stage_document


def start(workspace: Path, documents: list[str] | None = None) -> Json:
    return initialize(
        workspace,
        "Example Employer",
        "42",
        "https://example.invalid/jobs/42",
        documents if documents is not None else ["cv"],
    )


def plan(workspace: Path, **constraints: object) -> Json:
    field = {
        "id": "resume",
        "required": True,
        "document_ids": ["cv"],
        "accept": [".pdf", ".docx"],
        "max_files": 1,
        "max_bytes": 5_000_000,
        **constraints,
    }
    return record_event(
        workspace,
        {"type": "plan", "required_sections": ["personal", "documents"], "upload_fields": [field]},
    )


def section(workspace: Path, identifier: str, **overrides: object) -> Json:
    return record_event(
        workspace,
        {
            "type": "section",
            "id": identifier,
            "status": "verified",
            "missing_fields": [],
            "unconfirmed_fields": [],
            "portal_saved": False,
            "evidence": "Synthetic fields read back correctly",
            **overrides,
        },
    )


def upload(workspace: Path, **overrides: object) -> Json:
    return record_event(
        workspace,
        {
            "type": "upload",
            "field_id": "resume",
            "document_ids": ["cv"],
            "evidence": "Synthetic portal displays the selected filename and completion",
            **overrides,
        },
    )


def observe(workspace: Path, **overrides: object) -> Json:
    return record_event(
        workspace,
        {
            "type": "observe",
            "url": "https://example.invalid/jobs/42/review",
            "company": "Example Employer",
            "reference": "42",
            "final_action": "submit_application",
            "validation_errors": [],
            "evidence": "Target job verified; next action submits",
            **overrides,
        },
    )


def ready(workspace: Path) -> Json:
    start(workspace)
    plan(workspace)
    section(workspace, "personal")
    section(workspace, "documents")
    upload(workspace)
    observe(workspace)
    return review(workspace)


def test_complete_flow_stops_at_review_without_submission(workspace: Path) -> None:
    result = ready(workspace)
    assert result["ready"] is True
    assert result["phase"] == "review-ready"
    assert "manually" in result["next_action"]
    state = load_state(workspace)
    assert state["mode"] == "review-only" and "submitted" not in state
    with pytest.raises(FileExistsError):
        start(workspace)


@pytest.mark.parametrize(
    "event",
    [{"type": "submit"}, {"type": "resume", "password": "never-store-this"}, {"type": "unknown"}],
)
def test_unknown_or_submission_events_are_rejected(workspace: Path, event: Json) -> None:
    start(workspace)
    before = load_state(workspace)
    with pytest.raises(ValueError):
        record_event(workspace, event)
    assert load_state(workspace) == before


def test_empty_or_incomplete_application_is_not_ready(workspace: Path) -> None:
    start(workspace)
    assert not review(workspace)["ready"]
    plan(workspace)
    section(workspace, "personal", unconfirmed_fields=["work-authorization"])
    observe(workspace)
    issues = review(workspace)["issues"]
    assert any("unconfirmed" in issue for issue in issues)
    assert any("documents" in issue for issue in issues)
    assert any("Upload not verified" in issue for issue in issues)


@pytest.mark.parametrize(
    "reason",
    [
        "login",
        "signup",
        "captcha",
        "mfa",
        "verification",
        "session-expired",
        "unsupported",
        "missing-input",
    ],
)
def test_handoff_resume_requires_fresh_verification(workspace: Path, reason: str) -> None:
    ready(workspace)
    record_event(
        workspace,
        {
            "type": "block",
            "reason": reason,
            "detail": "Complete this step in the connected browser",
        },
    )
    assert review(workspace)["phase"] == "blocked"
    with pytest.raises(ValueError, match="Resume"):
        section(workspace, "personal")
    record_event(workspace, {"type": "resume"})
    assert not review(workspace)["ready"]
    section(workspace, "personal")
    section(workspace, "documents")
    observe(workspace)
    assert any("needs rechecking" in issue for issue in review(workspace)["issues"])
    upload(workspace)
    observe(workspace)
    assert review(workspace)["ready"]


@pytest.mark.parametrize(
    "constraints",
    [{"max_bytes": 1}, {"accept": [".docx"]}, {"document_ids": []}, {"document_ids": ["other"]}],
)
def test_upload_constraints_are_enforced(workspace: Path, constraints: Json) -> None:
    start(workspace)
    plan(workspace, **constraints)
    with pytest.raises(ValueError):
        upload(workspace)


def test_unknown_limits_are_not_invented(workspace: Path) -> None:
    start(workspace)
    plan(workspace, max_bytes=None, max_files=None, accept=[])
    upload(workspace)


def test_changed_document_invalidates_prior_verified_upload(
    workspace: Path, document: Json
) -> None:
    assert ready(workspace)["ready"]
    document["title"] = "Alex Example updated CV"
    newer = export_document(document, workspace.parent / "updated", "pdf")[0]
    stage_document(workspace, newer, "cv", "cv", "en", replace=True)
    assert not review(workspace)["ready"]
    assert load_state(workspace)["phase"] == "filling"
    upload(workspace)
    observe(workspace)
    assert review(workspace)["ready"]


def test_changed_portal_requirements_invalidate_previous_checks(workspace: Path) -> None:
    ready(workspace)
    record_event(
        workspace, {"type": "plan", "required_sections": ["screening"], "upload_fields": []}
    )
    assert set(load_state(workspace)["required_sections"]) == {"personal", "documents", "screening"}
    assert not review(workspace)["ready"]
    section(workspace, "screening")
    plan(workspace, max_bytes=9_000_000)
    observe(workspace)
    assert not review(workspace)["ready"]
    upload(workspace)
    observe(workspace)
    assert review(workspace)["ready"]


def test_select_rechecks_uploads_and_rejects_unselected_files(workspace: Path) -> None:
    ready(workspace)
    record_event(workspace, {"type": "select", "document_ids": []})
    observe(workspace)
    assert any("unselected" in issue for issue in review(workspace)["issues"])
    record_event(workspace, {"type": "select", "document_ids": ["cv"]})
    upload(workspace)
    observe(workspace)
    assert review(workspace)["ready"]


def test_optional_attachment_can_be_omitted(tmp_path: Path) -> None:
    start(tmp_path, [])
    record_event(
        tmp_path,
        {
            "type": "plan",
            "required_sections": ["personal"],
            "upload_fields": [
                {
                    "id": "other",
                    "required": False,
                    "document_ids": [],
                    "accept": [],
                    "max_files": None,
                    "max_bytes": None,
                }
            ],
        },
    )
    section(tmp_path, "personal")
    observe(tmp_path)
    assert review(tmp_path)["ready"]


def test_wrong_job_or_errors_cannot_pass_final_review(workspace: Path) -> None:
    ready(workspace)
    with pytest.raises(ValueError, match="target company/job"):
        observe(workspace, reference="43")
    observe(workspace, validation_errors=["Please confirm enrollment"])
    assert not review(workspace)["ready"]
    observe(workspace, final_action="unknown")
    assert not review(workspace)["ready"]


def test_sections_and_uploads_must_be_discovered_first(workspace: Path) -> None:
    start(workspace)
    with pytest.raises(ValueError, match="section in a plan"):
        section(workspace, "personal")
    with pytest.raises(ValueError, match="upload field"):
        upload(workspace)
    with pytest.raises(ValueError, match="Duplicate upload"):
        record_event(
            workspace,
            {
                "type": "plan",
                "required_sections": ["personal"],
                "upload_fields": [
                    {
                        "id": "same",
                        "required": False,
                        "document_ids": [],
                        "accept": [],
                        "max_files": None,
                        "max_bytes": None,
                    }
                ]
                * 2,
            },
        )


def test_deleted_staged_file_blocks_review(workspace: Path) -> None:
    ready(workspace)
    for path in (workspace / "documents").iterdir():
        path.unlink()
    assert any("Missing or changed" in issue for issue in review(workspace)["issues"])


def test_required_empty_upload_and_count_rules(workspace: Path, document: Json) -> None:
    start(workspace)
    plan(workspace, document_ids=[])
    with pytest.raises(ValueError, match="count"):
        upload(workspace, document_ids=[])
    other = export_document(document, workspace.parent / "other", "pdf")[0]
    stage_document(workspace, other, "other", "supporting", "en")
    record_event(workspace, {"type": "select", "document_ids": ["cv", "other"]})
    plan(workspace, document_ids=["cv", "other"], max_files=1)
    with pytest.raises(ValueError, match="count"):
        upload(workspace, document_ids=["cv", "other"])
    plan(workspace, document_ids=["cv", "other"], max_files=2)
    upload(workspace, document_ids=["cv", "other"])
    state = load_state(workspace)
    state["uploads"]["resume"]["hashes"] = {}
    assert any("needs rechecking" in issue for issue in review_issues(workspace, state))
