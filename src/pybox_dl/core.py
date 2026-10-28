"""
Core implementation of the PyBox DL Program abstraction.
"""

from __future__ import annotations

import os
from pathlib import Path
import tempfile
from typing import Union


class Program:
    """
    Represents an individual bundled Deep Learning Python program within pybox_dl.

    Provides safe inspection of original source code without executing it,
    as well as export functionality to save standalone .py files.
    """

    def __init__(self, identifier: str) -> None:
        if not identifier or not isinstance(identifier, str):
            raise ValueError(f"Program identifier must be a non-empty string, got: {identifier!r}")
        self._identifier: str = identifier
        self._filename: str = f"{identifier}.py"

    @property
    def identifier(self) -> str:
        """The identifier of this program (e.g., 'one', 'two')."""
        return self._identifier

    @property
    def filename(self) -> str:
        """The default filename for this program (e.g., 'one.py')."""
        return self._filename

    def _read_source(self) -> str:
        """
        Locate and read the packaged source file using UTF-8 encoding.

        Raises:
            FileNotFoundError: If the source file cannot be found in the package.
            OSError: If an error occurs while reading the file.
        """
        try:
            from importlib import resources
            traversable = resources.files("pybox_dl.programs").joinpath(self._filename)
            try:
                is_file = traversable.is_file()
            except AttributeError:
                is_file = True

            if is_file:
                return traversable.read_text(encoding="utf-8")
        except Exception:
            pass

        fallback_path = Path(__file__).resolve().parent / "programs" / self._filename
        if fallback_path.is_file():
            return fallback_path.read_text(encoding="utf-8")

        raise FileNotFoundError(
            f"Packaged source file for program '{self._identifier}' "
            f"('{self._filename}') was not found in pybox_dl.programs."
        )

    @property
    def code(self) -> str:
        """The complete original source code of the program as a string."""
        return self._read_source()

    def __str__(self) -> str:
        """Return the complete source code when the program is converted to str or printed."""
        return self.code

    def __repr__(self) -> str:
        """Return a helpful developer representation."""
        return f"Program({self._identifier!r})"

    def save(
        self,
        destination: Union[str, Path, None] = None,
        *,
        overwrite: bool = False,
    ) -> Path:
        """
        Export the program's source code into a standalone Python file.

        Args:
            destination: Optional file path or directory. Defaults to '<identifier>.py'
                         in the current working directory.
            overwrite: If False (default), raises FileExistsError if the destination exists.
                       If True, safely replaces the destination file.

        Returns:
            The resolved Path to the saved Python file.

        Raises:
            FileExistsError: If destination exists and overwrite is False.
            IsADirectoryError: If destination is an existing directory and no filename is given.
            OSError: If an error occurs creating directories or writing the file.
        """
        source_code = self.code

        if destination is None:
            dest_path = Path.cwd() / self._filename
        else:
            dest_path = Path(destination)
            dest_str = str(destination)
            if dest_str.endswith(("/", "\\")) or (dest_path.is_dir() and not dest_path.suffix):
                dest_path = dest_path / self._filename

        # Refuse to overwrite directory
        if dest_path.is_dir():
            raise IsADirectoryError(
                f"Destination path '{dest_path}' is an existing directory. "
                "Cannot overwrite a directory with a file."
            )

        # Strict overwrite check
        if dest_path.exists() and not overwrite:
            raise FileExistsError(
                f"Destination file '{dest_path}' already exists. "
                "Pass 'overwrite=True' to allow overwriting."
            )

        parent_dir = dest_path.parent
        try:
            parent_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise OSError(f"Failed to create directory '{parent_dir}': {e}") from e

        # Safe atomic write via temporary file in the target directory
        temp_file_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=parent_dir,
                delete=False,
                prefix=f".tmp_{dest_path.stem}_",
                suffix=".tmp",
            ) as tmp:
                temp_file_path = Path(tmp.name)
                tmp.write(source_code)
                tmp.flush()
                os.fsync(tmp.fileno())

            # Atomic replace
            os.replace(temp_file_path, dest_path)
            temp_file_path = None
        except Exception as e:
            if temp_file_path is not None and temp_file_path.exists():
                try:
                    temp_file_path.unlink()
                except OSError:
                    pass
            raise OSError(f"Failed to export source code to '{dest_path}': {e}") from e

        return dest_path.resolve()
