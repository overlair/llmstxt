# llmstxt

A Python tool for compressing and organizing code files into a single, LLM-friendly text file. This tool is designed to help prepare codebases for analysis by Large Language Models by removing unnecessary content while preserving important semantic information.

## Features

- **Smart Code Compression**
  - Preserves docstrings and important comments
  - Removes redundant whitespace and formatting
  - Maintains code structure and readability
  - Handles multiple programming languages

- **Language Support**
  - Python (with AST-based compression)
  - JavaScript
  - Java
  - C/C++
  - Shell scripts
  - HTML/CSS
  - Configuration files (JSON, YAML, TOML, INI)
  - Markdown

- **LLM-Friendly Output**
  - XML-style semantic markers
  - File metadata and type information
  - Organized imports section
  - Clear file boundaries
  - Consistent formatting

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install the package and its dependencies
uv pip install .

# For development
uv pip install -e ".[dev]"
```

## Usage

```python
# Basic usage
python llms.py

# The script will:
# 1. Scan the current directory
# 2. Process files according to .gitignore rules
# 3. Generate llms.txt with compressed content
```

## Output Format

The generated `llms.txt` file follows this structure:

``` python
# Project metadata
<file>path/to/file.py</file>
<metadata>
path: path/to/file.py
type: py
size: 1234 bytes
</metadata>

<imports>
import ast
from typing import Optional
</imports>

<code lang='python'>
def example():
    """Docstring preserved."""
    return True
</code>
```

## Configuration

- Maximum file size: 100KB (configurable)
- Supported file extensions: .py, .js, .java, .c, .cpp, .h, .hpp, .sh, .txt, .md, .json, .xml, .yaml, .yml, .toml, .ini
- Respects .gitignore rules

## Development

Requirements:

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) for dependency management

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run type checking
mypy llms.py

# Run linting and formatting
ruff check .
ruff format .
```

## License

MIT License - See LICENSE file for details
