# Local Codebase Digest Generator

# FOR HUMANS 🤝
1. add the contents of this file or the script itself to the context window 
2. ask your question. 

**Example questions:**
- What does this script do?
- How do I run this script?
- How to run this script and exclude all files with .aac extention?
- How to to exclude all directories and subdirectories that contain "_deleteme"?

# FOR LLMS 🦾
This Python script crawls a specified local directory, reads the content of selected text files, and generates a structured JSON output containing the directory hierarchy and the content of included files. This "digest" is primarily intended for use with Large Language Models (LLMs) to provide them with context about a codebase.

## Features

*   Recursively scans a directory.
*   Filters files and directories based on various criteria:
    *   Default ignore patterns (similar to `.gitignore`, can be disabled).
    *   User-defined include/exclude patterns (`fnmatch` syntax).
    *   Maximum file size limit.
    *   Likely binary file detection (can be disabled).
    *   Hidden files and directories (can be included).
*   Handles text file encoding with configurable error strategies.
*   Outputs a structured JSON representing the directory tree and file contents.
*   Provides informative logging to stderr about included/excluded items and applied rules.

## Requirements

*   Python 3.x

## Usage

```bash
./dir-digest.py [OPTIONS] <directory>
```

Or if the script is not executable:

```bash
python dir-digest.py [OPTIONS] <directory>
```

**Basic Example:**

```bash
# Process the current directory and print JSON to stdout
python dir-digest.py .

# Process a specific project directory and save to a file
python dir-digest.py /path/to/my/project --output project_digest.json
```

## Command-Line Options

*   **`directory`** (Positional Argument)
    *   **Required.** The path to the local directory you want to process.
    *   Example: `.` for the current directory, `../my_project` for a sibling directory.

*   **`--output <path>`**
    *   **Optional.** Path to a file where the JSON output digest should be saved.
    *   If not provided, the JSON output is printed to standard output (stdout).
    *   Example: `--output codebase.json`

*   **`--include <pattern_list>`**
    *   **Optional.** A comma-separated list of `fnmatch` patterns to include. If used, only files matching these patterns will be processed.
    *   Patterns apply to relative paths from the root `directory`. Use forward slashes (`/`) as separators, even on Windows.
    *   Patterns ending with `/` specifically match directories.
    *   Cannot be used together with `--exclude`.
    *   Example: `--include "*.py,docs/,*.md,src/utils/*"`

*   **`--exclude <pattern_list>`**
    *   **Optional.** A comma-separated list of `fnmatch` patterns to exclude. Files matching these patterns will be skipped.
    *   Patterns work the same way as `--include` patterns.
    *   Cannot be used together with `--include`.
    *   Example: `--exclude "*.log,build/,test_*"`

*   **`--max-size <kb>`**
    *   **Optional.** Maximum file size in Kilobytes (KB) to include. Files larger than this will be skipped.
    *   Default: `100` (100 KB).
    *   Use `0` or `-1` for no size limit.
    *   Example: `--max-size 500` (include files up to 500KB)
    *   Example: `--max-size -1` (include files of any size)

*   **`--no-ignore-binary`**
    *   **Optional.** Flag to *include* files detected as binary.
    *   By default (`--ignore-binary` is implicitly `True`), the script attempts to detect binary files (by checking for null bytes in the first 1KB) and skips them. Use this flag if you need to include files that might be misidentified or if you intentionally want binary content representation (decoded with errors replaced). Use with caution, as it can significantly increase output size and include non-human-readable content.
    *   Example: `--no-ignore-binary`

*   **`--no-default-ignore`**
    *   **Optional.** Flag to *disable* the default exclusion patterns.
    *   By default, the script ignores common VCS directories (`.git/`), build artifacts (`build/`, `dist/`), hidden files/directories (`.*`, `.*/`), specific config folders (`.vscode/`), temporary files (`*.pyc`, `*.swp`), etc.
    *   Use this flag if you need to include files or directories that are normally ignored by default (e.g., process files inside `.git` or hidden configuration files).
    *   Example: `--no-default-ignore`

*   **`--encoding <encoding_name>`**
    *   **Optional.** Specify the character encoding to use when reading text files.
    *   Default: `utf-8`.
    *   If you encounter `UnicodeDecodeError`, you might need to specify a different encoding (e.g., `latin-1`, `cp1252`).
    *   Example: `--encoding latin-1`

*   **`--errors <handler>`**
    *   **Optional.** How to handle encoding errors when reading files.
    *   Default: `replace` (replace problematic characters with a placeholder).
    *   Choices: `strict` (raise an error and skip the file), `ignore` (discard problematic characters), `replace`, `surrogateescape`, `xmlcharrefreplace`, `backslashreplace`.
    *   Example: `--errors ignore`

## Pattern Matching Details (`fnmatch`)

The script uses Python's `fnmatch` module for pattern matching, which works similarly to shell wildcard patterns or `.gitignore` rules.

*   `*`: Matches everything.
*   `?`: Matches any single character.
*   `[seq]`: Matches any character in `seq`.
*   `[!seq]`: Matches any character not in `seq`.

**Important:**

*   Paths are matched relative to the starting `directory`.
*   Use forward slashes (`/`) as path separators in patterns.
*   **Directory Matching:** Patterns ending with a forward slash (`/`) are specifically treated as directory patterns. A path matches such a pattern if it is exactly the pattern (without the slash) or if it starts with the pattern (e.g., `docs/` matches the directory `docs` and anything inside it like `docs/file.txt` or `docs/subdir/`).
*   File extension matching like `*.log` works as expected.

**Default Ignore Patterns (used unless `--no-default-ignore` is specified):**

```
.*
.*/
.git/
.svn/
.hg/
.vscode/
.idea/
__pycache__/
node_modules/
build/
dist/
target/
*.pyc
*.log
*.swp
*.swo
*~
.DS_Store
```

## Examples

1.  **Process current directory, exclude all Markdown files, save to `digest.json`:**
    ```bash
    python dir-digest.py . --exclude "*.md" --output digest.json
    ```

2.  **Process `my_app` directory, *only include* Python files and files in the `config/` directory:**
    ```bash
    python dir-digest.py my_app --include "*.py,config/" --output digest.json
    ```

3.  **Process current directory, include *all* files (including hidden and binary), no size limit:**
    ```bash
    python dir-digest.py . --no-default-ignore --no-ignore-binary --max-size -1 --output full_digest.json
    ```

4.  **Process a project, excluding the `tests/` directory and any `.tmp` files, handling potential encoding errors:**
    ```bash
    python dir-digest.py /path/to/project --exclude "tests/,*.tmp" --errors ignore --output project_digest.json
    ```

5.  **Process a project with a larger file size limit (500KB):**
    ```bash
    python dir-digest.py /path/to/project --max-size 500 --output project_digest.json
    ```

## Crawling Rules Summary

Before processing, the script prints a summary of the effective crawling rules to standard error (stderr) based on the flags provided. This helps confirm how files will be filtered. Example:

```
===== DIRECTORY DIGEST - CRAWLING RULES =====
Target directory: ./

Mode: EXCLUDE

- Default ignore patterns: ENABLED
  Default Exclusions:
    - .*
    - .*/
    ... (rest of default patterns) ...

- User Exclude Patterns:
    - *.md

- File size limit: 100 KB

- Binary files: EXCLUDED (heuristic check)

- Hidden files/directories (.name): EXCLUDED (by default ignores)

- Encoding: utf-8 (Errors: replace)

- Output file: /path/to/digest.json (will be excluded)
============================================
```

## Output Format

The script outputs a JSON object representing the directory structure.

*   The root object is a dictionary representing the starting directory.
*   Each dictionary has:
    *   `"type"`: Either `"folder"` or `"file"`.
    *   `"relative_path"`: The path relative to the starting directory (empty string `""` for the root folder).
    *   If `type` is `"folder"`, it has a `"children"` key: a list containing dictionary representations of its files and subfolders (sorted alphabetically, with folders always listed before files). Empty folders might be excluded from the structure depending on filtering rules.
    *   If `type` is `"file"`, it has a `"content"` key: a string containing the entire content of the file (respecting encoding and error handling).

**Example Snippet:**

```json
{
  "type": "folder",
  "relative_path": "",
  "children": [
    {
      "type": "folder",
      "relative_path": "src",
      "children": [
        {
          "type": "file",
          "relative_path": "src/main.py",
          "content": "import sys\n\ndef main():\n    print(\"Hello, World!\")\n\nif __name__ == \"__main__\":\n    main()\n"
        },
        {
          "type": "file",
          "relative_path": "src/utils.py",
          "content": "# Utility functions\n\ndef helper():\n    pass\n"
        }
      ]
    },
    {
      "type": "file",
      "relative_path": "README.md",
      "content": "# My Project\n\nThis is a sample project.\n"
    }
  ]
}
```

## Notes & Troubleshooting

*   **Logging:** The script logs detailed information about skipped files/directories and the reasons to standard error (stderr). This does not interfere with the JSON output sent to standard output (stdout) unless you redirect stderr. Messages indicate when files are included or excluded from the structure.
*   **Performance:** Processing very large directories or directories with many large files can take time and consume memory.
*   **Output Size:** Be mindful that including large files or binary files (`--no-ignore-binary`, `--max-size -1`) can result in extremely large JSON output files.
*   **Encoding:** If file content looks garbled, experiment with the `--encoding` and `--errors` flags. `utf-8` with `errors=replace` is usually a safe default. When using `--errors strict`, files with encoding issues will be skipped and warnings will be logged.
*   **Directory Structure:** In the output JSON, folders are always listed before files to maintain a consistent, organized structure.
