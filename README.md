[![CodeQL Advanced](https://github.com/ngmisl/llmstxt/actions/workflows/codeql.yml/badge.svg)](https://github.com/ngmisl/llmstxt/actions/workflows/codeql.yml)
[![Update llms.txt](https://github.com/ngmisl/llmstxt/actions/workflows/update-llms.yml/badge.svg)](https://github.com/ngmisl/llmstxt/actions/workflows/update-llms.yml)

# llmstxt

A Python tool to compress code files into a single, LLM-friendly text file.

## Features

- Preserves important comments and docstrings
- Removes unnecessary content
- Structured, LLM-friendly output
- GitHub Actions integration for automatic updates

## Installation

```bash
pip install git+https://github.com/ngmisl/llmstxt.git
```

## Usage

### Command Line

```bash
# Generate llms.txt in current directory
python -m llmstxt

# Or import and use in your code
from llmstxt import generate_llms_txt
generate_llms_txt()
```

### GitHub Actions Integration

To automatically update `llms.txt` in your repository:

1. Create `.github/workflows/update-llms.yml` with:

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

## Development

```bash
# Clone the repository
git clone https://github.com/ngmisl/llmstxt.git
cd llmstxt

# Install development dependencies
pip install -e ".[dev]"

# Run type checking
mypy llmstxt

# Run linting
ruff check llmstxt
```

## License

MIT
