# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-10-29

### Added
- Initial release of `pybox-dl`.
- Core `Program` class supporting UTF-8 source inspection and safe file export.
- 8 top-level program access attributes (`pybox_dl.one` through `pybox_dl.eight`).
- String representation (`__str__`) and inspection property (`.code`) for direct access to Deep Learning program source.
- Export mechanism (`.save()`) with custom destination support, automatic directory creation, and strict overwrite protection (`overwrite=True`).
- Safe atomic export using temporary file replacement to prevent corrupted or partial file writes.
- Non-executing architecture: importing `pybox_dl` and inspecting source code never executes bundled programs or triggers heavy framework loading (e.g. TensorFlow/Keras).
- Complete automated test suite covering access, printing, export safety, error handling, and package bundling.
- Packaging configuration via `pyproject.toml` adhering to PEP 517/518/621 standards.
