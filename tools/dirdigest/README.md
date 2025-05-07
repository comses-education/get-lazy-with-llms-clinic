# dirdigest 🦾

Generate Markdown or JSON digests of directory structures and file contents, designed primarily for providing context to Large Language Models (LLMs).

`dirdigest` recursively scans a directory, intelligently filters files based on `.gitignore`-style patterns and size limits, reads the content of relevant text files, and generates a consolidated output. **By default, the generated digest is copied to the system clipboard.**

[![PyPI version](https://badge.fury.io/py/dirdigest.svg)](https://badge.fury.io/py/dirdigest) <!-- TODO: Add link after publishing -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
<!-- Add build status, coverage badges etc. -->

## Features

*   **Recursive Traversal:** Scans entire directory trees.
*   **Smart Filtering:**
    *   Uses a comprehensive set of default `.gitignore`-style exclusions (VCS, common artifacts, binaries, etc.).
    *   Supports custom `--include` and `--exclude` glob patterns.
    *   Filters files based on maximum size (`--max-size`).
*   **Content Extraction:** Reads UTF-8 text files, with graceful handling of encoding errors and binary files (placeholders).
*   **Flexible Output:**
    *   **Markdown:** Structured format with clear delimiters and a file tree overview for each directory.
    *   **JSON:** Nested structure representing the directory hierarchy and file contents.
*   **Output Destinations:** Copies to the system clipboard **by default**. Optionally writes to a file (`-o <PATH>`). Use `--no-clipboard` to disable clipboard copy (output goes to file if `-o` is used, otherwise stdout).
*   **Configuration:** Customize defaults via a `.diringest` file (TOML format).
*   **Usability:** Informative logging (`--verbose`), clear help messages, sensible defaults.
*   **Cross-Platform:** Designed to work on Linux, macOS, and Windows.

## Installation

You need Python 3.8+ and `uv` (or `pip`).

```bash
# Using uv (recommended)
uv venv # create virtual environment (optional but good practice)
# Activate environment (e.g., source .venv/bin/activate)
uv pip install dirdigest # install from PyPI (once published)
# Or install from local source:
uv pip install .
```

```bash
# Using pip
python -m venv .venv
# Activate environment (e.g., source .venv/bin/activate or .venv\Scripts\activate on Windows)
pip install dirdigest # install from PyPI (once published)
# Or install from local source:
pip install .
```

## Usage

```bash
dirdigest [OPTIONS] <DIRECTORY>
```

**Arguments:**

*   `DIRECTORY`: The root directory to scan (defaults to the current directory `.`).

**Common Options:**

*   `-o, --output <PATH>`: Write digest to a file. **Note:** By default, the digest is *also* copied to the clipboard unless `--no-clipboard` is used.
*   `-f, --format [markdown|json]`: Set the output format (default: `markdown`).
*   `--include <PATTERN>`: Only include files/dirs matching the glob pattern(s). Can be used multiple times.
*   `--exclude <PATTERN>`: Exclude files/dirs matching the glob pattern(s). Can be used multiple times. Takes precedence over `--include`.
*   `--max-size <KB>`: Maximum file size (in KB) for including content (default: 300).
*   `--no-default-ignore`: Disable the built-in exclusion rules (like `.git`, `node_modules`).
*   `--clipboard / --no-clipboard`: Copy output to clipboard (this is the **default** behavior) / Disable clipboard copy. If disabled and `-o` is not used, output goes to stdout.
*   `-v, --verbose`: Enable detailed debug logging.
*   `-V, --version`: Show version information.
*   `-h, --help`: Show the full help message.

**Examples:**

1.  **Scan current directory, copy Markdown to clipboard (default behavior):**
    ```bash
    dirdigest .
    ```

2.  **Scan `my_project/`, output JSON to `digest.json`, and copy to clipboard (default):**
    ```bash
    dirdigest my_project/ -f json -o digest.json
    ```

3.  **Scan `my_project/`, output JSON to `digest.json` ONLY (no clipboard):**
    ```bash
    dirdigest my_project/ -f json -o digest.json --no-clipboard
    ```

4.  **Scan `src/`, include only Python files, exclude `tests/`, output to stdout ONLY (no clipboard):**
    ```bash
    dirdigest src/ --include '*.py' --exclude 'tests/' --no-clipboard
    ```

5.  **Scan current directory, increase max file size, disable default ignores, write to `large_digest.md`, and copy to clipboard:**
    ```bash
    dirdigest . --max-size 1000 --no-default-ignore -o large_digest.md
    ```

6.  **Scan with verbose logging (output still goes to clipboard):**
    ```bash
    dirdigest . -v
    ```

## Output Formats

### Markdown (`--format markdown`)

Creates a structured Markdown document. Each folder includes a tree overview of its included children.

```markdown
## FOLDER: `.`

```text
./
├── src/
│   └── main.py
├── data.bin [skipped]
└── README.md
```

### FILE: `README.md`
```markdown
# My Project
This project does things.
```

### FILE: `data.bin`
```
[dirdigest: binary or non-UTF8 file] at data.bin
```

## FOLDER: `src`

```text
src/
└── main.py
```

### FILE: `src/main.py`
```python
print("Hello, world!")
```

```

### JSON (`--format json`)

Generates a nested JSON object representing the directory structure. Files with skipped content will have a `status` field indicating the reason.

```json
{
  "type": "folder",
  "relative_path": ".",
  "children": [
    {
      "type": "folder",
      "relative_path": "src",
      "children": [
        {
          "type": "file",
          "relative_path": "src/main.py",
          "content": "print(\"Hello, world!\")\n"
        }
      ]
    },
    {
      "type": "file",
      "relative_path": "README.md",
      "content": "# My Project\nThis project does things.\n"
    },
    {
      "type": "file",
      "relative_path": "data.bin",
      "content": "[dirdigest: content skipped - skipped_encoding]",
      "status": "skipped_encoding"
    }
  ]
}
```

## Configuration File (`.diringest`)

You can set default options by creating a `.diringest` file in the directory where you run `dirdigest` or its parent directories (it searches upwards). The file uses TOML format. Command-line arguments always override settings in this file.

See `.diringest.example` for all available options.

**Example `.diringest`:**

```toml
# Default to JSON output, increase max size
format = "json"
max_size = 500

# Add custom excludes (these are ADDED to defaults unless no_default_ignore=true)
exclude = [
  "config/",
  "*.tmp"
]

# Disable clipboard by default in this project
# Command line --clipboard would override this
clipboard = false
```

## Development

1.  **Clone:** `git clone https://github.com/yourusername/dirdigest.git && cd dirdigest`
2.  **Create Environment (uv):** `uv venv`
3.  **Activate:** `source .venv/bin/activate` (or `.venv\Scripts\activate` on Windows)
4.  **Install Dev Dependencies:** `uv pip install -e ".[dev]"` (Assuming you define a `[project.optional-dependencies.dev]` section in `pyproject.toml` for dev tools like pytest, ruff) or `uv pip install -e . pytest pytest-cov ruff`
5.  **Run Tests:** `pytest`
6.  **Run Linters/Formatters:** `ruff format . && ruff check .`

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.