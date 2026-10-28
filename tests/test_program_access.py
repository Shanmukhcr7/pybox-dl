"""
Tests for program access, attributes, and non-execution behavior in pybox_dl.
"""

import sys
import pybox_dl
from pybox_dl import Program, PROGRAM_NAMES, PROGRAMS


def test_import_pybox_dl():
    """Verify pybox_dl imports cleanly and exposes expected package metadata."""
    assert hasattr(pybox_dl, "__version__")
    assert pybox_dl.__version__ == "0.1.0"
    assert issubclass(Program, object)


def test_program_names_list():
    """Verify PROGRAM_NAMES contains exactly the 8 identifiers."""
    expected = (
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
    )
    assert PROGRAM_NAMES == expected
    assert len(PROGRAM_NAMES) == 8


def test_all_8_program_attributes_exist():
    """Verify all 8 program attributes are directly accessible on pybox_dl."""
    for name in PROGRAM_NAMES:
        assert hasattr(pybox_dl, name), f"Missing attribute: pybox_dl.{name}"
        program = getattr(pybox_dl, name)
        assert isinstance(program, Program)
        assert program.identifier == name
        assert program.filename == f"{name}.py"


def test_programs_dictionary_mapping():
    """Verify pybox_dl.PROGRAMS correctly maps identifiers to Program instances."""
    assert len(PROGRAMS) == 8
    for name in PROGRAM_NAMES:
        assert name in PROGRAMS
        assert PROGRAMS[name] is getattr(pybox_dl, name)


def test_program_representation():
    """Verify Program.__repr__ returns Program('<identifier>')."""
    for name in PROGRAM_NAMES:
        program = getattr(pybox_dl, name)
        assert repr(program) == f"Program({name!r})"


def test_programs_are_not_executed_on_import_or_access():
    """
    Verify that accessing programs and reading their source code does not execute them.
    TensorFlow or heavy frameworks should NOT be imported, and modules must not be added to sys.modules.
    """
    for name in PROGRAM_NAMES:
        prog = getattr(pybox_dl, name)
        code = prog.code
        assert isinstance(code, str)
        assert len(code) > 0
        assert f"pybox_dl.programs.{name}" not in sys.modules
