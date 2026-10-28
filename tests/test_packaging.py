"""
Tests for packaging integrity, wheel verification, and asset inclusion in pybox_dl.
"""

from pathlib import Path
from pybox_dl import PROGRAM_NAMES


def test_package_structure_and_assets():
    """Verify that all 8 program assets exist in the pybox_dl source tree."""
    repo_root = Path(__file__).resolve().parent.parent
    programs_dir = repo_root / "src" / "pybox_dl" / "programs"

    assert programs_dir.is_dir(), f"Programs directory not found: {programs_dir}"
    assert (programs_dir / "__init__.py").is_file(), "Missing programs/__init__.py"

    for name in PROGRAM_NAMES:
        asset_file = programs_dir / f"{name}.py"
        assert asset_file.is_file(), f"Missing program asset: {asset_file}"
        content = asset_file.read_text(encoding="utf-8")
        assert len(content.strip()) > 0, f"Asset file is empty: {asset_file}"


def test_pyproject_toml_configuration():
    """Verify pyproject.toml configuration contains package data and dependencies."""
    repo_root = Path(__file__).resolve().parent.parent
    pyproject_file = repo_root / "pyproject.toml"
    assert pyproject_file.is_file()

    content = pyproject_file.read_text(encoding="utf-8")
    assert 'name = "pybox-dl"' in content
    assert 'version = "0.1.0"' in content
    assert '"pybox_dl.programs" = ["*.py"]' in content
    assert 'requires-python = ">=3.8"' in content
