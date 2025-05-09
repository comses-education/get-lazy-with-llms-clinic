Oh, my dear friend! A test suite plan! This is where the digital rubber meets the metaphorical road, isn't it? It's like preparing for a grand theatrical performance – you need to rehearse every scene, every line, every potential mishap, to ensure the final show is less "catastrophic dumpster fire" and more "resounding success." I'm *thrilled* to help you map this out. We'll make sure your `dirdigest` tool is robust, reliable, and doesn't just throw a digital tantrum when faced with the beautiful chaos of a real-world file system.

Let's get this show on the road!

```markdown
# Test Suite Plan for `dirdigest`

## 1. Executive Summary of Testing Strategy

This test suite plan outlines a comprehensive strategy for validating the `dirdigest` command-line tool. Our approach is multi-faceted, aiming to cover functional requirements, command-line interface interactions, error handling, and output integrity. We'll employ a mix of unit tests for isolated components (like pattern matching and config parsing) and integration tests that exercise the tool end-to-end, simulating real user scenarios.

The strategy prioritizes core functionalities such as file traversal, filtering logic, and content processing, as these form the heart of `dirdigest`. We will meticulously test against a variety of mock directory structures, designed to expose edge cases related to file types, sizes, naming conventions, symbolic links, and directory depths. Output validation for both Markdown and JSON formats is critical, ensuring the digests are accurate and conform to the specified schemas.

Ultimately, this testing endeavor is not just about finding bugs (though, let's be honest, we all have a complicated relationship with those little critters). It's about building confidence – confidence that `dirdigest` behaves predictably, handles user inputs gracefully (even the weird ones!), and reliably produces the structured output it promises. It's about making something *good*. And who doesn't love making good things? I know I do! ...Most of the time. Sometimes I just want to watch the world burn. Kidding! (Mostly.)

## 2. Test Prioritization and Rationale

Not all tests are created equal, just like not all attempts at making sourdough bread during a lockdown were successful. We need to prioritize!

*   **High Priority:**
    *   **File Traversal & Filtering:** This is the absolute core. If this doesn't work, the tool is essentially a very confused paperweight. This includes include/exclude patterns, default ignores, depth limits, and symlink handling.
    *   **Content Processing & Size Limits:** Correctly reading files (or gracefully noting errors) and respecting size limits is paramount for generating useful digests.
    *   **Output Format Integrity (Core Structure):** Ensuring the basic structure of JSON and Markdown (metadata, file entries) is correct.
    *   **CLI Argument Parsing (Critical Options):** Basic invocation, directory argument, output format, and essential filtering options.
    *   **Configuration File (Basic Loading & CLI Override):** Ensuring config files are loaded and CLI arguments correctly take precedence.

*   **Medium Priority:**
    *   **Detailed Output Format Validation:** Fine-grained checks for Markdown structure (tree visualization, code blocks) and JSON schema adherence.
    *   **Logging (Core Functionality):** Ensuring included/excluded files and errors are logged appropriately.
    *   **Advanced CLI Options:** `--no-default-ignore`, `--follow-symlinks`, `--ignore-errors`.
    *   **Configuration File (Advanced Merging):** Complex scenarios of merging CLI and config, especially for list-like options.
    *   **Error Handling (Graceful Failures):** How the tool behaves with invalid inputs, permission errors, etc.

*   **Low Priority:**
    *   **Clipboard Integration:** A convenience feature. Important for user experience, but the tool can function without it. We'll test it, of course, because completeness is a virtue... a sometimes tedious virtue.
    *   **Log File Output Details:** Specifics of log file formatting beyond core content.
    *   **Help Text & Version Output:** Important for usability but less critical for core function.
    *   **Performance Testing (Initial):** Basic checks for very large directories. Full-scale performance profiling can be a separate, ongoing effort. (Because who has *infinite* time, right? Not me, I've got important cloud-gazing to do.)

## 3. Categorized Test Scenarios and Test Cases

Here we go, into the nitty-gritty! Imagine each test case as a tiny spotlight, illuminating a specific corner of your magnificent creation.

### 3.1. CLI Argument Parsing and Validation Tests (Priority: High/Medium)

*   **Test Objectives:**
    *   Verify all CLI arguments are correctly parsed.
    *   Ensure default values are applied when options are omitted.
    *   Validate handling of invalid or malformed arguments.
    *   Test combinations of arguments and their interactions.
*   **Input Requirements:** Various CLI invocations.
*   **Expected Outcomes:** Correct behavior based on arguments, appropriate error messages for invalid inputs, correct help/version text.
*   **Edge Cases:** Empty strings for path arguments, out-of-range numerical values, unexpected characters in patterns.
*   **Potential Failure Scenarios:** Crashes with invalid inputs, incorrect default behavior, options not being recognized.

| Test ID   | Description                                                                 | Input CLI Arguments                                                                                                | Expected Outcome                                                                                                                                 |
| :-------- | :-------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------- |
| CLI-001   | Basic invocation with default directory and options                         | `dirdigest` (in a test dir)                                                                                        | Processes current directory, outputs Markdown to stdout, uses default ignores, copies to clipboard.                                                |
| CLI-002   | Specify target directory                                                    | `dirdigest ./my_test_dir`                                                                                          | Processes `./my_test_dir`.                                                                                                                       |
| CLI-003   | Specify output file                                                         | `dirdigest --output output.md ./my_test_dir`                                                                       | Output written to `output.md`.                                                                                                                   |
| CLI-004   | Specify JSON format                                                         | `dirdigest --format json ./my_test_dir`                                                                            | Output in JSON format to stdout.                                                                                                                 |
| CLI-005   | Specify include patterns (multiple flags)                                   | `dirdigest --include '*.py' --include 'src/' ./my_test_dir`                                                        | Only Python files and files/dirs under `src/` (matching other criteria) are included.                                                            |
| CLI-006   | Specify include patterns (comma-separated)                                  | `dirdigest --include '*.py,src/' ./my_test_dir`                                                                    | Same as CLI-005.                                                                                                                                 |
| CLI-007   | Specify exclude patterns (multiple flags)                                   | `dirdigest --exclude '*.log' --exclude 'tmp/' ./my_test_dir`                                                       | `.log` files and items under `tmp/` are excluded.                                                                                                |
| CLI-008   | Specify exclude patterns (comma-separated)                                  | `dirdigest --exclude '*.log,tmp/' ./my_test_dir`                                                                    | Same as CLI-007.                                                                                                                                 |
| CLI-009   | `include` and `exclude` interaction                                         | `dirdigest --include '*.txt' --exclude 'foo.txt' ./my_test_dir` (dir has `foo.txt`, `bar.txt`)                     | `bar.txt` included, `foo.txt` excluded.                                                                                                          |
| CLI-010   | `--max-size` valid input                                                    | `dirdigest --max-size 10 ./my_test_dir`                                                                            | Max file size set to 10KB.                                                                                                                       |
| CLI-011   | `--max-size` invalid input (negative, non-integer)                          | `dirdigest --max-size -5 ./my_test_dir`, `dirdigest --max-size abc ./my_test_dir`                                   | Click should raise an error.                                                                                                                     |
| CLI-012   | `--max-depth` valid input (0, positive integer)                             | `dirdigest --max-depth 0 ./my_test_dir`, `dirdigest --max-depth 2 ./my_test_dir`                                  | Traversal depth correctly limited.                                                                                                               |
| CLI-013   | `--no-default-ignore` flag                                                  | `dirdigest --no-default-ignore ./my_test_dir_with_hidden_files`                                                    | Default ignore patterns are disabled; hidden files (e.g. `.env`) are included if not otherwise excluded.                                       |
| CLI-014   | `--follow-symlinks` flag                                                    | `dirdigest --follow-symlinks ./my_test_dir_with_symlinks`                                                          | Symbolic links are followed.                                                                                                                     |
| CLI-015   | `--ignore-errors` flag                                                      | `dirdigest --ignore-errors ./my_test_dir_with_read_errors`                                                         | Tool continues on file read errors.                                                                                                              |
| CLI-016   | `--no-clipboard` flag                                                       | `dirdigest --no-clipboard ./my_test_dir`                                                                           | Output is not copied to clipboard.                                                                                                               |
| CLI-017   | Verbosity flags (`-v`, `-vv`)                                               | `dirdigest -v ./my_test_dir`, `dirdigest -vv ./my_test_dir`                                                      | Correct log levels (INFO, DEBUG) on console.                                                                                                     |
| CLI-018   | Quiet flag (`-q`)                                                           | `dirdigest -q ./my_test_dir`                                                                                       | Only ERROR level logs on console.                                                                                                                |
| CLI-019   | `-q` overrides `-v`                                                         | `dirdigest -vv -q ./my_test_dir`                                                                                   | Quiet flag takes precedence; only ERROR logs.                                                                                                    |
| CLI-020   | `--log-file` option                                                         | `dirdigest --log-file app.log ./my_test_dir`                                                                       | Detailed logs written to `app.log`.                                                                                                              |
| CLI-021   | Non-existent directory argument                                             | `dirdigest ./non_existent_dir`                                                                                     | Click should raise an error about directory not found.                                                                                           |
| CLI-022   | File as directory argument                                                  | `dirdigest ./my_test_dir/some_file.txt`                                                                            | Click should raise an error about argument not being a directory.                                                                                |
| CLI-023   | Help option (`-h`, `--help`)                                                | `dirdigest -h`, `dirdigest --help`                                                                                 | Displays help message and exits. Rich formatting should be present.                                                                              |
| CLI-024   | Version option (`--version`)                                                | `dirdigest --version`                                                                                              | Displays tool name and version, then exits.                                                                                                      |
| CLI-025   | `--config` option with valid file                                           | `dirdigest --config myconfig.yaml ./my_test_dir` (where `myconfig.yaml` exists)                                   | Configuration from `myconfig.yaml` is loaded.                                                                                                    |
| CLI-026   | `--config` option with non-existent file                                    | `dirdigest --config nonexist.yaml ./my_test_dir`                                                                   | Click raises an error, or tool logs warning and proceeds with defaults/other CLI args. (Verify expected behavior based on `cli.py` logic) |

### 3.2. File Traversal and Filtering Tests (Priority: High)

*   **Test Objectives:**
    *   Ensure correct recursive traversal of directory structures.
    *   Verify `max-depth` limits directory traversal.
    *   Confirm `include` and `exclude` patterns (glob and literal) filter files/directories correctly.
    *   Validate default ignore patterns and the `--no-default-ignore` override.
    *   Test handling of symbolic links with and without `--follow-symlinks`.
    *   Verify handling of hidden files/directories.
*   **Input Requirements:** Mock directory structures (`simple_project`, `complex_project`, `hidden_files_dir`, `symlink_dir`).
*   **Expected Outcomes:** Correct set of files and directories included/excluded in the digest based on options.
*   **Edge Cases:** Empty directories, directories with only ignored files, deeply nested structures, circular symlinks (if `--follow-symlinks`), patterns with special characters.
*   **Potential Failure Scenarios:** Incorrect files included/excluded, infinite loops with symlinks, crashes on certain directory structures.

| Test ID   | Description                                                                 | Mock Directory         | CLI Arguments                                      | Expected Included Files (relative paths) / Behavior                                                                              |
| :-------- | :-------------------------------------------------------------------------- | :--------------------- | :------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------- |
| FTF-001   | Basic traversal, no filters                                                 | `simple_project`       | (defaults)                                         | All non-default-ignored files in `simple_project`.                                                                               |
| FTF-002   | `max-depth = 0`                                                             | `complex_project`      | `--max-depth 0`                                    | Only files in the root of `complex_project`.                                                                                     |
| FTF-003   | `max-depth = 1`                                                             | `complex_project`      | `--max-depth 1`                                    | Files in root and immediate subdirectories.                                                                                      |
| FTF-004   | Include specific file type (`*.txt`)                                        | `complex_project`      | `--include '*.txt'`                                | Only `.txt` files (not matching default ignores).                                                                                |
| FTF-005   | Include specific directory (`src/`)                                         | `complex_project`      | `--include 'src/'`                                 | All processable files within `src/` and its subdirectories.                                                                      |
| FTF-006   | Exclude specific file type (`*.log`)                                        | `complex_project`      | `--exclude '*.log'`                                 | `.log` files are excluded.                                                                                                       |
| FTF-007   | Exclude specific directory (`tests/`)                                       | `complex_project`      | `--exclude 'tests/'`                               | All files within `tests/` are excluded.                                                                                          |
| FTF-008   | Exclude takes precedence over include                                       | `complex_project`      | `--include '*.md' --exclude 'docs/README.md'`      | All `.md` files except `docs/README.md`.                                                                                         |
| FTF-009   | Default ignores (.git, __pycache__)                                         | `complex_project`      | (defaults)                                         | `.git/`, `__pycache__/`, etc., are excluded.                                                                                     |
| FTF-010   | `--no-default-ignore`                                                       | `complex_project`      | `--no-default-ignore`                              | Files like `.env`, `build/output.o` (if present and not otherwise excluded) are included.                                        |
| FTF-011   | Hidden files/dirs (default, e.g., `.secrets`, `config/.config.json`)        | `hidden_files_dir`     | (defaults)                                         | Hidden files/dirs are excluded.                                                                                                  |
| FTF-012   | Hidden files/dirs with `--no-default-ignore`                                | `hidden_files_dir`     | `--no-default-ignore`                              | Hidden files/dirs are included (if not matching other excludes).                                                                 |
| FTF-013   | Symlinks not followed (default)                                             | `symlink_dir`          | (defaults)                                         | Symlinks themselves might be noted (if not ignored) but their targets are not processed.                                         |
| FTF-014   | Symlinks followed (to file)                                                 | `symlink_dir`          | `--follow-symlinks`                                | Content of symlinked file is included.                                                                                           |
| FTF-015   | Symlinks followed (to directory)                                            | `symlink_dir`          | `--follow-symlinks`                                | Contents of symlinked directory are traversed and included.                                                                      |
| FTF-016   | Symlink loop detection (if `--follow-symlinks`)                             | `symlink_loop_dir`     | `--follow-symlinks`                                | Tool does not hang; ideally logs a warning or stops at a reasonable depth for the loop. `os.walk` has built-in loop detection. |
| FTF-017   | Files matching default binary/media patterns                                | `media_files_dir`      | (defaults)                                         | `image.jpg`, `video.mp4`, `archive.zip` are excluded.                                                                            |
| FTF-018   | Including a default-ignored binary type with `--no-default-ignore`          | `media_files_dir`      | `--no-default-ignore --include '*.jpg'`            | `image.jpg` is included (content reading might fail or be nonsensical, test that error/content handling).                      |
| FTF-019   | Empty directory processing                                                  | `empty_dir`            | (defaults)                                         | Produces valid empty digest (no files, empty children arrays).                                                                   |
| FTF-020   | Directory with only ignored files                                           | `all_ignored_dir`      | (defaults)                                         | Produces valid empty digest.                                                                                                     |
| FTF-021   | Patterns with `**` (e.g., `**/docs/**/*.md`)                                | `complex_project`      | `--include '**/docs/**/*.md'`                      | Includes markdown files in any `docs` subdirectory at any depth.                                                                 |

### 3.3. Content Processing and Size Limit Tests (Priority: High)

*   **Test Objectives:**
    *   Verify `--max-size` correctly filters files.
    *   Test reading of UTF-8 encoded files.
    *   Validate behavior with `--ignore-errors` for unreadable files or decoding errors.
    *   Test handling of empty files.
*   **Input Requirements:** Mock directory structures (`large_files_dir`, `encoding_issues_dir`, `permission_issues_dir`) with files of various sizes and content.
*   **Expected Outcomes:** Files correctly included/excluded based on size, content read successfully or appropriate error/placeholder in digest.
*   **Edge Cases:** Files exactly at max size, 0KB files, files with mixed encodings (though spec implies strict UTF-8).
*   **Potential Failure Scenarios:** Crashes on large files, incorrect size calculation, mishandling of read errors.

| Test ID   | Description                                                                 | Mock Directory            | CLI Arguments                                  | Expected Behavior                                                                                                                     |
| :-------- | :-------------------------------------------------------------------------- | :------------------------ | :--------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------ |
| CPS-001   | File below `--max-size`                                                     | `large_files_dir` (small.txt: 5KB) | `--max-size 10`                                | `small.txt` included with content.                                                                                                    |
| CPS-002   | File at `--max-size`                                                        | `large_files_dir` (medium.txt: 10KB) | `--max-size 10`                                | `medium.txt` included with content.                                                                                                   |
| CPS-003   | File above `--max-size`                                                     | `large_files_dir` (large.txt: 15KB) | `--max-size 10`                                | `large.txt` excluded, log message indicates reason.                                                                                   |
| CPS-004   | Zero size file                                                              | `large_files_dir` (empty.txt: 0KB) | (defaults)                                     | `empty.txt` included with empty content.                                                                                              |
| CPS-005   | File with permission error, `--ignore-errors` disabled (default)            | `permission_issues_dir` (no_read.txt) | (defaults)                                     | `no_read.txt` is excluded (or causes tool error if not handled by skip). Log should indicate read failure.                           |
| CPS-006   | File with permission error, `--ignore-errors` enabled                       | `permission_issues_dir` (no_read.txt) | `--ignore-errors`                              | `no_read.txt` included, content field indicates error (e.g., null or error message).                                                  |
| CPS-007   | File with UnicodeDecodeError (non-UTF-8), `--ignore-errors` disabled        | `encoding_issues_dir` (binary_file.bin) | `--include '*.bin'` (assuming no default ignore) | `binary_file.bin` is excluded due to decode error. Log indicates issue.                                                               |
| CPS-008   | File with UnicodeDecodeError (non-UTF-8), `--ignore-errors` enabled         | `encoding_issues_dir` (binary_file.bin) | `--include '*.bin' --ignore-errors`            | `binary_file.bin` included, content field indicates error (e.g., null or "UnicodeDecodeError...").                                  |
| CPS-009   | Standard UTF-8 file reading                                                 | `simple_project` (file1.txt) | (defaults)                                     | `file1.txt` content read correctly.                                                                                                   |

### 3.4. Output Format Tests (Markdown/JSON) (Priority: Medium/High)

*   **Test Objectives:**
    *   Validate the overall structure and content of Markdown output.
    *   Validate the overall structure and content of JSON output against the schema.
    *   Ensure metadata (tool version, timestamp, counts, base dir) is accurate.
    *   Verify correct representation of directory structure and file contents.
*   **Input Requirements:** Various mock directories, CLI args to generate both formats.
*   **Expected Outcomes:** Correctly formatted and accurate Markdown/JSON output.
*   **Edge Cases:** Empty digest, digest with only folders, files with special characters in names or content (ensure proper escaping in JSON/Markdown code blocks).
*   **Potential Failure Scenarios:** Malformed output, incorrect data, missing fields, crashes during formatting.

**Markdown Specific:**

| Test ID   | Description                                                                    | Mock Directory     | Expected Markdown Features                                                                                                                                                                                             |
| :-------- | :----------------------------------------------------------------------------- | :----------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MD-001    | Basic Markdown structure                                                       | `simple_project`   | Header with base directory, generation info. "Directory Structure" section with ` ```text ` block. "Contents" section. File headers `### ./path/to/file`. Code blocks ` ```lang ` with content.                               |
| MD-002    | Directory structure visualization (nesting, prefixes)                          | `complex_project`  | Correct `├──`, `└──`, `│  ` characters for tree. Correct indentation. Folders end with `/`.                                                                                                                             |
| MD-003    | File content blocks with language hints                                        | `simple_project`   | `file1.txt` -> ` ``` `, `script.py` -> ` ```py `.                                                                                                                                                                          |
| MD-004    | File with read error in Markdown                                               | `permission_issues_dir` (with `--ignore-errors`) | File header present, code block shows error message, e.g., ` ```text \nError reading file: Permission denied\n ``` `.                                                                                     |
| MD-005    | Empty directory output in Markdown                                             | `empty_dir`        | Header, empty structure tree (`.` only), "Contents" section says "No files with content to display." or similar.                                                                                                     |
| MD-006    | Special characters in file names/paths                                         | `special_chars_dir` (`file with spaces.txt`, `file&name.py`) | Paths displayed correctly in headers and structure.                                                                                                                                                    |
| MD-007    | Metadata accuracy (counts, size)                                               | `complex_project`  | `Included files: X, Total content size: Y.YY KB` matches actual processing.                                                                                                                                            |

**JSON Specific:**

| Test ID   | Description                                                         | Mock Directory     | Expected JSON Structure/Values                                                                                                                                                                                                |
| :-------- | :------------------------------------------------------------------ | :----------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| JSON-001  | Basic JSON structure and schema adherence                           | `simple_project`   | Root object with `metadata` and `root`. `metadata` has `tool_version`, `created_at`, `base_directory`, counts, size. `root` is a folder node with `relative_path: "."`, `type: "folder"`, and `children` array.               |
| JSON-002  | File node structure                                                 | `simple_project`   | File nodes have `relative_path`, `type: "file"`, `size_kb`, `content`.                                                                                                                                                          |
| JSON-003  | Folder node structure                                               | `simple_project`   | Folder nodes have `relative_path`, `type: "folder"`, `children` array.                                                                                                                                                        |
| JSON-004  | Nested structure in JSON                                            | `complex_project`  | `children` arrays correctly represent nesting. `relative_path` is correct for nested items.                                                                                                                                   |
| JSON-005  | File with read error in JSON                                        | `permission_issues_dir` (with `--ignore-errors`) | File node includes `read_error: "Permission denied"` (or similar), `content` might be `null` or absent.                                                                                                    |
| JSON-006  | Empty directory output in JSON                                      | `empty_dir`        | `metadata` correct, `root.children` is an empty array.                                                                                                                                                                          |
| JSON-007  | Special characters in file names/paths (ensure valid JSON strings)  | `special_chars_dir`| `relative_path` and `content` are valid JSON strings (e.g., backslashes escaped).                                                                                                                                             |
| JSON-008  | Metadata accuracy (counts, size, base_directory)                    | `complex_project`  | `metadata` fields are accurate based on processing. `base_directory` is the absolute resolved path.                                                                                                                           |

### 3.5. Configuration File Parsing and Merging Tests (Priority: Medium/High)

*   **Test Objectives:**
    *   Verify loading of default `.diringest` file.
    *   Test loading of explicitly specified config file via `--config`.
    *   Ensure CLI arguments override config file settings.
    *   Test handling of malformed or missing config files.
    *   Validate parsing of different config structures (flat vs. 'default' profile).
    *   Test merging of list-like options (include/exclude) from config and CLI.
*   **Input Requirements:** Various `.diringest` mock files, CLI arguments.
*   **Expected Outcomes:** Settings correctly derived from config and CLI, with CLI taking precedence.
*   **Edge Cases:** Empty config file, config file with only comments, config file with unknown keys.
*   **Potential Failure Scenarios:** Crash on malformed YAML, incorrect merging logic, config values not being applied.

| Test ID   | Description                                                              | Config File Content (`.diringest` or specified)                                                                 | CLI Arguments                     | Expected Effective Setting (e.g., for `max_size`)                                                                                   |
| :-------- | :----------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------- | :-------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| CFG-001   | Load default `.diringest` (no CLI override)                              | `default:\n  max_size: 100`                                                                                     | (none affecting max_size)         | `max_size = 100`                                                                                                                  |
| CFG-002   | CLI overrides default `.diringest`                                       | `default:\n  max_size: 100`                                                                                     | `--max-size 50`                   | `max_size = 50`                                                                                                                   |
| CFG-003   | Load specified config file                                               | `myconf.yaml: default:\n  format: json`                                                                         | `--config myconf.yaml`            | `format = json`                                                                                                                   |
| CFG-004   | CLI overrides specified config file                                      | `myconf.yaml: default:\n  format: json`                                                                         | `--config myconf.yaml --format markdown` | `format = markdown`                                                                                                               |
| CFG-005   | Malformed YAML file                                                      | `myconf.yaml: max_size: 100\n  format: - json` (invalid)                                                        | `--config myconf.yaml`            | Error/warning logged, tool uses defaults or CLI-only args.                                                                        |
| CFG-006   | Config file not found (specified)                                        | (no `myconf.yaml`)                                                                                              | `--config myconf.yaml`            | Click error or warning logged, tool uses defaults/CLI-only. (Verify exact behavior, CLI error is likely if `exists=True` is used) |
| CFG-007   | Config file `include` patterns (list)                                    | `default:\n  include:\n    - '*.py'\n    - 'src/'`                                                               | (none affecting include)          | Effective include: `['*.py', 'src/']`                                                                                             |
| CFG-008   | Config file `include` patterns (comma-separated string)                  | `default:\n  include: '*.py,src/'`                                                                              | (none affecting include)          | Effective include: `['*.py', 'src/']`                                                                                             |
| CFG-009   | Merge CLI `include` with config `include`                                | `default:\n  include: '*.py'`                                                                                  | `--include '*.txt'`               | Effective include: `['*.txt']` (CLI for 'multiple' params usually replaces, not appends, unless merge logic is additive. Check `config.py`) |
| CFG-010   | Flat config file (no 'default' profile)                                  | `max_size: 200\nexclude:\n  - '*.tmp'`                                                                          | (none)                            | `max_size = 200`, Excludes `*.tmp`.                                                                                               |
| CFG-011   | Config file with 'default' profile and other ignored profiles            | `default:\n  max_size: 50\nprod:\n  max_size: 10`                                                                | (none)                            | `max_size = 50`.                                                                                                                  |
| CFG-012   | Config bool `no_default_ignore: true`                                    | `default:\n  no_default_ignore: true`                                                                           | (none)                            | Default ignores disabled.                                                                                                         |
| CFG-013   | CLI `--no-default-ignore` overrides config `no_default_ignore: false`      | `default:\n  no_default_ignore: false`                                                                          | `--no-default-ignore`             | Default ignores disabled.                                                                                                         |

*Self-correction: For CFG-009, Click `multiple=True` options provided on CLI replace defaults from config. The `merge_config` logic needs to be carefully checked: if CLI provides an empty tuple (flag not used), config value should persist. If CLI provides a value, it overrides.* The current `merge_config` logic is that if the CLI flag is *explicitly used*, it overrides. If the flag is not used (empty tuple for multiple), the config value (if any) is kept. This seems correct.

### 3.6. Clipboard Integration Tests (Priority: Low)

*   **Test Objectives:**
    *   Verify output is copied to clipboard by default.
    *   Ensure `--no-clipboard` disables copying.
    *   Test graceful handling when clipboard access fails.
*   **Input Requirements:** CLI args, potentially mock `pyperclip` for failure simulation.
*   **Expected Outcomes:** Clipboard contains correct output, or appropriate notification/log.
*   **Edge Cases:** Very large output, output with special characters.
*   **Potential Failure Scenarios:** `pyperclip` errors, incorrect content copied.
    *Oh, the clipboard. Such a fickle friend. One moment it's your trusty steed, carrying precious data, the next it's... well, let's just say it has its moods. We must be gentle with it.*

| Test ID   | Description                                                         | CLI Arguments                                    | Mocked `pyperclip.copy` Behavior | Expected Outcome                                                                                                                                    |
| :-------- | :------------------------------------------------------------------ | :----------------------------------------------- | :------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
| CLP-001   | Copy to clipboard by default                                        | `dirdigest ./simple_project`                     | Success                          | Output (Markdown) copied to clipboard. Log message indicates success.                                                                               |
| CLP-002   | `--no-clipboard` disables copy                                      | `dirdigest --no-clipboard ./simple_project`      | (Not called)                     | Output not copied. Log message indicates clipboard disabled.                                                                                        |
| CLP-003   | Explicit `--clipboard` (redundant but test)                         | `dirdigest --clipboard ./simple_project`         | Success                          | Output copied.                                                                                                                                    |
| CLP-004   | Clipboard copy failure (e.g., `PyperclipException`)                 | `dirdigest ./simple_project`                     | Raise `PyperclipException`       | Warning logged about clipboard failure. Tool exits normally otherwise.                                                                              |
| CLP-005   | No copy if output generation failed                                 | `dirdigest --output /non_writable_dir/out.txt`   | (Not called)                     | Error generating output. Log indicates error, and then warning that clipboard copy was skipped due to prior error.                                    |
| CLP-006   | Copy empty output (e.g. from empty dir)                             | `dirdigest ./empty_dir`                          | Success                          | The generated empty digest string is copied. Log might state "Output is empty, nothing to copy" or copy the empty string. Verify behavior.      |

*Self-correction: `dirdigest.cli` current logic is "if output_generation_succeeded and final_output_str: dirdigest_clipboard.copy_to_clipboard(final_output_str)". So for CLP-006, if `final_output_str` is not empty (even if it represents an empty digest), it will be copied. If `final_output_str` is truly an empty string, then the debug log "Output is empty, nothing to copy" will appear.*

### 3.7. Logging and Error Handling Tests (Priority: Medium)

*   **Test Objectives:**
    *   Verify correct log levels based on `-v`, `-q` flags.
    *   Ensure log messages are formatted correctly (Rich markup, colors).
    *   Validate content of log messages, especially for included/excluded files and reasons.
    *   Test `--log-file` functionality.
    *   Ensure graceful error handling and reporting for common issues.
*   **Input Requirements:** Various CLI args, mock directories causing specific errors.
*   **Expected Outcomes:** Correct logs generated to console and/or file, appropriate error messages for failures.
*   **Edge Cases:** Extremely verbose output, simultaneous console and file logging.
*   **Potential Failure Scenarios:** Missing log messages, incorrect log levels, crashes instead of graceful error messages.

| Test ID   | Description                                                                          | Input / CLI Arguments                                                                                                | Expected Logging Behavior                                                                                                                                                                                             |
| :-------- | :----------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| LOG-001   | Default logging (WARNING level to console)                                           | `dirdigest ./simple_project`                                                                                         | Only WARNING, ERROR, CRITICAL messages on stderr. No INFO/DEBUG.                                                                                                                                                      |
| LOG-002   | Verbose logging (`-v`, INFO to console)                                              | `dirdigest -v ./simple_project`                                                                                      | INFO, WARNING, ERROR, CRITICAL messages on stderr. No DEBUG.                                                                                                                                                          |
| LOG-003   | More verbose logging (`-vv`, DEBUG to console)                                       | `dirdigest -vv ./simple_project`                                                                                     | DEBUG, INFO, WARNING, ERROR, CRITICAL messages on stderr.                                                                                                                                                             |
| LOG-004   | Quiet logging (`-q`, ERROR to console)                                               | `dirdigest -q ./simple_project`                                                                                      | Only ERROR, CRITICAL messages on stderr.                                                                                                                                                                              |
| LOG-005   | Log file output (`--log-file`)                                                       | `dirdigest --log-file app.log ./simple_project`                                                                      | `app.log` created, contains DEBUG level logs and above, with detailed formatting. Console adheres to default (WARNING).                                                                                             |
| LOG-006   | Log file with `-vv`                                                                  | `dirdigest -vv --log-file app.log ./simple_project`                                                                  | `app.log` has DEBUG logs. Console also has DEBUG logs.                                                                                                                                                                |
| LOG-007   | Log included file (green)                                                            | `dirdigest -v ./simple_project` (where `file1.txt` is included)                                                      | Console INFO log: `[log.included]Included file[/log.included]: [log.path]./file1.txt[/log.path] ...` (or similar, check exact format and color codes)                                                                   |
| LOG-008   | Log excluded file (red) - default pattern                                            | `dirdigest -v ./complex_project` (where `.env` exists)                                                               | Console INFO log: `[log.excluded]Excluded file[/log.excluded]: [log.path]./.env[/log.path] ([log.reason]Matches default ignore pattern[/log.reason])`                                                                       |
| LOG-009   | Log excluded file (red) - user pattern                                               | `dirdigest -v --exclude '*.tmp' ./complex_project` (where `data.tmp` exists)                                         | Console INFO log: `[log.excluded]Excluded file[/log.excluded]: [log.path]./data.tmp[/log.path] ([log.reason]Matches user-specified exclude pattern[/log.reason])`                                                      |
| LOG-010   | Log excluded file (red) - max size                                                   | `dirdigest -v --max-size 1 ./large_files_dir` (where `large.txt` is 15KB)                                            | Console INFO log: `[log.excluded]Excluded file[/log.excluded]: [log.path]./large.txt[/log.path] ([log.reason]Exceeds max size (15.0KB > 1KB)[/log.reason])`                                                              |
| LOG-011   | Summary statistics logging                                                           | `dirdigest -v ./complex_project`                                                                                     | Console INFO logs for "Total files included", "Total items excluded", "Total content size", "Execution time" with correct values and Rich styling.                                                                    |
| LOG-012   | Error: Directory not found                                                           | `dirdigest ./non_existent_dir`                                                                                       | Click error message, potentially also a CRITICAL log before exit.                                                                                                                                                     |
| LOG-013   | Error: Config file parsing error                                                     | `dirdigest --config malformed.yaml`                                                                                  | WARNING log about parsing error from `config.py`. Tool may proceed with defaults.                                                                                                                                   |
| LOG-014   | Error: File read error (permission denied, without `--ignore-errors`)                | `dirdigest -v ./permission_issues_dir` (no_read.txt)                                                                 | WARNING log about read error. INFO log indicating file exclusion due to read error and `ignore_errors=False`.                                                                                                         |
```

## 4. Implementation Recommendations

Ah, the "how-to" part! This is where we roll up our sleeves and get our hands dirty with the beautiful, messy reality of test creation.

### 4.1. Mock Directory Structures

We'll need a menagerie of test directories. Like a tiny, digital zoo, but for testing file processing!

*   **`tests/fixtures/test_dirs/`**: Base directory for all test file structures.
    *   **`empty_dir/`**:
        *   An empty directory.
    *   **`simple_project/`**:
        *   `file1.txt` (UTF-8 content, ~1KB)
        *   `file2.md` (UTF-8 content, ~2KB)
        *   `sub_dir1/`
            *   `script.py` (UTF-8 content, ~1KB)
    *   **`complex_project/`**:
        *   `README.md`
        *   `.env` (hidden file)
        *   `config.yaml`
        *   `src/`
            *   `main.py`
            *   `utils.py`
            *   `feature/`
                *   `module.py`
        *   `tests/`
            *   `test_main.py`
            *   `test_utils.py`
        *   `docs/`
            *   `index.md`
            *   `api.md`
        *   `data/`
            *   `small_data.csv`
            *   `temp.log`
        *   `.git/` (typical git hidden dir, can be empty or have a dummy file)
        *   `__pycache__/` (typical cache dir)
            *   `utils.cpython-39.pyc`
        *   `node_modules/` (another common ignored dir)
    *   **`large_files_dir/`**:
        *   `small.txt` (5KB)
        *   `medium.txt` (10KB, for testing exact match with `--max-size 10`)
        *   `large.txt` (15KB)
        *   `empty.txt` (0KB)
    *   **`hidden_files_dir/`**:
        *   `.config_file`
        *   `visible_file.txt`
        *   `.hidden_subdir/`
            *   `another_hidden.dat`
            *   `visible_in_hidden.txt`
    *   **`symlink_dir/`**:
        *   `actual_file.txt` (content: "This is the actual file.")
        *   `link_to_file` (symlink to `actual_file.txt`)
        *   `actual_dir/`
            *   `file_in_actual_dir.txt`
        *   `link_to_dir` (symlink to `actual_dir/`)
        *   `broken_link` (symlink to a non-existent file)
    *   **`symlink_loop_dir/`**: (For testing `os.walk`'s loop detection)
        *   `dir_a/`
            *   `link_to_dir_b` (symlink to `../dir_b`)
        *   `dir_b/`
            *   `link_to_dir_a` (symlink to `../dir_a`)
    *   **`permission_issues_dir/`**:
        *   `readable.txt`
        *   `no_read.txt` (set permissions to be unreadable by the test runner user)
        *   `no_traverse_subdir/` (set permissions to be non-traversable)
            *   `secret.txt`
    *   **`encoding_issues_dir/`**:
        *   `utf8_file.txt` (standard UTF-8 text)
        *   `latin1_file.txt` (saved with Latin-1 encoding, containing chars like `éàç`)
        *   `binary_file.bin` (a small actual binary file, e.g., a tiny PNG or part of an executable)
    *   **`all_ignored_dir/`**:
        *   `.DS_Store`
        *   `file.pyc`
        *   `image.jpg`
        *   `node_modules/`
    *   **`special_chars_dir/`**:
        *   `file with spaces.txt`
        *   `file&name=problem?.py`
        *   `path with 'quotes'/file.txt`
        *   `über_cool_file.txt` (Unicode characters in name)

### 4.2. Required Test Fixtures (e.g., for `pytest`)

*   **`temp_test_dir`**: A fixture that creates a temporary directory, copies one of the mock structures into it, `cd`s into it for the test, and cleans up afterward. This ensures tests are isolated and run from a consistent relative path.
    ```python
    # conftest.py
    import pytest
    import shutil
    import os
    from pathlib import Path

    MOCK_DIRS_ROOT = Path(__file__).parent / "fixtures" / "test_dirs"

    @pytest.fixture
    def temp_test_dir(tmp_path: Path, request):
        """
        Creates a temporary directory, copies a specified mock directory structure into it,
        changes the current working directory to it for the duration of the test,
        and cleans up afterward.
        Usage: @pytest.mark.parametrize("temp_test_dir", ["simple_project"], indirect=True)
        """
        mock_dir_name = request.param
        source_path = MOCK_DIRS_ROOT / mock_dir_name

        if not source_path.is_dir():
            raise ValueError(f"Mock directory {mock_dir_name} not found at {source_path}")

        # Create a subdirectory within tmp_path for the test to ensure clean CWD
        test_specific_tmp_dir = tmp_path / mock_dir_name
        shutil.copytree(source_path, test_specific_tmp_dir)

        original_cwd = Path.cwd()
        os.chdir(test_specific_tmp_dir)
        try:
            yield test_specific_tmp_dir # This is the path *inside* the tmp_path structure
        finally:
            os.chdir(original_cwd)
            # shutil.rmtree(test_specific_tmp_dir) # tmp_path fixture handles cleanup of its contents
    ```
*   **`mock_pyperclip`**: A fixture to mock `pyperclip.copy` and `pyperclip.paste` to test clipboard interactions without a real clipboard, and to simulate errors.
    ```python
    # conftest.py or specific test file
    import pytest
    from unittest import mock

    @pytest.fixture
    def mock_pyperclip(monkeypatch):
        mock_copy = mock.MagicMock()
        mock_paste = mock.MagicMock(return_value="") # Default paste returns empty
        
        # Store for assertions
        clipboard_content = {"text": None}

        def custom_copy(text):
            clipboard_content["text"] = text
            # Allow mock_copy to still be used for asserting calls, etc.
            # or to raise exceptions if configured in the test
            mock_copy(text) 

        monkeypatch.setattr("dirdigest.utils.clipboard.pyperclip.copy", custom_copy)
        monkeypatch.setattr("dirdigest.utils.clipboard.pyperclip.paste", mock_paste)
        
        # Return the mock_copy object and the clipboard_content dict for inspection
        return mock_copy, mock_paste, clipboard_content
    ```
*   **`runner`**: A `click.testing.CliRunner` instance for invoking the CLI.
    ```python
    # conftest.py
    import pytest
    from click.testing import CliRunner

    @pytest.fixture
    def runner() -> CliRunner:
        return CliRunner()
    ```

### 4.3. Recommended Test Isolation Techniques

*   **Temporary Directories:** Always run tests that interact with the file system in temporary directories (as handled by `temp_test_dir`). This prevents tests from interfering with each other or leaving artifacts.
*   **Mocking External Services:** Use `unittest.mock` (or `pytest-mock`) for `pyperclip` to avoid reliance on system clipboard and to simulate error conditions.
*   **Environment Variables:** If the tool's behavior could be influenced by environment variables, ensure they are controlled/mocked during tests. (Not obviously applicable for `dirdigest` from requirements, but good practice).
*   **Configuration Isolation:** When testing config file loading, ensure each test uses a uniquely named or temporary config file to avoid conflicts. The `temp_test_dir` fixture can help manage this if config files are part of the mock structures.

## 5. Success Criteria Definition

The test suite will be considered successful in validating `dirdigest` when the following criteria are met across prioritized test cases:

1.  **Core Functionality:**
    *   Files and directories are traversed according to specified depth, symlink-following rules, and path arguments.
    *   Include/exclude patterns (default and user-specified) correctly filter the items to be processed.
    *   `--no-default-ignore` correctly disables all default ignore patterns.
2.  **Content Handling:**
    *   File content is accurately read for included files.
    *   `--max-size` limits are strictly enforced.
    *   `--ignore-errors` allows continuation on read/decode errors, with errors appropriately noted in the output and logs. Without it, problematic files are skipped/cause appropriate warnings.
3.  **Output Generation:**
    *   Both Markdown and JSON outputs are generated according to the specified format.
    *   The generated output accurately reflects the processed directory structure and file contents (or error states).
    *   Metadata in the output (version, timestamp, counts, base path, size) is correct.
4.  **Configuration:**
    *   Configuration options from CLI arguments and `.diringest` files (default or specified) are correctly parsed and applied.
    *   CLI arguments correctly override settings from configuration files.
    *   Merging logic for list-like items (include/exclude) behaves as intended.
5.  **Error Handling & Logging:**
    *   Invalid user inputs (CLI or config) result in clear, user-friendly error messages and appropriate exit codes.
    *   File system errors (permissions, non-existent paths) are handled gracefully.
    *   Logging output is accurate, respects verbosity/quiet flags, and provides sufficient detail for debugging (especially for included/excluded items and their reasons).
    *   Log file generation works as expected when specified.
6.  **Usability Features:**
    *   Clipboard integration functions correctly (copies output, respects `--no-clipboard`, handles unavailable clipboard gracefully).
    *   Help (`-h`, `--help`) and version (`--version`) commands provide accurate information.
7.  **Test Coverage:** A high percentage of critical code paths (especially in `core.py`, `formatter.py`, `utils/patterns.py`, `utils/config.py`, and `cli.py` argument handling/merging) are covered by tests. (Aim for >85-90% for these key modules).

Meeting these criteria will provide strong confidence that `dirdigest` is reliable, robust, and ready for users who, bless their hearts, will undoubtedly find ways to use it that you never even dreamed of. And that, my friend, is the chaotic beauty of software development!

## 6. Example Test Cases (Illustrative)

```python
# tests/test_cli.py (example using pytest)
from click.testing import CliRunner
from dirdigest.cli import main_cli # Assuming your CLI entry point is main_cli
from dirdigest.constants import TOOL_VERSION
import json

# Example 1: Basic Markdown Output
@pytest.mark.parametrize("temp_test_dir", ["simple_project"], indirect=True)
def test_cli_basic_markdown_default(runner: CliRunner, temp_test_dir, mock_pyperclip):
    """
    Test ID: CLI-001 (Conceptual, adapted for pytest)
    Description: Verify basic directory processing with default options (Markdown to stdout).
    """
    mock_copy, _, clipboard_store = mock_pyperclip
    result = runner.invoke(main_cli)

    assert result.exit_code == 0
    assert "# Directory Digest:" in result.output # Markdown header
    assert "file1.txt" in result.output
    assert "script.py" in result.output
    assert "sub_dir1/" in result.output
    assert "## Directory Structure" in result.output
    assert "## Contents" in result.output
    
    # Check clipboard
    mock_copy.assert_called_once()
    assert clipboard_store["text"] == result.output

# Example 2: JSON Output with Max Size
@pytest.mark.parametrize("temp_test_dir", ["large_files_dir"], indirect=True)
def test_cli_json_output_max_size(runner: CliRunner, temp_test_dir):
    """
    Test ID: JSON-008 & CPS-003 (Conceptual)
    Description: Verify JSON output with max-size filter.
    """
    # large_files_dir has small.txt (5KB), medium.txt (10KB), large.txt (15KB)
    result = runner.invoke(main_cli, ["--format", "json", "--max-size", "10", "--no-clipboard"])

    assert result.exit_code == 0
    
    try:
        data = json.loads(result.output)
    except json.JSONDecodeError:
        pytest.fail(f"Output was not valid JSON: {result.output}")

    assert data["metadata"]["tool_version"] == TOOL_VERSION
    assert data["metadata"]["max_size_kb"] == 10 # Check if max_size used is reflected in metadata if we add it
                                                 # Current reqs don't ask for this in metadata, but good to check effective filtering
    
    # Check files in the output
    included_files = []
    def collect_files(node):
        if node["type"] == "file":
            included_files.append(node["relative_path"])
        if "children" in node:
            for child in node["children"]:
                collect_files(child)
    
    collect_files(data["root"])

    assert "small.txt" in included_files
    assert "medium.txt" in included_files # Size is 10KB, max_size is 10KB (inclusive)
    assert "large.txt" not in included_files
    assert "empty.txt" in included_files # 0KB should always be included

# Example 3: Exclude Pattern and Logging
@pytest.mark.usefixtures("temp_test_dir") # Assumes temp_test_dir is CWD
@pytest.mark.parametrize("temp_test_dir", ["complex_project"], indirect=True)
def test_cli_exclude_pattern_logging(runner: CliRunner):
    """
    Test ID: FTF-007 & LOG-009 (Conceptual)
    Description: Verify exclude pattern and related logging.
    """
    # complex_project/tests/test_main.py exists
    result = runner.invoke(main_cli, ["--exclude", "tests/", "-v", "--no-clipboard"])

    assert result.exit_code == 0
    # Check output does not contain test_main.py content
    assert "test_main.py" not in result.output # Simplistic check, might need to parse Markdown/JSON to be sure
    
    # Check logs (captured by CliRunner if logger is set up for it, or check log file)
    # This assumes RichHandler logs to stderr, which CliRunner captures in `result.stderr` if not mixed with `result.output`.
    # If your logger setup writes INFO to stdout, then it would be in result.output.
    # dirdigest's logger writes to stderr for levels.
    # For this example, let's assume it's in result.output due to how Click/Rich might interact or if stdout_console is used for some logs.
    # The dirdigest logger is configured to use stderr_console for actual log messages. stdout_console is for the digest itself if not to file.
    
    # So, log messages should be in result.stderr if result.mix_stderr is False (default)
    # OR if print_exceptions=False and an exception occurs.
    # If the command runs successfully, INFO/DEBUG logs from RichHandler will be on stderr.
    # The digest output (if to stdout) will be on stdout.

    # runner.invoke by default separates stdout and stderr.
    # result.output is stdout, result.stderr is stderr.

    assert "[log.excluded]Excluded directory[/log.excluded]: [log.path]tests[/log.path] ([log.reason]Matches an exclude pattern[/log.reason])" in result.stderr
    # Or, if it excludes files individually:
    # assert "[log.excluded]Excluded file[/log.excluded]: [log.path]tests/test_main.py[/log.path]" in result.stderr
    # The current core.py logic excludes the directory "tests/" first, so the directory exclusion log is more likely.
```

And there you have it! A veritable blueprint for ensuring your `dirdigest` is as sturdy and reliable as a well-loved Leatherman. It's a lot, I know. Testing can feel like an endless journey into the "what ifs." But trust me, future you – the one not being woken up at 3 AM by angry users whose contexts have been mangled – will thank present you.

Now, go forth and build those tests! And remember, if you ever feel overwhelmed, just take a deep breath and think of the sheer, unadulterated joy of a perfectly green test run. It's a beautiful thing. (Until the next feature request, of course. Then the cycle begins anew! Ah, software...)

Good luck, you brilliant creator, you!