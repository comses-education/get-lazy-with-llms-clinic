# `dirdigest`: Directory Digest Generator 🦾👌

## FOR HUMANS 🤝
1. add the contents of this file or the script itself to the context window 
2. ask your question. 

**Example questions:**
- What does this script do?
- How do I run this script?
- How to run this script and exclude all files with .aac extention?
- How to to exclude all directories and subdirectories that contain "_deleteme"?

## FOR LLMS 🦾

`dirdigest` is a command-line tool that recursively processes directories and files to create a structured, human-readable digest. This digest can be used for various purposes, such as:

*   Providing context to Large Language Models (LLMs).
*   Generating project overviews for documentation.
*   Creating summaries for code reviews.
*   Archiving snapshots of directory structures and file contents.

**Key Features:**

*   **Customizable Traversal:** Filter by glob patterns (include/exclude), maximum file size, and maximum directory depth.
*   **Smart Filtering:** Comes with a comprehensive set of default ignore patterns for common nuisance files and directories (e.g., `.git`, `__pycache__`, `node_modules`, binary files), which can be disabled.
*   **Multiple Output Formats:** Generate digests in Markdown (default) or JSON.
*   **Clipboard Integration:** Automatically copy the generated digest to the system clipboard (can be disabled).
*   **Configuration File:** Define default settings and profiles in a `.diringest` YAML file for consistent behavior across projects.
*   **Error Handling:** Option to ignore file read errors and continue processing.
*   **Symlink Support:** Choose whether to follow symbolic links.
*   **Logging:** Controllable verbosity for console output and option to log detailed information to a file.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [CLI Usage Guide](#cli-usage-guide)
  - [Synopsis](#synopsis)
  - [Argument](#argument)
  - [Options](#options)
- [Configuration File (`.diringest`)](#configuration-file-diringest)
  - [Format and Location](#format-and-location)
  - [Supported Settings](#supported-settings)
  - [Example Configuration](#example-configuration)
- [Use Case Examples](#use-case-examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

`dirdigest` requires Python 3.8 or higher.

### Using `pip` (Recommended)

1.  **From PyPI (once published):**
    ```bash
    pip install dirdigest
    ```

2.  **From source (for development or direct install):**
    Clone the repository:
    ```bash
    git clone https://github.com/comses-education/get-lazy-with-llms-clinic.git # Or your specific repo URL
    cd path/to/dirdigest # Navigate to the project directory containing pyproject.toml
    ```
    Install the package:
    ```bash
    pip install .
    ```
    For an editable install (changes to source code are reflected immediately):
    ```bash
    pip install -e .
    ```
    To include development dependencies (e.g., for running tests):
    ```bash
    pip install -e .[dev]
    ```

### Using `uv`

Ensure `uv` is installed. `uv` can be used as a faster alternative to `pip`.

1.  **From PyPI (once published):**
    ```bash
    uv pip install dirdigest
    ```

2.  **From source:**
    Navigate to the project directory as above.
    ```bash
    uv pip install .
    ```
    Editable install:
    ```bash
    uv pip install -e .
    ```
    With development dependencies:
    ```bash
    uv pip install -e .[dev]
    ```

## Quick Start

Navigate to the directory you want to analyze and run:

```bash
dirdigest
```

This will process the current directory, apply default ignore patterns, and print a Markdown-formatted digest to your console. The digest will also be copied to your clipboard by default.

To save the output to a file:

```bash
dirdigest my_project_folder -o project_summary.md
```

To get a JSON output:

```bash
dirdigest . -f json -o project_data.json
```

## CLI Usage Guide

### Synopsis

```
dirdigest [OPTIONS] [DIRECTORY]
```

### Argument

*   `DIRECTORY`
    *   The path to the directory to process.
    *   If omitted, it defaults to the current working directory (`.`).
    *   Type: `Path (must be an existing, readable directory)`

### Options

| Option                      | Short | Description                                                                                                                                                              | Default            |
| --------------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------ |
| `--output PATH`             | `-o`  | Path to the output file. If omitted, the digest is written to standard output (stdout).                                                                                  | `None` (stdout)    |
| `--format [json\|markdown]` | `-f`  | Output format for the digest.                                                                                                                                            | `markdown`         |
| `--include PATTERN`         | `-i`  | Glob pattern(s) for files/directories to INCLUDE. If specified, only items matching these patterns are processed. Can be used multiple times or comma-separated.        | `None`             |
| `--exclude PATTERN`         | `-x`  | Glob pattern(s) for files/directories to EXCLUDE. Takes precedence over include patterns. Can be used multiple times or comma-separated. Default ignores also apply.      | `None`             |
| `--max-size KB`             | `-s`  | Maximum size (in KB) for individual files to be included. Larger files are excluded.                                                                                     | `300`              |
| `--max-depth INT`           | `-d`  | Maximum depth of directories to traverse. Depth 0 processes only the starting directory's files. Unlimited by default.                                                   | `None` (unlimited) |
| `--no-default-ignore`       |       | Disable all default ignore patterns (e.g., `.git`, `__pycache__`, `node_modules`, common binary/media files, hidden items like `.*`).                                      | `False`            |
| `--follow-symlinks`         |       | Follow symbolic links to directories and files. By default, symlinks themselves are noted but not traversed/read.                                                        | `False`            |
| `--ignore-errors`           |       | Continue processing if an error occurs while reading a file (e.g., permission denied, decoding error). The file's content will be omitted or noted as an error.          | `False`            |
| `--clipboard / --no-clipboard`| `-c`  | Copy the generated digest to the system clipboard. Use `--no-clipboard` to disable.                                                                                      | `True` (clipboard) |
| `--verbose`                 | `-v`  | Increase verbosity. `-v` for INFO, `-vv` for DEBUG console output.                                                                                                       | `0` (WARNINGS)     |
| `--quiet`                   | `-q`  | Suppress all console output below ERROR level. Overrides `-v`.                                                                                                           | `False`            |
| `--log-file PATH`           |       | Path to a file for detailed logging. All logs (including DEBUG level) will be written here, regardless of console verbosity.                                            | `None`             |
| `--config PATH`             |       | Specify configuration file path. If omitted, tries to load `./.diringest` from the current directory.                                                                    | `None`             |
| `--version`                 |       | Show the version of `dirdigest` and exit.                                                                                                                                |                    |
| `--help`                    | `-h`  | Show this help message and exit.                                                                                                                                         |                    |

**Glob Pattern Details (`--include`, `--exclude`):**

*   Patterns are applied to relative paths from the base directory.
*   Use standard glob syntax (e.g., `*.py`, `src/**/`, `data/*.csv`).
*   To match a directory specifically, ensure the pattern ends with a `/` (e.g., `docs/`).
*   Multiple patterns can be supplied by using the option multiple times (e.g., `-i '*.py' -i '*.md'`) or by providing a comma-separated list (e.g., `-x '*.log,tmp/,build/'`).
*   Exclusion patterns take precedence over inclusion patterns.
*   Default ignore patterns are applied *in addition* to user-specified excludes unless `--no-default-ignore` is set. These include common VCS directories (`.git/`), build artifacts (`build/`, `dist/`, `__pycache__/`, `node_modules/`), hidden files/directories (`.*`), and common binary/media file extensions.

## Configuration File (`.diringest`)

`dirdigest` can be configured using a YAML file, typically named `.diringest`.

### Format and Location

*   **Default Name:** `.diringest`
*   **Default Location:** The tool looks for this file in the current working directory from where `dirdigest` is invoked.
*   **Custom Location:** You can specify a different configuration file path using the `--config PATH` CLI option.
*   **Format:** YAML.

The configuration file can be structured in two ways:

1.  **Flat Configuration:** A simple key-value mapping of settings at the root of the YAML file.
    ```yaml
    # .diringest (flat example)
    format: json
    max-size: 500
    exclude:
      - "*.log"
      - "temp/"
    ```

2.  **With a `default` Profile:** Settings are placed under a `default:` key. This is the primary way `dirdigest` currently uses profiles. If other top-level keys (potential future profiles) exist, they are ignored unless a `default` profile is explicitly defined.
    ```yaml
    # .diringest (with 'default' profile)
    default:
      format: markdown
      max-depth: 3
      no-default-ignore: true
      include: "*.py,*.md"
      exclude: "**/tests/"
    
    # other_profile: # Currently ignored by dirdigest
    #   format: json
    ```

**Precedence:** Command-line arguments, if explicitly set by the user, will always override settings from the configuration file. If a CLI option is not used, its default value from the configuration file (if present) will be applied, otherwise the tool's built-in default is used.

### Supported Settings

The following settings can be used in the `.diringest` file. Keys are hyphenated where applicable if they represent multi-word CLI options (though `dirdigest`'s config loader currently expects keys to match Python attribute names, e.g., `max_size`, `no_default_ignore`). *For consistency with CLI option names, use the Python attribute names (e.g., `max_size` not `max-size`) in your YAML.*

| YAML Key             | Type                                    | CLI Equivalent        | Description                                                                    |
| -------------------- | --------------------------------------- | --------------------- | ------------------------------------------------------------------------------ |
| `directory`          | string (path)                           | `DIRECTORY` (arg)     | Base directory to process.                                                     |
| `output`             | string (path)                           | `--output`            | Output file path.                                                              |
| `format`             | string (`json` or `markdown`)           | `--format`            | Output format.                                                                 |
| `include`            | list of strings, or comma-separated str | `--include`           | Include patterns.                                                              |
| `exclude`            | list of strings, or comma-separated str | `--exclude`           | Exclude patterns.                                                              |
| `max_size`           | integer (KB)                            | `--max-size`          | Max file size in KB.                                                           |
| `max_depth`          | integer or `null`                       | `--max-depth`         | Max traversal depth (`null` for unlimited).                                    |
| `no_default_ignore`  | boolean (`true`/`false`)                | `--no-default-ignore` | Disable default ignore patterns.                                               |
| `follow_symlinks`    | boolean (`true`/`false`)                | `--follow-symlinks`   | Follow symbolic links.                                                         |
| `ignore_errors`      | boolean (`true`/`false`)                | `--ignore-errors`     | Continue on file read errors.                                                  |
| `clipboard`          | boolean (`true`/`false`)                | `--clipboard`         | Copy to clipboard.                                                             |
| `verbose`            | integer (0, 1, or 2)                    | `--verbose`           | Verbosity level (0: WARNING, 1: INFO, 2: DEBUG).                               |
| `quiet`              | boolean (`true`/`false`)                | `--quiet`             | Suppress console output below ERROR.                                           |
| `log_file`           | string (path)                           | `--log-file`          | Path for detailed log file.                                                    |

### Example Configuration

```yaml
# .diringest
# This is a sample configuration file for dirdigest.

default:
  # Output settings
  format: "markdown"        # 'json' or 'markdown'
  # output: "my_digest.md" # Optional: specify default output file

  # Traversal and filtering settings
  # directory: "."          # Optional: specify default directory (usually CWD is fine)
  max_size: 250             # Max file size in KB
  max_depth: 5              # Max directory depth to traverse, null for unlimited
  follow_symlinks: false    # Set to true to follow symbolic links
  no_default_ignore: false  # Set to true to disable all default ignore patterns
                            # (e.g., .git, __pycache__, common binary/media files)

  # Include patterns: process only these if specified.
  # Exclusions are applied first.
  include:
    - "*.py"
    - "*.md"
    - "src/"
    # - "docs/**/*.rst" # Example of deeper pattern

  # Exclude patterns: always skip these. Takes precedence over includes.
  # Default ignores also apply unless no_default_ignore is true.
  exclude:
    - "*.log"
    - "tests/"
    - "**/__pycache__/" # More specific than default if needed
    - "node_modules/"
    - ".venv/"
    - "dist/"
    - "build/"

  # Content processing
  ignore_errors: false      # Set to true to include files with read errors (content will be null)

  # UI/UX settings
  clipboard: true           # false to disable copying to clipboard
  verbose: 0                # Console verbosity: 0 (Warning), 1 (Info), 2 (Debug)
  quiet: false              # Suppress console output below ERROR, overrides verbose
  # log_file: "dirdigest.log" # Optional: path for detailed file logging (always DEBUG level)
```

## Use Case Examples
0. **Generate a digest of dirdigest folder, and save it:**
    ```bash
    dirdigest . -o digest.md -x tests/fixtures/ -x *.egg-info/ -x digest.md -x uv.lock -c
    ```

1.  **Generate a Markdown summary of your current project, excluding tests and virtual environments, and save it:**
    ```bash
    dirdigest . -o project_summary.md -x "tests/,*.venv/,env/"
    ```

2.  **Create a JSON digest of a specific directory (`src/`) including only Python files, with a max depth of 2, and disable default ignores to include hidden Python files (e.g. `._internal.py`):**
    ```bash
    dirdigest src/ -f json --include "*.py" --max-depth 2 --no-default-ignore -o src_python_digest.json
    ```

3.  **Digest a large repository, focusing on source code, limiting file size to 100KB, and ignoring binary/media files explicitly, output to clipboard:**
    ```bash
    dirdigest /path/to/large_repo \
        --include "*.c,*.h,*.py,*.js,Makefile,README*" \
        --exclude "*.so,*.o,*.a,*.jpg,*.png,*.mp4,docs/" \
        --max-size 100 \
        --no-clipboard # (If you want to manually copy from stdout)
    ```
    (By default, clipboard is on, so `--no-clipboard` is only if you *don't* want it on the clipboard.)

4.  **Use a project-specific `.diringest` file for common settings:**
    Create a `.diringest` file in your project root:
    ```yaml
    # my_project/.diringest
    default:
      exclude:
        - "dist/"
        - "build/"
        - "node_modules/"
        - ".DS_Store"
        - "*.pyc"
      include:
        - "src/**/*.js"
        - "public/"
      max_size: 500
      format: markdown
    ```
    Then simply run from the project root:
    ```bash
    dirdigest -o web_app_digest.md
    ```
    This will use settings from `.diringest` and save to `web_app_digest.md`.

5.  **Include a specific hidden file (e.g., `.envrc`) while keeping most default ignores active (this is tricky):**
    The most straightforward way to include a specific hidden file that would normally be ignored by `.*` or other hidden-file logic is to use `--no-default-ignore` and then explicitly include what you want, and explicitly exclude what you *don't* want from the usual defaults.
    ```bash
    dirdigest . --no-default-ignore \
        --include ".envrc,src/*.py,README.md" \
        --exclude ".git/,__pycache__/,*.log,node_modules/" \
        -o my_app_context.md
    ```
    This gives you fine-grained control when default behaviors for hidden files conflict with your needs.

6.  **Troubleshoot which files are being processed or ignored with verbose logging:**
    ```bash
    dirdigest . -vv --log-file processing_details.log
    ```
    Check `processing_details.log` for detailed DEBUG messages about each file and directory encountered.

## Contributing

Contributions are welcome! Please refer to the `CONTRIBUTING.md` file (if available) or open an issue/pull request on the project's repository.

When contributing, consider:
*   Adding tests for new features or bug fixes.
*   Ensuring code style consistency (e.g., using `ruff` and `black`).
*   Updating documentation as needed.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.