"""
Tests for error handling, missing assets, and invalid inputs in pybox_dl.
"""

from pathlib import Path
import pytest
from pybox_dl import Program


def test_invalid_program_identifier():
    """Verify Program rejects empty or non-string identifiers."""
    with pytest.raises(ValueError):
        Program("")

    with pytest.raises(ValueError):
        Program(None)  # type: ignore

    with pytest.raises(ValueError):
        Program(123)  # type: ignore


def test_missing_packaged_source_file():
    """Verify accessing .code for a non-existent program raises FileNotFoundError."""
    prog = Program("non_existent_dl_model")
    with pytest.raises(FileNotFoundError) as exc_info:
        _ = prog.code

    assert "non_existent_dl_model" in str(exc_info.value)


def test_export_destination_collision_with_existing_directory(tmp_path):
    """Verify that attempting to overwrite an existing directory raises IsADirectoryError."""
    prog = Program("sample")
    prog._read_source = lambda: "# sample code"  # type: ignore

    dir_collision = tmp_path / "sample.py"
    dir_collision.mkdir()

    with pytest.raises(IsADirectoryError) as exc_info:
        prog.save(dir_collision, overwrite=True)

    assert "is an existing directory" in str(exc_info.value)


def test_export_creates_clean_error_on_missing_source():
    """Verify save() raises FileNotFoundError if underlying source asset is missing."""
    prog = Program("ghost")
    with pytest.raises(FileNotFoundError):
        prog.save("ghost.py")
