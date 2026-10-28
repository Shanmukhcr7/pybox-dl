# PyBox-DL (`pybox-dl`)

A production-ready Python library bundling 8 standalone Deep Learning programs into one installable package. Access each program via intuitive top-level attributes, inspect its original source code directly, and safely export it into standalone `.py` scripts.

[![PyPI Version](https://img.shields.io/badge/pypi-v0.1.0-blue.svg)](https://pypi.org/project/pybox-dl/)
[![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://pypi.org/project/pybox-dl/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Table of Contents

- [Overview](#overview)
- [Key Distinction: Inspection vs. Execution](#key-distinction-inspection-vs-execution)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Program Identifiers & Bundled Programs](#program-identifiers--bundled-programs)
- [Features and Usage](#features-and-usage)
  - [1. Viewing Source Code](#1-viewing-source-code)
  - [2. Accessing Raw Source String](#2-accessing-raw-source-string)
  - [3. Exporting to Standalone Files](#3-exporting-to-standalone-files)
  - [4. Custom Export Destinations](#4-custom-export-destinations)
  - [5. Overwrite Protection](#5-overwrite-protection)
  - [6. Developer Representation](#6-developer-representation)
- [Individual Program Dependencies](#individual-program-dependencies)
- [Safety and Security](#safety-and-security)
- [Compatibility](#compatibility)
- [Development and Testing](#development-and-testing)
- [Publishing to PyPI](#publishing-to-pypi)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

`pybox-dl` bundles 8 standalone Deep Learning programs into a unified package. Instead of hunting through past lab directories or copying and pasting snippets, developers can:
- Import `pybox_dl` and inspect any bundled program's complete source code in Python interactive shells, logging, or scripts.
- Export bundled programs into standalone `.py` files on demand with atomic write safety and directory creation.
- Keep source code intact: all comments, imports, neural network architectures, and training logic are preserved identically.

---

## Key Distinction: Inspection vs. Execution

> [!IMPORTANT]
> **`pybox-dl` does NOT execute bundled programs or import heavy machine learning frameworks (such as TensorFlow) when you import the library, inspect source code, or export scripts.**

`pybox-dl` acts as a curated code distribution and extraction engine. When you access `pybox_dl.one` or invoke `pybox_dl.one.save()`, `pybox-dl` reads the packaged source assets as UTF-8 text.

To **run** an exported model script after saving it, execute it in Python directly using your terminal:

```bash
python one.py
```

Ensure any third-party frameworks required by that specific model (e.g. `tensorflow`, `numpy`, `scikit-learn`, `matplotlib`) are installed in your Python environment before running it.

---

## Installation

### From PyPI

```bash
python -m pip install pybox-dl
```

### From Local Source (Editable Mode)

```bash
git clone https://github.com/Shanmukhcr7/pybox-dl.git
cd pybox-dl
python -m pip install -e ".[dev]"
```

---

## Quick Start

```python
import pybox_dl

# 1. Print the complete source code of a program
print(pybox_dl.one)

# 2. Get the raw source code string
code = pybox_dl.two.code
print(f"Total lines: {len(code.splitlines())}")

# 3. Export to a standalone Python script
saved_path = pybox_dl.one.save()
print(f"Exported to: {saved_path}")
```

---

## Program Identifiers & Bundled Programs

The package exposes 8 curated Deep Learning programs as attributes on the top-level `pybox_dl` module:

| Attribute | Default Export | Description | Dependencies |
| :--- | :--- | :--- | :--- |
| `pybox_dl.one` | `one.py` | **Simple Linear Regression**: Implements basic linear regression with dataset generation and plot visualization. | `numpy`, `scikit-learn`, `matplotlib` |
| `pybox_dl.two` | `two.py` | **TensorFlow Fundamentals**: Demonstrates tensor constants, matrix operations, and tensor manipulation. | `numpy`, `tensorflow` |
| `pybox_dl.three` | `three.py` | **Artificial Neural Network (ANN)**: Constructs, trains, and evaluates a dense multi-layer perceptron. | `tensorflow` |
| `pybox_dl.four` | `four.py` | **Small Image Classification using CNN**: Builds a Convolutional Neural Network for small image recognition. | `tensorflow` |
| `pybox_dl.five` | `five.py` | **Sentiment Analysis using LSTM**: Implements Long Short-Term Memory recurrent layers for sequence classification. | `tensorflow` |
| `pybox_dl.six` | `six.py` | **Language Modeling using RNN**: Trains a Recurrent Neural Network for character/word-level language prediction. | `numpy`, `tensorflow` |
| `pybox_dl.seven` | `seven.py` | **Sentiment Analysis using GRU**: Implements Gated Recurrent Units for efficient recurrent sentiment analysis. | `tensorflow` |
| `pybox_dl.eight` | `eight.py` | **Transfer Learning for Image Classification**: Leverages pre-trained deep architectures for image recognition tasks. | `tensorflow` |

You can iterate over all programs programmatically:

```python
import pybox_dl

for name, prog in pybox_dl.PROGRAMS.items():
    print(f"Loaded {prog.identifier}: {prog.filename}")
```

---

## Features and Usage

### 1. Viewing Source Code

Converting any program object to `str` (or passing it to `print()`) renders its complete source code:

```python
import pybox_dl

print(pybox_dl.one)
```

### 2. Accessing Raw Source String

Access the `.code` property on any program object to obtain the unmodified source code as a Python `str`:

```python
import pybox_dl

source = pybox_dl.one.code
assert isinstance(source, str)
print(f"Total lines: {len(source.splitlines())}")
```

### 3. Exporting to Standalone Files

Call `.save()` without arguments to export the program to the current working directory under its default filename (e.g., `one.py`):

```python
import pybox_dl

path = pybox_dl.one.save()
print(path)  # /path/to/cwd/one.py
```

### 4. Custom Export Destinations

Specify a custom file name or path. If intermediate parent directories do not exist, `pybox-dl` creates them automatically:

```python
import pybox_dl

# Export to a custom filename in the current directory
pybox_dl.one.save("linear_regression.py")

# Export to a nested subdirectory (directories created automatically)
pybox_dl.four.save("models/cnn/classify.py")

# Export into an existing directory (uses default filename 'three.py')
pybox_dl.three.save("exports/")
```

### 5. Overwrite Protection

To protect existing scripts from accidental loss, `pybox-dl` **refuses to overwrite existing files by default**:

```python
import pybox_dl

# First export succeeds
pybox_dl.one.save("script.py")

# Second export raises FileExistsError
try:
    pybox_dl.one.save("script.py")
except FileExistsError as e:
    print("Caught expected protection error:", e)

# Explicitly authorize overwriting
pybox_dl.one.save("script.py", overwrite=True)
```

Export writes use atomic temporary file replacement (`os.replace`) to ensure a partially written file is never left on disk in the event of an interruption.

### 6. Developer Representation

In interactive environments, `repr()` provides clear identification:

```python
import pybox_dl

print(repr(pybox_dl.one))
# Output: Program('one')
```

---

## Individual Program Dependencies

`pybox-dl` itself has **zero runtime third-party dependencies**. It relies strictly on Python standard library modules (`pathlib`, `tempfile`, `os`, `importlib.resources`).

Exporting a program writes its standalone source code to disk. Before running the exported scripts, install any required deep learning libraries:

```bash
# To run exported Deep Learning programs:
pip install tensorflow numpy scikit-learn matplotlib
```

| Program | External Dependencies |
| :--- | :--- |
| `one.py` | `numpy`, `scikit-learn`, `matplotlib` |
| `two.py` | `numpy`, `tensorflow` |
| `three.py` | `tensorflow` |
| `four.py` | `tensorflow` |
| `five.py` | `tensorflow` |
| `six.py` | `numpy`, `tensorflow` |
| `seven.py` | `tensorflow` |
| `eight.py` | `tensorflow` |

---

## Safety and Security

- **No Execution on Import**: Bundled code is never imported, evaluated, or executed by `pybox-dl`.
- **Atomic Writes**: Export files are written to a temporary file before being atomically moved into destination path.
- **Directory Traversal & Overwrite Guards**: Prevents accidental directory replacement and unintended data destruction.
- **Zero Secrets**: Bundled programs contain no API keys, passwords, or personal credentials.

---

## Compatibility

- **Python**: `>= 3.8` (tested across Python 3.8, 3.9, 3.10, 3.11, 3.12, and 3.13)
- **Platforms**: Windows, macOS, and Linux
- **Packaging Standard**: PEP 517 / PEP 518 / PEP 621 compliant build

---

## Development and Testing

### Setup Environment

```powershell
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

```bash
# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### Run Tests

```bash
pytest -v
```

### Build Distribution Artifacts

```bash
python -m build
python -m twine check dist/*
```

---

## Publishing to PyPI

### Option A: PyPI Trusted Publishing (Recommended)

1. Connect your GitHub repository to PyPI at [PyPI Manage Account > Publishing](https://pypi.org/manage/account/publishing/).
2. Push a release tag or trigger the included `.github/workflows/publish.yml` workflow.
3. GitHub Actions authenticates via short-lived OIDC tokens without requiring static API keys.

### Option B: Manual Publishing via Twine

```bash
python -m twine upload --repository testpypi dist/*  # Test on TestPyPI first
python -m twine upload dist/*                        # Publish to production PyPI
```

---

## Contributing

1. Fork the repository (`https://github.com/Shanmukhcr7/pybox-dl`).
2. Create a feature branch (`git checkout -b feature/my-feature`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Run the test suite (`pytest -v`).
5. Open a Pull Request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
