"""
Tests for source code export and filesystem safety in pybox_dl.
"""

from pathlib import Path
import pytest
import pybox_dl
from pybox_dl import PROGRAM_NAMES


def test_default_export_in_current_working_directory(tmp_path, monkeypatch):
    """Verify default save() exports '<identifier>.py' in the current working directory."""
    monkeypatch.chdir(tmp_path)

    saved_path = pybox_dl.one.save()
    expected_path = tmp_path / "one.py"

    assert isinstance(saved_path, Path)
    assert saved_path == expected_path.resolve()
    assert expected_path.is_file()
    assert expected_path.read_text(encoding="utf-8") == pybox_dl.one.code


def test_export_with_custom_filename(tmp_path):
    """Verify save() with a custom filename writes to the specified target."""
    custom_target = tmp_path / "my_custom_one.py"
    saved_path = pybox_dl.one.save(custom_target)

    assert saved_path == custom_target.resolve()
    assert custom_target.is_file()
    assert custom_target.read_text(encoding="utf-8") == pybox_dl.one.code


def test_export_to_nested_directory_and_creates_parents(tmp_path):
    """Verify save() creates nested parent directories when they do not exist."""
    nested_target = tmp_path / "nested" / "models" / "custom_two.py"
    assert not nested_target.parent.exists()

    saved_path = pybox_dl.two.save(nested_target)

    assert saved_path == nested_target.resolve()
    assert nested_target.is_file()
    assert nested_target.read_text(encoding="utf-8") == pybox_dl.two.code


def test_export_to_existing_directory_uses_default_filename(tmp_path):
    """Verify save() when given a directory saves '<identifier>.py' inside that directory."""
    target_dir = tmp_path / "output_dir"
    target_dir.mkdir(parents=True)

    saved_path = pybox_dl.three.save(target_dir)
    expected_file = target_dir / "three.py"

    assert saved_path == expected_file.resolve()
    assert expected_file.is_file()
    assert expected_file.read_text(encoding="utf-8") == pybox_dl.three.code


def test_export_refuses_overwrite_by_default(tmp_path):
    """Verify save() raises FileExistsError when target exists and overwrite=False."""
    target_file = tmp_path / "existing.py"
    target_file.write_text("existing content", encoding="utf-8")

    with pytest.raises(FileExistsError) as exc_info:
        pybox_dl.four.save(target_file, overwrite=False)

    assert "already exists" in str(exc_info.value)
    assert target_file.read_text(encoding="utf-8") == "existing content"


def test_export_allows_overwrite_when_explicit(tmp_path):
    """Verify save() overwrites target file when overwrite=True is explicitly passed."""
    target_file = tmp_path / "overwrite_me.py"
    target_file.write_text("old content", encoding="utf-8")

    saved_path = pybox_dl.five.save(target_file, overwrite=True)

    assert saved_path == target_file.resolve()
    assert target_file.read_text(encoding="utf-8") == pybox_dl.five.code


@pytest.mark.parametrize("name", PROGRAM_NAMES)
def test_export_all_8_programs(name, tmp_path):
    """Verify every one of the 8 programs exports successfully and content matches exactly."""
    program = getattr(pybox_dl, name)
    out_file = tmp_path / f"export_{name}.py"
    saved = program.save(out_file)

    assert saved == out_file.resolve()
    assert out_file.is_file()
    assert out_file.read_text(encoding="utf-8") == program.code
