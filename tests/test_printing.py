"""
Tests for source code printing and direct inspection in pybox_dl.
"""

import pytest
import pybox_dl
from pybox_dl import PROGRAM_NAMES


@pytest.mark.parametrize("name", PROGRAM_NAMES)
def test_str_matches_code_property(name):
    """Verify that str(pybox_dl.<name>) returns the exact content of .code."""
    program = getattr(pybox_dl, name)
    assert str(program) == program.code
    assert len(program.code) > 0


@pytest.mark.parametrize("name", PROGRAM_NAMES)
def test_printing_program(name, capsys):
    """Verify that print(pybox_dl.<name>) prints the complete source code to stdout."""
    program = getattr(pybox_dl, name)
    print(program)
    captured = capsys.readouterr()
    assert captured.out == f"{program.code}\n"
    assert captured.err == ""


def test_code_property_is_string():
    """Verify that .code is a valid UTF-8 string containing actual source code."""
    for name in PROGRAM_NAMES:
        program = getattr(pybox_dl, name)
        code = program.code
        assert isinstance(code, str)
        assert len(code.strip()) > 0
