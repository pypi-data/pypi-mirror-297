# Licenser

A Python tool to add or update license headers in your project files.

## Description

Licenser is a command-line utility designed to automate the process of adding or updating license headers in your project's source code files. It supports multiple programming languages and license types, ensuring that your code complies with the licensing requirements of your choice.

## Features

- **Supports Multiple Licenses**:
  - MIT License
  - Apache License 2.0
  - GNU General Public License v3.0
  - BSD 2-Clause Simplified License
- **Multi-language Support**:
  - Python, Shell Script, C, C++, Java, JavaScript, C#, Go, Ruby, PHP, HTML, XML, CSS, and more.
- **Automatic Detection and Replacement**:
  - Detects existing license headers and replaces them.
  - Only updates the license header at the top of the file without affecting other comments.
- **Customizable Placeholders**:
  - Replaces placeholders like `|year|`, `|author|`, `|projectname|`, and `|projectnamecaps|` with actual values.

## Installation

### Prerequisites

- Python 3.6 or higher
- `pip` package manager

### Using `setup.py`

You can install Licenser by cloning the repository and running the `setup.py` script:

```bash
# Clone the repository
git clone https://github.com/yummydirtx/licenser-h.git
cd licenser-h

# Install the package
python setup.py install
```

### Using `pip`

Licenser is available on PyPI, and you can install it directly:

```bash
pip install licenser-h
```

## Usage

### Command-Line Interface

Run the Licenser tool:

```bash
licenser-h
```