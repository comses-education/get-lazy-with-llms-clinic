# Test Suite for `dirdigest` 🦾

Welcome to the `dirdigest` test suite! This suite is designed to ensure the reliability, correctness, and robustness of the `dirdigest` command-line tool. We use `pytest` as our test runner and leverage various mock objects and fixtures to create isolated and repeatable test environments.

Our philosophy is to test thoroughly, from the command-line interface down to the core logic of file processing and output formatting. We believe that a strong test suite is the bedrock of a high-quality tool. (And also, it helps us sleep better at night, knowing the digital gremlins are kept at bay!)

## Running the Tests

It's as easy as pie! (A well-tested, perfectly baked pie, of course.)

1.  **Ensure Dependencies are Installed:**
    Make sure you have `pytest` and all project dependencies (including those used by `dirdigest` itself, like `click`, `rich`, `pyyaml`, `pyperclip`) installed in your Python environment. If you're using a `pyproject.toml` with a test group, you can typically install them via:
    ```bash
    # Example using pip with a common convention for test dependencies
    pip install -e .[test] 
    # Or, if you manage dependencies differently, ensure pytest is available.
    ```
    Refer to the main project's `README.md` or `CONTRIBUTING.md` for specific instructions on setting up the development environment.

2.  **Set Up Mock Directory Fixtures:**
    Some tests rely on pre-defined directory structures located in `tests/fixtures/test_dirs/`. A helper script is provided to create these structures with the necessary files, permissions, and symlinks:
    ```bash
    # From the root directory of the project (where dirdigest/ and tests/ are)
    ./setup_test_dirs.sh 
    ```
    It's recommended to run this script once before running the test suite, especially if you've made changes to the fixture definitions or are setting up the project for the first time.

3.  **Run `pytest`:**
    Navigate to the root directory of the `dirdigest` project (the one containing `pyproject.toml` and the `tests/` folder). Then, simply run:
    ```bash
    pytest
    ```
    This will discover and run all tests within the `tests/` directory.

    To run a specific test file:
    ```bash
    pytest tests/test_cli_args.py
    pytest tests/test_traversal_filtering.py
    # etc.
    ```

    To run a specific test function or class:
    ```bash
    pytest tests/test_configuration.py::TestConfigLoadingAndMerging::test_load_default_config_file_name
    pytest tests/test_content_processing.py::TestMaxSizeHandling
    ```

    For more verbose output (useful for debugging failures):
    ```bash
    pytest -vv
    ```

## Test Organization and Coverage

The tests are organized into several files, each focusing on a specific aspect of `dirdigest`:

*   **`tests/conftest.py`**:
    *   Contains shared `pytest` fixtures used across multiple test files.
    *   `runner`: Provides a `click.testing.CliRunner` instance to invoke CLI commands.
    *   `temp_test_dir`: Creates isolated temporary directories, populates them with mock file structures from `tests/fixtures/test_dirs/`, and manages CWD for tests. This is crucial for filesystem-dependent tests.
    *   `mock_pyperclip`: Mocks the `pyperclip` library for testing clipboard functionality without interacting with the system clipboard and for simulating clipboard errors.

*   **`tests/test_cli_args.py`**:
    *   **Focus**: Command-Line Interface (CLI) argument parsing and basic invocation.
    *   **Coverage**:
        *   Help messages (`-h`, `--help`).
        *   Version output (`--version`).
        *   Basic successful invocation with default arguments.
        *   Handling of invalid arguments (e.g., non-existent directory, file as directory).
        *   Parsing of various options like `--output`, `--format`, include/exclude patterns (at the parsing stage, not full effect), size/depth limits, and boolean flags.
        *   Verifies that parsed CLI options are correctly passed to underlying application logic (often by mocking core functions and inspecting call arguments).
        *   Clipboard enable/disable flags (`--no-clipboard`).

*   **`tests/test_traversal_filtering.py`**:
    *   **Focus**: Core file and directory traversal logic, and filtering mechanisms.
    *   **Coverage**:
        *   Basic recursive directory traversal.
        *   Application of default ignore patterns (e.g., `.git`, `__pycache__`, hidden files).
        *   Functionality of the `--no-default-ignore` flag.
        *   Correct handling and exclusion/inclusion of hidden files and directories.
        *   Enforcement of `--max-depth` for directory traversal.
        *   User-defined `--include` and `--exclude` patterns (glob matching for file types, directory paths).
        *   Precedence of `--exclude` patterns over `--include` patterns.
        *   Symbolic link handling: default behavior (not following) and with `--follow-symlinks` (following links to files and directories, handling of broken links).
    *   **Methodology**: Uses mock directory structures and primarily asserts against the set of *included files* extracted from JSON output for precision.

*   **`tests/test_content_processing.py`**:
    *   **Focus**: How `dirdigest` handles file content after selection.
    *   **Coverage**:
        *   `--max-size` enforcement: files below, at, and above the size limit.
        *   Handling of empty files (0KB).
        *   Behavior with file read errors:
            *   Permission denied errors (with and without `--ignore-errors`).
            *   Unicode decoding errors when attempting to read binary files as text (with and without `--ignore-errors`).
        *   Successful reading of standard UTF-8 files, including those with various Unicode characters.
    *   **Methodology**: Uses a dedicated mock directory with files of varying sizes and problematic content/permissions. Asserts against JSON output, checking for file inclusion, content, or `read_error` attributes.

*   **`tests/test_output_formatting.py`**:
    *   **Focus**: Validation of the structure and formatting of the generated Markdown and JSON outputs.
    *   **Coverage (Markdown)**:
        *   Correctness of the main header section (title, tool version, timestamp, summary statistics).
        *   Accurate rendering of the directory structure visualization (tree prefixes, indentation).
        *   Proper formatting of file content sections (headers, code blocks).
        *   Correct application of language hints in Markdown code blocks based on file extensions.
        *   Representation of files with read errors when `--ignore-errors` is active.
    *   **Coverage (JSON)**:
        *   Presence and correctness of all specified metadata fields (e.g., `tool_version`, `created_at`, `base_directory`, counts).
        *   Validation of the `root` node structure.
    *   **Methodology**: Uses mock directory structures and inspects the generated string output, often using regular expressions for flexible matching of Markdown, and `json.loads` for JSON.

*   **`tests/test_configuration.py`**:
    *   **Focus**: Loading and merging of settings from configuration files and CLI arguments.
    *   **Coverage**:
        *   Loading settings from the default `.diringest` file.
        *   Loading settings from a custom config file specified via `--config`.
        *   Correct precedence of CLI arguments over config file settings.
        *   Parsing of various data types from YAML (booleans, strings, numbers, lists for include/exclude).
        *   Handling of different config file structures (e.g., with a `default:` profile vs. flat).
        *   Graceful handling of malformed or missing configuration files.
    *   **Methodology**: Creates temporary config files with different contents, invokes the CLI with various combinations of config files and CLI arguments, and typically mocks core processing functions to inspect the *effective settings* passed to them.

## Mock Fixtures (`tests/fixtures/test_dirs/`)

This directory contains various pre-defined directory structures used by the tests. They are designed to cover a wide range of scenarios:

*   `empty_dir/`: An empty directory.
*   `simple_project/`: A basic project with a few files and one subdirectory.
*   `complex_project/`: A more elaborate structure with nested directories, hidden files, default-ignored directories (like `.git`, `__pycache__`, `node_modules`), and various file types. Used to test default ignores, depth, and complex traversals.
*   `large_files_dir/`: Contains files of specific sizes (small, medium/exact, large, empty) to test `--max-size`.
*   `hidden_files_dir/`: Specifically for testing handling of hidden files (e.g., `.config`) and files within hidden directories (e.g., `.hidden_subdir/somefile.txt`).
*   `symlink_dir/`: Contains target files/directories and various symbolic links (to file, to directory, broken link) to test symlink handling logic.
*   `symlink_loop_dir/`: Contains a simple symlink loop to test `os.walk`'s resilience (though `os.walk` handles this internally).
*   `content_processing_dir/`: Contains files for testing content-related scenarios:
    *   Files of different sizes (empty, small, exact-for-limit, large).
    *   A file with diverse UTF-8 characters.
    *   A binary file designed to cause UTF-8 decoding errors.
    *   A file that will have its permissions changed to unreadable during tests (`permission_denied_file.txt`).
*   `lang_hint_project/`: Contains files with various common extensions (`.py`, `.css`, `.json`, `.md`) as well as unknown extensions and files with no extension, to test language hinting in Markdown output.
*   `all_ignored_dir/`: A directory where all contents should be ignored by default patterns.
*   `special_chars_dir/`: Contains files and directory names with spaces, special characters, and Unicode characters to test path handling.

These fixtures are crucial for creating consistent and reproducible test conditions. The `setup_test_dirs.sh` script in the project root is provided to help create/recreate these fixtures easily.

---

Happy Testing! May your runs be green and your bugs be few (and easy to find)!