[![CodeQL Advanced](https://github.com/ngmisl/llmstxt/actions/workflows/codeql.yml/badge.svg)](https://github.com/ngmisl/llmstxt/actions/workflows/codeql.yml)
[![Update llms.txt](https://github.com/ngmisl/llmstxt/actions/workflows/update-llms.yml/badge.svg)](https://github.com/ngmisl/llmstxt/actions/workflows/update-llms.yml)

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

### Local Usage

```bash
# Generate llms.txt from current directory
python llms.py
```

The script will:
1. Scan the current directory recursively
2. Process files according to .gitignore rules
3. Generate `llms.txt` with compressed content

### GitHub Actions Integration

This tool can automatically generate and update `llms.txt` in your repository using GitHub Actions. To set it up:

1. Copy the workflow file:
   ```bash
   mkdir -p .github/workflows
   curl -o .github/workflows/update-llms.yml https://raw.githubusercontent.com/ngmisl/llmstxt/main/.github/workflows/update-llms.yml
   ```

2. Commit and push the workflow file:
   ```bash
   git add .github/workflows/update-llms.yml
   git commit -m "chore: add llmstxt workflow"
   git push
   ```

The workflow will:
- Run automatically on pushes to main/master
- Generate/update llms.txt
- Commit and push changes if needed
- Can be manually triggered from the Actions tab

## Output Format

The generated `llms.txt` file follows this structure:

```python
# Project: llmstxt

## Project Structure
This file contains the compressed and processed contents of the project.

### File Types
- .py
- .js
- .java
...

<file>src/main.py</file>
<metadata>
path: src/main.py
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

<file>src/utils.js</file>
<metadata>
path: src/utils.js
type: js
size: 567 bytes
</metadata>

<code lang='javascript'>
function helper() {
  return true;
}
</code>
```

## Configuration

The tool can be configured through function parameters:

```python
generate_llms_txt(
    output_file="llms.txt",      # Output filename
    max_file_size=100 * 1024,    # Max file size (100KB)
    allowed_extensions=(         # Supported file types
        ".py", ".js", ".java",
        ".c", ".cpp", ".h", ".hpp",
        ".sh", ".txt", ".md",
        ".json", ".xml", ".yaml",
        ".yml", ".toml", ".ini"
    )
)
```

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
