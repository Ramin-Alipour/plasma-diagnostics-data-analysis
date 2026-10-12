from pathlib import Path
import re
import tomllib


ROOT = Path(__file__).resolve().parents[1]


def test_project_version_matches_citation_changelog_and_readme():
    with (ROOT / "pyproject.toml").open("rb") as stream:
        project = tomllib.load(stream)["project"]
    version = project["version"]

    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    citation_version = re.search(r"(?m)^version:\s*([^\s#]+)\s*$", citation)
    assert citation_version is not None
    assert citation_version.group(1) == version
    assert f"## [{version}]" in changelog

    assert f"**Latest published release: v{version}**" in readme
    release_section = readme.split("## Release", maxsplit=1)[1].split("## Citation", maxsplit=1)[0]
    version_dois = re.findall(r"10\.5281/zenodo\.(\d+)", release_section)
    assert version_dois, "Published version must identify a version-specific Zenodo DOI"
    doi = f"10.5281/zenodo.{version_dois[0]}"
    assert f"https://doi.org/{doi}" in readme
    assert f"[v{version} release](https://doi.org/{doi})" in readme
    assert f"Version v{version}" in readme
    assert doi in readme


def test_citation_uses_the_concept_doi_and_readme_explains_it():
    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    concept_doi = "10.5281/zenodo.23298821"

    assert concept_doi in citation
    assert concept_doi in readme
    assert "version-specific DOI" in readme

def test_release_workflow_packages_existing_tags_without_rewriting_them():
    workflow = (ROOT / ".github" / "workflows" / "package-release-assets.yml").read_text(encoding="utf-8")

    assert "types: [published]" in workflow
    assert "workflow_dispatch:" in workflow
    assert "Align the existing v0.2.2 tag" not in workflow
    assert "-X PATCH" not in workflow
    assert "force\\\\\\\":true" not in workflow
    assert "push:\\n  branches: [main]" not in workflow
    assert "ref: ${{ github.event.release.tag_name || inputs.tag || 'v0.2.2' }}" in workflow

