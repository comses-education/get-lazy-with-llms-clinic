Great! Let's proceed with **Phase 2: Core File Traversal and Initial Filtering**.

**Phase 2: Core File Traversal and Initial Filtering**

**Step 2.1: Define Constants (`constants.py`)**

Update `dirdigest/dirdigest/constants.py` with the default ignore patterns.

```python
# dirdigest/dirdigest/constants.py
TOOL_NAME = "dirdigest"
TOOL_VERSION = "0.1.0" # Corresponds to pyproject.toml version

# Using gitignore style patterns.
# Ensure patterns for directories end with a '/' if they are meant to only match directories.
# Otherwise, fnmatch might match 'node_modules.txt' with 'node_modules'.
# For simplicity here, we'll rely on os.path.isdir checks later for directory-specific patterns
# if not using a library that handles this distinction well (like gitignore_parser).
# For now, fnmatch will be used, and it doesn't distinguish files from dirs based on trailing slash.

DEFAULT_IGNORE_PATTERNS = [
    # Hidden files and directories
    ".*",               # Matches .git, .DS_Store, .env, etc.
    "**/.DS_Store",     # More specific for .DS_Store in any subdir
    "**/Thumbs.db",

    # Binary and media files (common examples)
    "*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.tiff", "*.webp",
    "*.mp4", "*.avi", "*.mov", "*.mkv", "*.wmv",
    "*.mp3", "*.wav", "*.flac", "*.aac", "*.ogg",
    "*.exe", "*.dll", "*.so", "*.dylib", "*.app", "*.msi", "*.com", "*.bat", "*.sh",
    "*.zip", "*.tar", "*.tar.gz", "*.tar.bz2", "*.rar", "*.7z", "*.gz", "*.bz2",
    "*.woff", "*.woff2", "*.ttf", "*.otf", "*.eot",
    "*.pdf",
    "*.doc", "*.docx",
    "*.ppt", "*.pptx",
    "*.xls", "*.xlsx",
    "*.odt", "*.ods", "*.odp",
    "*.iso", "*.img", "*.dmg",

    # Development artifacts
    "*.pyc", "*.pyo", "*.pyd",
    "*.class", "*.jar", "*.war", "*.ear",
    "*.o", "*.obj", "*.lib", "*.a", "*.o.*", # *.o.* for object files from some compilers
    "__pycache__/",     # Matches the directory itself
    ".cache/",
    "dist/",
    "build/",
    "target/",          # Common for Java/Rust
    "out/",             # Common for some build systems
    "node_modules/",
    "bower_components/",
    ".venv/", "venv/", "ENV/", "env/", ".env/", # Virtual environments
    ".git/",            # VCS directories
    ".svn/",
    ".hg/",
    "*.egg-info/",

    # Data and temporary files
    "*.db", "*.sqlite", "*.sqlite3", "*.mdb",
    "*.log",
    "*.tmp", "*.temp", "*.bak", "*.swp", "~*", # ~* for Vim backup files
    "*.DS_Store", # Already covered by .*, but explicit is fine
    "Thumbs.db",  # Already covered by .*, but explicit is fine
]
```
*Self-correction:* Added more common extensions and ensured directory patterns like `__pycache__/` are listed. While `fnmatch` doesn't treat trailing slashes specially by default, having them helps convey intent. We'll refine matching for directory-only patterns if needed.

**Step 2.2: Pattern Matching Utilities (`utils/patterns.py`)**

Create/Update `dirdigest/dirdigest/utils/patterns.py`:

```python
# dirdigest/dirdigest/utils/patterns.py
import fnmatch
from pathlib import Path

def matches_pattern(path_str: str, pattern: str) -> bool:
    """
    Checks if a path string matches a single glob-style pattern.
    This is a simplified matcher. For full .gitignore style, a dedicated library is better.
    Path components are matched. e.g. pattern "dir/*.py" matches "dir/file.py"
    """
    # Normalize path separators for consistent matching, especially for Windows paths
    # fnmatch on Windows still expects / as separator in patterns
    path_str_normalized = path_str.replace(Path().sep, '/')
    return fnmatch.fnmatch(path_str_normalized, pattern)

def matches_patterns(path_str: str, patterns: list[str]) -> bool:
    """
    Checks if a path string matches any of the provided glob-style patterns.
    """
    # If a directory pattern ends with '/', we might want to ensure path_str is also a dir.
    # For now, simple fnmatch.
    for pattern in patterns:
        if matches_pattern(path_str, pattern):
            return True
    return False

def is_path_hidden(path_obj: Path) -> bool:
    """Checks if any part of the path starts with a dot."""
    # Check the name itself or any parent directory part in the relative path
    # For example, "dir/.hidden_subdir/file.txt" should be considered hidden.
    # os.path.basename check is not enough.
    # We are usually passed relative paths from the base directory.
    return any(part.startswith('.') for part in path_obj.parts)
```
*Self-correction:* `is_path_hidden` should check all parts of the path, not just the basename, to correctly identify files within hidden directories. `matches_pattern` added for clarity and to handle path normalization for `fnmatch`.

**Step 2.3: Implement Core Traversal Logic (`core.py`)**

Create/Update `dirdigest/dirdigest/core.py`:

```python
# dirdigest/dirdigest/core.py
import os
import pathlib
from typing import Any, Generator, Tuple

from dirdigest.constants import DEFAULT_IGNORE_PATTERNS
from dirdigest.utils.patterns import matches_patterns, is_path_hidden

# Placeholder for logging, will be replaced/enhanced in Phase 5
def log_debug(message: str): print(f"DEBUG: {message}")
def log_info(message: str): print(f"INFO: {message}")
def log_warning(message: str): print(f"WARNING: {message}")
def log_error(message: str): print(f"ERROR: {message}")


ProcessedItem = Tuple[pathlib.Path, str, dict[str, Any]] # Path, Type ("file"/"folder"), Attributes

def process_directory_recursive(
    base_dir_path: pathlib.Path,
    include_patterns: list[str],
    exclude_patterns: list[str],
    no_default_ignore: bool,
    max_depth: int | None,
    follow_symlinks: bool
    # More args will be added: max_size, ignore_errors, etc.
) -> Generator[ProcessedItem, None, None]:
    """
    Recursively traverses the directory, applying filters and yielding processed items.
    For now, it just yields paths of items that would be included.
    """
    log_info(f"Starting traversal of {base_dir_path}")
    log_debug(f"Include patterns: {include_patterns}")
    log_debug(f"Exclude patterns: {exclude_patterns}")
    log_debug(f"No default ignore: {no_default_ignore}")
    log_debug(f"Max depth: {max_depth}")
    log_debug(f"Follow symlinks: {follow_symlinks}")

    # Combine all exclude patterns
    effective_exclude_patterns = list(exclude_patterns)
    if not no_default_ignore:
        effective_exclude_patterns.extend(DEFAULT_IGNORE_PATTERNS)
    log_debug(f"Effective exclude patterns: {effective_exclude_patterns}")


    for root, dirs, files in os.walk(str(base_dir_path), topdown=True, followlinks=follow_symlinks):
        current_root_path = pathlib.Path(root)
        relative_root_path = current_root_path.relative_to(base_dir_path)

        # --- Depth Filtering ---
        current_depth = len(relative_root_path.parts)
        if relative_root_path == pathlib.Path("."): # Root itself is depth 0
            current_depth = 0
        
        log_debug(f"Walking: {current_root_path}, Rel: {relative_root_path}, Depth: {current_depth}")

        if max_depth is not None and current_depth >= max_depth:
            log_info(f"Max depth {max_depth} reached at {relative_root_path}, pruning subdirectories.")
            dirs[:] = []  # Don't descend further
            # Files in this directory (at max_depth) can still be processed below if max_depth allows current_depth
            if current_depth > max_depth : # only prune if current_depth has exceeded max_depth
                 files[:] = []


        # --- Directory Filtering (modifies `dirs` in place) ---
        # Iterate over a copy of dirs for safe removal
        original_dirs = list(dirs)
        dirs[:] = [] # Clear dirs, we will re-add only those that pass filters

        for dir_name in original_dirs:
            dir_path_obj = current_root_path / dir_name
            relative_dir_path_str = str(relative_root_path / dir_name)
            log_debug(f"  Considering dir: {relative_dir_path_str}")

            is_symlink = dir_path_obj.is_symlink() # Check before resolving if follow_symlinks is false
            if not follow_symlinks and is_symlink:
                log_info(f"  Skipping symlinked directory {relative_dir_path_str} (symlink following disabled).")
                continue

            # Resolve symlink if following is enabled and it's a link (os.walk handles this if followlinks=True)
            # However, for pattern matching, we might need the target's nature for some patterns.
            # For now, pattern matching is on the link name or path.

            if is_path_hidden(pathlib.Path(relative_dir_path_str)) and not no_default_ignore:
                 # Apply no_default_ignore to hidden files/dirs as well as pattern ignores
                log_info(f"  Skipping hidden directory {relative_dir_path_str}.")
                continue

            if matches_patterns(relative_dir_path_str, effective_exclude_patterns):
                log_info(f"  Skipping directory {relative_dir_path_str} due to exclude pattern.")
                continue
            
            # If include_patterns are specified, the directory must match at least one
            # unless it's an ancestor of an included file (handled by os.walk).
            # For explicit directory inclusion/exclusion, this check is important.
            if include_patterns and not matches_patterns(relative_dir_path_str, include_patterns):
                # This logic is tricky: if "foo/bar.txt" is included, "foo/" should not be skipped here.
                # os.walk will continue into 'foo'. We are filtering what `dirdigest` *itself* reports as a directory.
                # For now, if an include pattern is present, a dir must match it to be *explicitly* processed.
                # This might need refinement based on how we want to interpret dir includes.
                # A common interpretation: if includes are present, only included items (files or dirs) are processed.
                # If a dir is not explicitly included, it's skipped unless it's a necessary parent.
                # For now, let's assume this filter applies to directories we might *list* or *process content for*.
                # Actual traversal for finding files is handled by os.walk. This is more about pruning `dirs` for `os.walk`.
                log_info(f"  Directory {relative_dir_path_str} does not match any include pattern. Will still traverse for files if not pruned by os.walk due to other dirs.")
                # To prevent os.walk from traversing it if it doesn't match include:
                # dirs.remove(dir_name) # This was the old logic; new logic below.
            else: # Passed all filters or no include patterns specified, or matches include
                dirs.append(dir_name) # Re-add to dirs for os.walk to traverse
                # For now, we don't "yield" directories until we decide on their structure
                # yield (relative_root_path / dir_name, "folder", {"reason": "Passed dir filters"})


        # --- File Filtering and Yielding ---
        for file_name in files:
            file_path_obj = current_root_path / file_name
            relative_file_path = relative_root_path / file_name
            relative_file_path_str = str(relative_file_path)
            log_debug(f"    Considering file: {relative_file_path_str}")

            is_symlink = file_path_obj.is_symlink()
            if not follow_symlinks and is_symlink:
                log_info(f"    Skipping symlinked file {relative_file_path_str} (symlink following disabled).")
                continue
            
            # Actual file path (resolves symlink if follow_symlinks is True, but os.walk already gave us the target if so)
            # For consistency, always use file_path_obj which is based on what os.walk provided.

            if is_path_hidden(relative_file_path) and not no_default_ignore:
                log_info(f"    Skipping hidden file {relative_file_path_str}.")
                continue

            if matches_patterns(relative_file_path_str, effective_exclude_patterns):
                # Find which pattern matched for better logging (optional enhancement)
                log_info(f"    Skipping file {relative_file_path_str} due to exclude pattern.")
                continue

            if include_patterns and not matches_patterns(relative_file_path_str, include_patterns):
                log_info(f"    Skipping file {relative_file_path_str} as it does not match include patterns.")
                continue
            
            # If all filters pass:
            log_info(f"    Including file: {relative_file_path_str}")
            yield (relative_file_path, "file", {"reason": "Passed all filters"})
            # Later: add size, read content, etc.

    log_info(f"Traversal of {base_dir_path} finished.")

```
*Self-corrections and clarifications in `core.py`:*
*   Used `pathlib.Path` more consistently.
*   Clarified depth calculation. `max_depth` now means directories *at* `max_depth` are pruned from further traversal, but files *within* a directory at `max_depth -1` (i.e., files at `max_depth`) can still be processed. Corrected the pruning logic slightly.
*   Refined directory filtering: iterate over a copy of `dirs` for safe modification. Only add directories back to `dirs` if they pass filters. This ensures `os.walk` correctly prunes.
*   `is_path_hidden` now checks the relative path components.
*   The logic for directory inclusion vs. traversal is tricky. `os.walk` will traverse a directory if it's not pruned and might contain an included file. The filtering here in `dirs[:]` primarily controls what `os.walk` itself will descend into. The "yielding" of directories as items for the digest is a separate concern for later.
*   Basic logging placeholders added.

**Step 2.4: Integrate Basic Traversal with CLI (`cli.py`)**

First, add the new CLI options to `dirdigest/dirdigest/cli.py`:

```python
# ... (imports at the top of cli.py) ...
from dirdigest import core # Import the core module

# ... (inside @click.command decorator for main_cli) ...
# Add these options:
@click.option(
    '--include', '-i',
    multiple=True, # Can be specified multiple times
    help="Pattern(s) for files/directories to include (e.g., '*.py', 'docs/*'). "
         "Can be comma-separated or specified multiple times. "
         "If used, only matching items are included."
)
@click.option(
    '--exclude', '-x',
    multiple=True, # Can be specified multiple times
    help="Pattern(s) for files/directories to exclude (e.g., '*.log', 'node_modules/'). "
         "Can be comma-separated or specified multiple times."
)
@click.option(
    '--max-depth', '-d',
    type=click.IntRange(min=0), # Depth must be non-negative
    default=None, # Python None means unlimited
    show_default="unlimited",
    help='Maximum directory depth to traverse.'
)
@click.option(
    '--no-default-ignore',
    is_flag=True,
    default=False,
    show_default=True, # Shows that the default is to use ignore patterns
    help='Disable default ignore patterns (for hidden files, binaries, etc.).'
)
@click.option(
    '--follow-symlinks',
    is_flag=True,
    default=False,
    show_default=True,
    help='Follow symbolic links (default: false).'
)
# Update the main_cli function signature and body:
def main_cli(
    directory: pathlib.Path,
    output: click.utils.LazyFile,
    format: str,
    include: tuple[str, ...], # Click passes multiple options as a tuple
    exclude: tuple[str, ...],
    max_depth: int | None,
    no_default_ignore: bool,
    follow_symlinks: bool
):
    """
    dirdigest: Recursively processes directories and files,
    creating a structured digest in markdown or JSON format.
    """
    # --- Argument Parsing for include/exclude ---
    parsed_include_patterns = []
    for item in include:
        parsed_include_patterns.extend(p.strip() for p in item.split(',') if p.strip())

    parsed_exclude_patterns = []
    for item in exclude:
        parsed_exclude_patterns.extend(p.strip() for p in item.split(',') if p.strip())

    click.echo(f"Processing directory: {directory}")
    click.echo(f"Output to: {output.name if output != sys.stdout else 'stdout'}")
    click.echo(f"Format: {format}")
    click.echo(f"Include patterns: {parsed_include_patterns}")
    click.echo(f"Exclude patterns: {parsed_exclude_patterns}")
    click.echo(f"Max depth: {max_depth if max_depth is not None else 'unlimited'}")
    click.echo(f"No default ignore: {no_default_ignore}")
    click.echo(f"Follow symlinks: {follow_symlinks}")
    click.echo("--- Core Processing Output ---")

    # Call core processing logic
    processed_items_generator = core.process_directory_recursive(
        base_dir_path=directory,
        include_patterns=parsed_include_patterns,
        exclude_patterns=parsed_exclude_patterns,
        no_default_ignore=no_default_ignore,
        max_depth=max_depth,
        follow_symlinks=follow_symlinks
    )

    # For now, just print what the generator yields
    # This will be replaced by building the data tree and formatting
    item_count = 0
    for item_path, item_type, item_attrs in processed_items_generator:
        click.echo(f"  Yielded: [{item_type}] {item_path} (Attrs: {item_attrs})")
        item_count += 1
    
    click.echo(f"--- End Core Processing Output ({item_count} items yielded) ---")


    # Placeholder for formatting and writing output
    # result_data_tree, metadata = build_tree_from_generator(processed_items_generator)
    # formatted_output = formatter.format(result_data_tree, metadata, format)
    # output.write(formatted_output)

    if output != sys.stdout:
        click.echo(f"Digest would be written to {output.name}")

# ... (if __name__ == '__main__': ...)
```

**Verification for Phase 2:**

1.  Ensure your virtual environment is active and the package is installed (`uv pip install -e .`).
2.  Create a test directory structure. You can use the one from `tests/conftest.py` as a guide or create a simpler one manually:
    ```bash
    mkdir -p my_test_dir/subdir1 my_test_dir/.hidden_dir my_test_dir/node_modules
    touch my_test_dir/file1.txt
    touch my_test_dir/script.py
    touch my_test_dir/.configfile
    touch my_test_dir/subdir1/file2.md
    touch my_test_dir/.hidden_dir/secret.txt
    touch my_test_dir/image.png
    touch my_test_dir/app.log
    touch my_test_dir/node_modules/package.json
    ln -s my_test_dir/file1.txt my_test_dir/link_to_file1.txt # Create a symlink (if on Unix-like system)
    ```
3.  Test various CLI commands with this structure:
    *   `dirdigest ./my_test_dir/` (default behavior, observe logs)
    *   `dirdigest ./my_test_dir/ --no-default-ignore` (should include `.configfile`, `image.png`, etc.)
    *   `dirdigest ./my_test_dir/ -i "*.txt"` (should only consider `.txt` files)
    *   `dirdigest ./my_test_dir/ -i "*.txt" -i "*.md"`
    *   `dirdigest ./my_test_dir/ -i "*.txt,*.md"`
    *   `dirdigest ./my_test_dir/ -x "*.log"` (should exclude `app.log`)
    *   `dirdigest ./my_test_dir/ -x "subdir1/*"`
    *   `dirdigest ./my_test_dir/ --max-depth 0` (should only process files in `my_test_dir` itself, not `subdir1`)
    *   `dirdigest ./my_test_dir/ --max-depth 1`
    *   `dirdigest ./my_test_dir/ --follow-symlinks` (if you created `link_to_file1.txt`, observe if it's processed)

    Observe the `INFO: ...` and `DEBUG: ...` printouts from `core.py` to see how files and directories are being filtered. The final output will be lines like `Yielded: [file] ...`.

This completes Phase 2. We now have a core traversal mechanism that applies several key filtering rules. The next phase will focus on actually reading file content and building the hierarchical data structure for output.

Ready for Phase 3?