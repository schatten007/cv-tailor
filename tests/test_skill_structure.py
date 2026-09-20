"""Check complete standalone packages against the native OpenCode skill contract."""

from tools.check import check


def test_skill_frontmatter_references_and_schemas() -> None:
    assert check() == []
