from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_release_packaging_never_rewrites_tags_or_runs_on_main_push():
    """Release packaging must consume an existing tag, never move one."""
    workflow = (ROOT / ".github" / "workflows" / "package-release-assets.yml").read_text(
        encoding="utf-8"
    )

    assert "PATCH" not in workflow
    assert '"force":true' not in workflow
    assert "TARGET_SHA" not in workflow
    assert "push:" not in workflow
    assert "types: [published]" in workflow
    assert "workflow_dispatch:" in workflow
    assert "Check out the existing release tag" in workflow
