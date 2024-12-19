[![CodeQL Advanced](https://github.com/ngmisl/llmstxt/actions/workflows/codeql.yml/badge.svg)](https://github.com/ngmisl/llmstxt/actions/workflows/codeql.yml)
[![Update llms.txt](https://github.com/ngmisl/llmstxt/actions/workflows/update-llms.yml/badge.svg)](https://github.com/ngmisl/llmstxt/actions/workflows/update-llms.yml)

# llmstxt

A Python tool for compressing and organizing code files into a single, LLM-friendly text file. This tool is designed to help prepare codebases for analysis by Large Language Models by removing unnecessary content while preserving important semantic information.

## Features

### Smart Code Compression

- Preserves docstrings and important comments
- Removes redundant whitespace and formatting
- Maintains code structure and readability
- Handles multiple programming languages

### Language Support

- Python (with AST-based compression)
- JavaScript
- Java
- C/C++
- Shell scripts
- HTML/CSS
- Configuration files (JSON, YAML, TOML, INI)
- Markdown

### LLM-Friendly Output

- XML-style semantic markers
- File metadata and type information
- Organized imports section
- Clear file boundaries
- Consistent formatting

### Automation

- GitHub Actions integration
- Automatic updates on code changes
- CI/CD friendly

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management, but can also be installed directly with pip.

```bash
# Using pip
pip install git+https://github.com/ngmisl/llmstxt.git

# Using uv (recommended for development)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv pip install .

# For development
uv pip install -e ".[dev]"
```

## Usage

### Local Usage

```bash
# Generate llms.txt from current directory
python -m llmstxt

# Or import and use in your code
from llmstxt import generate_llms_txt
generate_llms_txt()
```

The script will:

1. Scan the current directory recursively
2. Process files according to .gitignore rules
3. Generate `llms.txt` with compressed content

### GitHub Actions Integration

There are two ways to use this tool with GitHub Actions:

1. **For Your Own Repository**

Create `.github/workflows/update-llms.yml` with:

```yaml
name: Update llms.txt

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]
  workflow_dispatch: # Allow manual triggering

permissions:
  contents: write

jobs:
  update-llms:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.12"
          cache: "pip"

      - name: Install llmstxt tool
        run: |
          python -m venv .venv
          . .venv/bin/activate
          python -m pip install --upgrade pip
          pip install git+https://github.com/ngmisl/llmstxt.git

      - name: Generate llms.txt
        run: |
          . .venv/bin/activate
          rm -f llms.txt
          python -c "from llmstxt import generate_llms_txt; generate_llms_txt()"

      - name: Configure Git
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"

      - name: Commit and push changes
        run: |
          git add llms.txt
          if git diff --staged --quiet; then
            echo "No changes to commit"
          else
            git commit -m "chore: update llms.txt"
            git push
          fi
```

The workflow will:

- Run on push to main/master
- Run on pull requests
- Can be triggered manually
- Generate and commit `llms.txt` automatically

2. **For Remote Repositories**
   You can trigger the action for any repository using the GitHub API:

```bash
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/ngmisl/llmstxt/dispatches \
  -d '{"event_type": "update-llms", "client_payload": {"repository": "https://github.com/user/repo.git"}}'
```

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
- [uv](https://github.com/astral-sh/uv) for dependency management (recommended)

```bash
# Clone the repository
git clone https://github.com/ngmisl/llmstxt.git
cd llmstxt

# Install development dependencies
uv pip install -e ".[dev]"

# Run type checking
mypy llmstxt

# Run linting and formatting
ruff check llmstxt
ruff format llmstxt
```

## License

MIT License - See LICENSE file for details
