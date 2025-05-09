Okay, here's a detailed implementation plan for `dirdigest`, based *solely* on the `final-requirements.md` document, broken into small, sequential steps.

We will aim for a logical progression, building foundational pieces first, then core logic, output, and finally auxiliary features and polish.

---

**Phase 1: Project Setup and Basic CLI**

1.  **Step 1.1: Initialize Project Structure and Dependencies**
    *   Create the directory structure:
        ```
        dirdigest/
        ├── dirdigest/
        │   ├── __init__.py
        │   ├── cli.py
        │   ├── core.py
        │   ├── formatter.py
        │   ├── constants.py
        │   └── utils/
        │       ├── __init__.py
        │       ├── clipboard.py
        │       ├── config.py
        │       └── patterns.py
        ├── tests/
        │   └── (test files will be added based on the pre-generated suite)
        └── pyproject.toml
        ```
    *   Create `pyproject.toml` specifying Python 3.8+, and add initial dependencies: `click`, `rich`, `pyperclip`, `pyyaml`. Use `uv` for package management.
    *   Create empty placeholder files for all `.py` modules listed above.

2.  **Step 1.2: Implement Basic CLI with Click (`cli.py`)**
    *   Define the main `dirdigest` command group using `click.group()` or `click.command()`.
    *   Add the `TOOL_VERSION` to be displayed (e.g., "1.0.0" as a placeholder, perhaps in `constants.py`).
    *   Implement the primary arguments:
        *   `DIRECTORY`: `click.argument`, type `click.Path(exists=True, file_okay=False, readable=True, path_type=pathlib.Path)`, default current directory (`.`).
        *   `--output, -o`: `click.option`, type `click.File('w')`, default `sys.stdout`.
        *   `--format, -f`: `click.option`, type `click.Choice(['json', 'markdown'])`, default `'markdown'`.
    *   Add a simple placeholder function that is called by the CLI command, which prints the received values for `DIRECTORY`, `output`, and `format`.
    *   Ensure `dirdigest --help` and `dirdigest --version` work.

**Phase 2: Core File Traversal and Initial Filtering**

3.  **Step 2.1: Define Constants (`constants.py`)**
    *   Populate `DEFAULT_IGNORE_PATTERNS` with all patterns listed under "Default Ignore Patterns" in the requirements.
        *   Hidden files/dirs (`.*`)
        *   Binary/media (images, videos, audio, executables, archives, fonts, document formats like PDF/DOCX)
        *   Development artifacts (compiled code, cache dirs, build dirs, package manager dirs, VCS dirs)
        *   Data/temp files (DBs, logs, temp files, system files)
    *   Confirm `TOOL_VERSION` is defined here.

4.  **Step 2.2: Pattern Matching Utilities (`utils/patterns.py`)**
    *   Create a function `matches_patterns(path_str, patterns)` that takes a string path and a list of glob-style patterns.
    *   It should return `True` if `path_str` matches any pattern in `patterns`. (Consider using `fnmatch.fnmatch` or `gitignore_parser`'s matching logic if allowed by "Minimize external dependencies" or implement simplified globbing).
    *   This will be used for include, exclude, and default ignore patterns.

5.  **Step 2.3: Implement Core Traversal Logic (`core.py`)**
    *   Create a main function `process_directory_recursive(base_dir_path, cli_args)`.
    *   Use `os.walk()` for recursive traversal.
    *   Inside the loop for `root, dirs, files`:
        *   Calculate current depth relative to `base_dir_path`.
        *   **Directory Filtering:**
            *   If `cli_args.max_depth` is set and `current_depth >= cli_args.max_depth`, prune `dirs` list (`del dirs[:]`) to stop descending further into those branches.
            *   Apply exclusion logic to directories in `dirs`:
                *   Hidden: If `d.startswith('.')`.
                *   Default Ignores: If `not cli_args.no_default_ignore` and `d` matches any `DEFAULT_IGNORE_PATTERNS` applicable to directories (e.g., `__pycache__/`, `.git/`).
                *   User Excludes: If `d` matches any `cli_args.exclude_patterns`.
                *   If excluded, remove from `dirs` list and log reason (logging later).
            *   Apply inclusion logic to directories if `cli_args.include_patterns` are specified. If `include_patterns` exist, a directory must match one to remain in `dirs` (unless it's the root).
        *   **Symlink Handling:**
            *   Before processing items in `dirs` and `files`, check if they are symlinks using `os.path.islink()`.
            *   If `cli_args.follow_symlinks` is `False` (default) and an item is a symlink, skip it and log reason. `os.walk(followlinks=cli_args.follow_symlinks)`.
    *   Initialize counters: `included_files_count`, `excluded_files_count`, `total_content_size_kb`.
    *   Create an internal list/structure to store data about files to be included (path, size, content placeholder).

6.  **Step 2.4: Integrate Basic Traversal with CLI (`cli.py`)**
    *   In the main CLI function, parse `--include` and `--exclude` arguments.
        *   Handle multiple occurrences of the flags.
        *   Handle comma-separated lists within a single flag.
        *   Combine all patterns into single lists: `parsed_include_patterns`, `parsed_exclude_patterns`.
    *   Call `core.process_directory_recursive` with the `DIRECTORY` path and an object/dict containing all relevant CLI options (`max_depth`, `no_default_ignore`, `follow_symlinks`, `parsed_include_patterns`, `parsed_exclude_patterns`, `max_size`, etc.).
    *   For now, the core function can just print the files it *would* process after initial filtering.

**Phase 3: File Content Processing and Advanced Filtering**

7.  **Step 3.1: File Filtering and Content Reading (`core.py`)**
    *   Inside the `os.walk` loop, for each `file_name` in `files`:
        *   Construct full file path.
        *   Apply filtering sequence:
            1.  Hidden: If `file_name.startswith('.')`. Reason: "Is a hidden file".
            2.  Default Ignores (if `not cli_args.no_default_ignore`): If `file_name` matches `DEFAULT_IGNORE_PATTERNS`. Reason: "Matches default ignore pattern".
            3.  User Excludes: If `file_name` (or full relative path) matches `cli_args.exclude_patterns`. Reason: "Matches user-specified exclude pattern '{pattern}'".
            4.  User Includes (if `cli_args.include_patterns` exist): If `file_name` (or full relative path) does NOT match any `cli_args.include_patterns`. Reason: "Does not match any include pattern". (This check only applies if include patterns are provided).
            5.  Symlink (if `not cli_args.follow_symlinks` and is symlink). Reason: "Is a symlink (symlink following disabled)".
        *   If file passes above filters:
            *   Get file size using `os.path.getsize()`.
            *   Convert `cli_args.max_size` (KB) to bytes.
            *   If `file_size_bytes > cli_args.max_size_bytes`. Reason: "Exceeds max size (X KB > Y KB)".
            *   If all checks pass:
                *   Try to read file content: `with open(file_path, 'r', encoding='utf-8', errors='replace') as f: content = f.read()`.
                *   If `IOError` or `UnicodeDecodeError` occurs:
                    *   If `cli_args.ignore_errors` is `True`, log a warning and skip content. Reason: "Read error (ignored)".
                    *   Else, log an error and skip content (or potentially halt, but requirements say "continue on error"). Reason: "Read error".
                *   Add file info (relative path, type='file', size_kb, content) to the list of items for output. Increment `included_files_count` and `total_content_size_kb`.
        *   If file is excluded at any step, increment `excluded_files_count` and store the reason for logging.

8.  **Step 3.2: Build Hierarchical Data Structure (`core.py`)**
    *   Modify `process_directory_recursive` to build a nested dictionary structure representing the directory hierarchy (as described for JSON output) for *included* items.
    *   Each node: `{"relative_path": "...", "type": "folder" or "file", ...}`.
    *   File nodes: `{"size_kb": ..., "content": "..."}`.
    *   Folder nodes: `{"children": [...]}`.
    *   This structure will be passed to the formatters.

**Phase 4: Output Generation**

9.  **Step 4.1: Formatter Interface (`formatter.py`)**
    *   Define a base class `BaseFormatter` with an abstract method `format(data_tree, metadata)`.

10. **Step 4.2: JSON Formatter (`formatter.py`)**
    *   Create `JsonFormatter(BaseFormatter)`.
    *   Implement the `format` method:
        *   Construct the full JSON object:
            ```json
            {
              "metadata": { ... }, // Filled with collected stats
              "root": data_tree     // The hierarchical structure from Step 3.2
            }
            ```
        *   Metadata fields: `tool_version`, `created_at` (ISO-8601 timestamp), `base_directory`, `included_files_count`, `excluded_files_count`, `total_content_size_kb`.
        *   Use `json.dumps(..., indent=2)`.

11. **Step 4.3: Markdown Formatter (`formatter.py`)**
    *   Create `MarkdownFormatter(BaseFormatter)`.
    *   Implement the `format` method:
        *   **Header:** `# Directory Digest: /path/to/directory` and `*Generated by ...*` (with metadata).
        *   **Directory Structure:**
            *   Use `rich.tree.Tree` or similar to generate a text-based tree from `data_tree` (only file/folder names).
            *   Wrap this in a markdown code block: ` ```\n...\n``` `.
        *   **Contents:** `## Contents`
            *   Iterate through `data_tree` to find all files with content.
            *   For each file:
                *   `### ./relative/path/to/file.ext`
                *   Determine language hint (e.g., 'python' for `.py`, 'javascript' for `.js`).
                *   ` ```{lang_hint}\n{file_content}\n``` ` (if no hint, just ` ``` `).

12. **Step 4.4: Integrate Formatters in CLI (`cli.py`)**
    *   After `core.process_directory_recursive` returns the `data_tree` and collected `metadata_stats`:
    *   Instantiate the chosen formatter (`JsonFormatter` or `MarkdownFormatter`) based on `cli_args.format`.
    *   Call `formatter.format(data_tree, metadata_stats)`.
    *   Write the result to `cli_args.output` (stdout or file).

**Phase 5: Logging and Reporting**

13. **Step 5.1: Setup Rich Logging (`cli.py`)**
    *   At the beginning of the main CLI function, configure logging.
    *   Use `rich.console.Console(stderr=True)` for logging messages.
    *   Verbosity:
        *   `--quiet, -q`: Suppress all console log output except explicit errors printed by the program.
        *   Default: Log warnings and errors.
        *   `--verbose, -v`: Log INFO level (e.g., included/excluded files).
        *   `-vv`: Log DEBUG level (more detailed internal steps, if any).
    *   Store the console instance for use in other modules if needed (e.g., by passing it around or using a global/contextvar).

14. **Step 5.2: Implement Detailed Logging (`core.py`)**
    *   During traversal (Steps 2.3, 3.1):
        *   When a file/directory is included: `console.print(f"[green]Included:[/green] {relative_path}")` (if verbose).
        *   When a file/directory is excluded: `console.print(f"[red]Excluded:[/red] {relative_path} ({reason_for_exclusion})")` (if verbose).
            *   Ensure all exclusion reasons from "Logging of Included and Excluded Files" are covered.

15. **Step 5.3: Log Summary Statistics (`cli.py`)**
    *   After processing and formatting, if not quiet:
        *   Print `[bold green]Total included:[/bold green] {count}`.
        *   Print `[bold red]Total excluded:[/bold red] {count}`.
        *   Report `Total content size of included content: {size_kb} KB`.
        *   Report `Execution time: {time_seconds}s`.
    *   These statistics should already be part of the `metadata` object passed to formatters.

16. **Step 5.4: Progress Indicator (`core.py`)**
    *   Integrate `rich.progress.Progress`. This might involve:
        *   Counting total files/directories first (an optional pre-scan or estimate).
        *   Updating the progress bar as each item is processed in `os.walk`.
        *   Display only if not quiet and output is to a file (to avoid mixing with stdout digest). Or if stderr is a TTY.

17. **Step 5.5: Log File Option (`cli.py`)**
    *   If `--log-file` is specified:
        *   Set up a standard Python `logging.FileHandler` to write to the specified path.
        *   Format log messages appropriately for a file.
        *   Ensure `rich` console output still respects verbosity/quiet, independent of file logging. All `console.print` for logging could be replaced by standard `logging` calls, with `RichHandler` for console and `FileHandler` for file.

**Phase 6: Behavior Control and Configuration**

18. **Step 6.1: Clipboard Integration (`utils/clipboard.py` and `cli.py`)**
    *   In `utils/clipboard.py`, create `copy_to_clipboard(text)` using `pyperclip.copy(text)`.
    *   Wrap in `try-except` to catch `pyperclip.PyperclipException` or general `Exception`.
    *   In `cli.py`, after output is generated:
        *   If `cli_args.clipboard` is `True` (default behavior, check `--no-clipboard` flag):
            *   Call `copy_to_clipboard(output_string)`.
            *   If successful and not quiet, print "Content copied to clipboard."
            *   If fails and not quiet, print a warning: "Could not copy to clipboard: {error}".

19. **Step 6.2: Configuration File Loading (`utils/config.py`)**
    *   Function `load_config(config_path_str)`:
        *   Takes optional `config_path_str`. If `None`, tries to load `.diringest` from current directory.
        *   Uses `pyyaml` to parse the YAML file.
        *   Handles file not found or YAML parsing errors gracefully.
        *   Returns the parsed config dictionary.
    *   The function should be able to extract a specific profile if the YAML structure includes them (e.g., `config.get(profile_name, config.get('default', {}))`). For now, assume `--config` implies using the "default" profile or the whole file if not structured with profiles. (Full profile selection can be an enhancement if not explicitly requested via a CLI arg like `--profile`).

20. **Step 6.3: Merge CLI Arguments with Configuration (`cli.py`)**
    *   At the start of the main CLI function:
        1.  Load configuration using `utils.config.load_config(cli_args.config_file_path)`.
        2.  Establish final settings: For each option, if the CLI argument was explicitly provided (i.e., not its default value from `click`), it overrides the config file setting. Otherwise, use the config file setting. If not in config, use Click's default.
        *   Special care for list-like options (`include`, `exclude`): CLI overrides config entirely.
        *   This merged configuration object/dict is then used throughout the application.

**Phase 7: Final Touches and Documentation**

21. **Step 7.1: Enhance CLI Help Text (`cli.py`)**
    *   Review all `help="..."` strings for `click` options.
    *   Ensure clarity, mention defaults.
    *   Add examples for `--include`/`--exclude` (comma-separated and multiple flags).
    *   Explain default ignore behavior and `--no-default-ignore`.
    *   Use `rich` markup in help strings if Click/Rich integration allows easy styling of help output (Click's built-in help is usually good; `rich-click` could be an option if "minimize dependencies" allows).

22. **Step 7.2: Code Quality and Refinement**
    *   Add type hints consistently across the codebase.
    *   Run linters (e.g., Ruff or Flake8+Black) and formatters to ensure PEP 8 compliance and readability.
    *   Review for modularity and maintainability.

23. **Step 7.3: Documentation (External)**
    *   Create/update a `README.md` file for the project:
        *   Overview of `dirdigest`.
        *   Installation instructions (using `uv`).
        *   Comprehensive CLI usage guide mirroring the `--help` output but with more narrative.
        *   Detailed explanation of configuration file format (`.diringest`) with examples, including profiles if supported.
        *   Examples for common use cases.

24. **Step 7.4: Testing (Continuous)**
    *   Throughout all steps, implement and run tests from the pre-generated test suite. Adapt and expand tests as necessary to cover the implemented logic accurately. Ensure all specified main functionalities are tested.

---

This plan provides a structured approach. Each step is relatively small and builds upon the previous ones. The "Logging of Included and Excluded Files" and metadata requirements are addressed by collecting necessary information during traversal and then using it for both logging and final output.