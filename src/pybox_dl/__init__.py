"""
pybox-dl: Bundles 8 Deep Learning Python programs into one installable package with source inspection and export capabilities.
"""

from __future__ import annotations

from typing import Dict, Tuple

from .core import Program

__version__ = "0.1.0"

PROGRAM_NAMES: Tuple[str, ...] = (
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
)

PROGRAMS: Dict[str, Program] = {name: Program(name) for name in PROGRAM_NAMES}

one: Program = PROGRAMS["one"]
two: Program = PROGRAMS["two"]
three: Program = PROGRAMS["three"]
four: Program = PROGRAMS["four"]
five: Program = PROGRAMS["five"]
six: Program = PROGRAMS["six"]
seven: Program = PROGRAMS["seven"]
eight: Program = PROGRAMS["eight"]

__all__ = [
    "Program",
    "PROGRAM_NAMES",
    "PROGRAMS",
    "__version__",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
]
