Excellent! Let's move on to **Phase 3: File Content Processing and Advanced Filtering**.

This phase involves:
*   Filtering files based on `max_size`.
*   Reading file content.
*   Handling read errors gracefully if `ignore_errors` is set.
*   Building the hierarchical data structure that will be passed to the formatters.

**Step 3.1: File Filtering (Max Size) and Content Reading (`core.py`)**

We'll modify `dirdigest/dirdigest/core.py`.

First, update the `process_directory_recursive` function signature to accept `max_size_kb` and `ignore_read_errors`.

Then, inside the file processing loop, add the size check and content reading logic.

```python
# dirdigest/dirdigest/core.py
import os
import pathlib
from typing import Any, Generator, Tuple, List, Dict # Changed from list, dict to List, Dict

from dirdigest.constants import DEFAULT_IGNORE_PATTERNS
from dirdigest.utils.patterns import matches_patterns, is_path_hidden

log_level = "INFO" 

def log_debug(message: str):
    if log_level == "DEBUG": print(f"DEBUG: {message}")
def log_info(message: str):
    if log_level in ["INFO", "DEBUG"]: print(f"INFO: {message}")
def log_warning(message: str):
    if log_level in ["WARNING", "INFO", "DEBUG"]: print(f"WARNING: {message}")
def log_error(message: str):
    print(f"ERROR: {message}")

# Represents an item in the directory structure (file or folder)
# For files, 'content' and 'size_kb' will be present.
# For folders, 'children' will be present.
DigestItemNode = Dict[str, Any] 

# ProcessedItem from generator will now contain more attributes for files
# For files: (relative_path, "file", {"size_kb": float, "content": str | None, "read_error": str | None})
# For folders (if we start yielding them): (relative_path, "folder", {})
ProcessedItemPayload = Dict[str, Any]
ProcessedItem = Tuple[pathlib.Path, str, ProcessedItemPayload]


def process_directory_recursive(
    base_dir_path: pathlib.Path,
    include_patterns: List[str],
    exclude_patterns: List[str],
    no_default_ignore: bool,
    max_depth: int | None,
    follow_symlinks: bool,
    max_size_kb: int, # New argument
    ignore_read_errors: bool # New argument
) -> Generator[ProcessedItem, None, None]:
    # ... (initial setup, effective_exclude_patterns - no changes here) ...
    log_debug(f"Core: Max size KB: {max_size_kb}, Ignore read errors: {ignore_read_errors}")
    max_size_bytes = max_size_kb * 1024

    for root, dirs_orig, files_orig in os.walk(str(base_dir_path), topdown=True, followlinks=follow_symlinks):
        current_root_path = pathlib.Path(root)
        relative_root_path = current_root_path.relative_to(base_dir_path)
        current_depth = len(relative_root_path.parts)
        if relative_root_path == pathlib.Path("."): current_depth = 0
        log_debug(f"Walking: {current_root_path}, Rel: {relative_root_path}, Depth: {current_depth}")

        # --- Depth Filtering ---
        if max_depth is not None and current_depth >= max_depth:
            log_info(f"Max depth ({max_depth}) reached at {relative_root_path}, pruning further subdirectory traversal.")
            dirs_orig[:] = []
        
        # --- Directory Filtering ---
        dirs_to_traverse_next = []
        for dir_name in dirs_orig:
            dir_path_obj = current_root_path / dir_name
            relative_dir_path = relative_root_path / dir_name
            relative_dir_path_str = str(relative_dir_path)
            log_debug(f"  Considering dir for traversal: {relative_dir_path_str}")
            
            is_symlink = dir_path_obj.is_symlink()
            if not follow_symlinks and is_symlink:
                log_info(f"  Skipping traversal of symlinked directory {relative_dir_path_str} (symlink following disabled).")
                continue
            if is_path_hidden(relative_dir_path) and not no_default_ignore:
                log_info(f"  Skipping traversal of hidden directory {relative_dir_path_str}.")
                continue
            if matches_patterns(relative_dir_path_str, effective_exclude_patterns):
                log_info(f"  Skipping traversal of directory {relative_dir_path_str} due to exclude pattern.")
                continue
            log_debug(f"  Queueing directory for os.walk traversal: {relative_dir_path_str}")
            dirs_to_traverse_next.append(dir_name)
        dirs_orig[:] = dirs_to_traverse_next

        # --- File Filtering and Content Reading ---
        for file_name in files_orig:
            file_path_obj = current_root_path / file_name # This is the absolute path
            relative_file_path = relative_root_path / file_name
            relative_file_path_str = str(relative_file_path)
            log_debug(f"    Considering file for inclusion: {relative_file_path_str}")

            # Standard filters (symlink, hidden, exclude, include)
            is_symlink = file_path_obj.is_symlink()
            if not follow_symlinks and is_symlink:
                log_info(f"    Skipping symlinked file {relative_file_path_str} (symlink following disabled).")
                continue
            if is_path_hidden(relative_file_path) and not no_default_ignore:
                log_info(f"    Skipping hidden file {relative_file_path_str}.")
                continue
            if matches_patterns(relative_file_path_str, effective_exclude_patterns):
                log_info(f"    Skipping file {relative_file_path_str} due to an exclude pattern.")
                continue
            if include_patterns and not matches_patterns(relative_file_path_str, include_patterns):
                log_info(f"    Skipping file {relative_file_path_str} as it does not match any include patterns.")
                continue

            # If we get here, the file has passed initial pattern filters. Now check size and read content.
            file_attributes: ProcessedItemPayload = {}
            
            try:
                # For size check, use stat on the actual file path (which os.walk gives, resolved if followlinks=True)
                file_size_bytes = file_path_obj.stat().st_size
                file_attributes["size_kb"] = round(file_size_bytes / 1024, 3)

                if file_size_bytes > max_size_bytes:
                    log_info(f"    Skipping file {relative_file_path_str} (Size: {file_attributes['size_kb']:.1f}KB > Max: {max_size_kb}KB).")
                    file_attributes["content"] = None # Indicate skipped due to size
                    file_attributes["skipped_reason"] = f"Exceeds max size ({file_attributes['size_kb']:.1f}KB > {max_size_kb}KB)"
                    # Even if skipped for size, we might still want to log it as "processed" for counts
                    # For now, let's not yield it if skipped for size, to align with "included_files_count"
                    continue # Skip yielding this file

                # Try reading content
                log_debug(f"    Reading content for: {relative_file_path_str}")
                with open(file_path_obj, 'r', encoding='utf-8', errors='replace') as f:
                    file_attributes["content"] = f.read()
                file_attributes["read_error"] = None

            except OSError as e: # Covers FileNotFoundError, PermissionError, etc.
                error_msg = f"OS error reading file {relative_file_path_str}: {e}"
                log_warning(error_msg)
                if not ignore_read_errors:
                    log_error(f"    Halting on read error (ignore_errors=False) for {relative_file_path_str}.")
                    # Or, if we want to continue processing other files but mark this one as errored:
                    # For now, let's adopt the "continue on error" from requirements, so skip this file from digest.
                    # Requirement: "Generate appropriate warnings for skipped or unreadable content"
                    # Requirement: "--ignore-errors: Continue on error when reading files (default: false)"
                    # This implies if ignore_errors is false, we might not continue OR we skip the file.
                    # Let's make it skip the file from the digest if ignore_errors is false and error occurs.
                    continue # Skip this file from the digest
                
                # If ignore_errors is True, we include it in the digest but without content
                file_attributes["content"] = None
                file_attributes["read_error"] = str(e)
                if "size_kb" not in file_attributes: # If stat() also failed
                     file_attributes["size_kb"] = 0.0
            
            except UnicodeDecodeError as e:
                error_msg = f"Unicode decode error reading file {relative_file_path_str}: {e}. File may be binary or use an unexpected encoding."
                log_warning(error_msg)
                if not ignore_read_errors:
                    log_error(f"    Halting on decode error (ignore_errors=False) for {relative_file_path_str}.")
                    continue # Skip this file

                file_attributes["content"] = None # Cannot include content
                file_attributes["read_error"] = "UnicodeDecodeError: " + str(e)
                # Size might have been read successfully before this
                if "size_kb" not in file_attributes: # If stat() failed before read attempt
                     try:
                        file_size_bytes = file_path_obj.stat().st_size
                        file_attributes["size_kb"] = round(file_size_bytes / 1024, 3)
                     except OSError:
                        file_attributes["size_kb"] = 0.0

            log_info(f"    Including file in digest: {relative_file_path_str} (Size: {file_attributes.get('size_kb', 0):.1f}KB)")
            yield (relative_file_path, "file", file_attributes)

    log_info(f"Core: Traversal of {base_dir_path} finished.")

```

**Changes in `core.py`:**
*   **Function Signature**: Added `max_size_kb: int` and `ignore_read_errors: bool`.
*   `max_size_bytes`: Calculated from `max_size_kb`.
*   **File Size Check**:
    *   Uses `file_path_obj.stat().st_size` to get the size.
    *   If size > `max_size_bytes`, logs a message and `continue`s (skips yielding this file). The requirements say "Generate appropriate warnings for skipped or unreadable content", implying skipped-for-size files are not in the final digest.
    *   Stores `size_kb` in `file_attributes`.
*   **Content Reading**:
    *   Wrapped in `try...except OSError as e:` and `try...except UnicodeDecodeError as e:`.
    *   If an error occurs:
        *   Logs a warning.
        *   If `ignore_read_errors` is `False` (default), it logs an error and `continue`s (skips the file from the digest).
        *   If `ignore_read_errors` is `True`, it sets `content` to `None`, stores the `read_error` message in `file_attributes`, and the file (without content) is still yielded.
    *   File content is read with `encoding='utf-8', errors='replace'` to handle most text files gracefully, replacing undecodable characters. `UnicodeDecodeError` is caught for more problematic cases.
*   **Yielded Item**: Now yields `(relative_file_path, "file", file_attributes)`, where `file_attributes` is a dictionary containing `size_kb`, `content` (or `None`), and `read_error` (or `None`).
*   **Type Hinting**: Changed `list`, `dict` to `List`, `Dict` for older Python compatibility if needed, though for 3.9+ built-in types are fine. Added `DigestItemNode` and updated `ProcessedItem` for clarity.

**Step 3.2: Build Hierarchical Data Structure (`core.py`)**

This step involves taking the flat list of `ProcessedItem`s yielded by `process_directory_recursive` and organizing it into the nested dictionary structure required for JSON/Markdown output. This is typically done *after* the generator has produced all its items.

We'll create a new function for this.

Add this function to `dirdigest/dirdigest/core.py`:

```python
# ... (at the end of core.py) ...

def build_digest_tree(
    base_dir_path: pathlib.Path, # For metadata
    processed_items: Generator[ProcessedItem, None, None]
) -> Tuple[DigestItemNode, Dict[str, Any]]:
    """
    Builds the hierarchical tree structure from the flat list of processed items.
    Also calculates metadata.
    """
    root_node: DigestItemNode = {
        "relative_path": ".",
        "type": "folder",
        "children": []
    }
    
    # Statistics for metadata
    included_files_count = 0
    excluded_files_count = 0 # This needs to be tallied during traversal, not here. Placeholder.
    total_content_size_kb = 0.0
    # We'll need to pass excluded_files_count from the traversal or recalculate somehow.
    # For now, focusing on included files structure.

    for relative_path, item_type, attributes in processed_items:
        if item_type == "file":
            included_files_count += 1
            if attributes.get("size_kb"): # size_kb might be missing if stat failed AND ignore_errors=True
                total_content_size_kb += attributes["size_kb"]

            parts = list(relative_path.parts)
            current_level_children = root_node["children"]
            current_path_so_far = pathlib.Path(".") # Keep track of path for nodes

            for i, part_name in enumerate(parts[:-1]): # Iterate through parent directory parts
                current_path_so_far = current_path_so_far / part_name
                # Find or create folder node
                folder_node = next((child for child in current_level_children if child["relative_path"] == str(current_path_so_far) and child["type"] == "folder"), None)
                if not folder_node:
                    folder_node = {
                        "relative_path": str(current_path_so_far),
                        "type": "folder",
                        "children": []
                    }
                    current_level_children.append(folder_node)
                current_level_children = folder_node["children"]
            
            # Add file node
            file_node: DigestItemNode = {
                "relative_path": str(relative_path),
                "type": "file",
                "size_kb": attributes.get("size_kb", 0.0), # Default if missing
            }
            if "content" in attributes : # Content might be None
                file_node["content"] = attributes["content"]
            if attributes.get("read_error"):
                file_node["read_error"] = attributes["read_error"]
            if attributes.get("skipped_reason"): # e.g. for size limit, though we currently 'continue'
                file_node["skipped_reason"] = attributes["skipped_reason"]

            current_level_children.append(file_node)
        # else: item_type == "folder" (not yielded by current generator)

    # Sort children alphabetically by relative_path for consistent output
    def sort_children_recursive(node: DigestItemNode):
        if node["type"] == "folder" and "children" in node:
            node["children"].sort(key=lambda x: x["relative_path"])
            for child in node["children"]:
                sort_children_recursive(child)
    
    sort_children_recursive(root_node)

    metadata = {
        # "tool_version": TOOL_VERSION, # Will be added by CLI or formatter
        # "created_at": datetime.now().isoformat(), # Will be added by CLI or formatter
        "base_directory": str(base_dir_path.resolve()),
        "included_files_count": included_files_count,
        "excluded_files_count": 0, # Needs proper calculation from traversal logs/stats
        "total_content_size_kb": round(total_content_size_kb, 3)
    }
    
    return root_node, metadata
```

**Changes in `core.py` for `build_digest_tree`:**
*   Takes the generator `processed_items`.
*   Iterates through yielded files, creating parent directory nodes in the `root_node` structure as needed.
*   Adds file nodes with their attributes (`size_kb`, `content`, `read_error`).
*   Recursively sorts children for consistent output.
*   Calculates some metadata (`included_files_count`, `total_content_size_kb`). `excluded_files_count` is a placeholder as it's not directly available from the *included* items generator. This count will need to be passed from the `process_directory_recursive` function or its caller if we want it accurate in metadata *from this function*. The requirements state "Logging of Included and Excluded Files" which will generate these counts during traversal.

**Update `cli.py` to call the new functions and pass new arguments:**

Modify `dirdigest/dirdigest/cli.py`:

```python
# dirdigest/dirdigest/cli.py
# ... (imports, command, options - no changes to options themselves) ...

def main_cli(
    directory: pathlib.Path,
    output: click.utils.LazyFile,
    format: str,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    max_size: int, # This is max_size_kb from the option
    max_depth: int | None,
    no_default_ignore: bool,
    follow_symlinks: bool,
    ignore_errors: bool, # This is ignore_read_errors
    clipboard: bool,
    verbose: int,
    quiet: bool,
    log_file: pathlib.Path | None,
    config: pathlib.Path | None
):
    # ... (parsing include/exclude, temporary logging setup - no changes here) ...

    # --- Echoing received parameters from CLI (for verification) ---
    if core.log_level in ["INFO", "DEBUG"]:
        # ... (existing click.echo calls for parameters - no changes) ...
        click.echo("CLI: --- Core Processing (File Traversal) ---")


    processed_items_generator = core.process_directory_recursive(
        base_dir_path=directory,
        include_patterns=parsed_include_patterns,
        exclude_patterns=parsed_exclude_patterns,
        no_default_ignore=no_default_ignore,
        max_depth=max_depth,
        follow_symlinks=follow_symlinks,
        max_size_kb=max_size, # Pass the CLI option value
        ignore_read_errors=ignore_errors # Pass the CLI option value
    )

    # --- Build the digest tree from processed items ---
    # Note: This consumes the generator. If you need to iterate it multiple times, convert to list first.
    if core.log_level in ["INFO", "DEBUG"]:
        click.echo(f"CLI: Building digest tree...")
    
    # We need to collect items if we want to print them before building tree
    # For now, build_digest_tree consumes the generator directly
    # collected_items = list(processed_items_generator) # If you need to inspect before tree building
    # root_node, metadata_from_core = core.build_digest_tree(directory, iter(collected_items))

    root_node, metadata_from_core = core.build_digest_tree(directory, processed_items_generator)

    if core.log_level in ["INFO", "DEBUG"]:
        click.echo(f"CLI: Digest tree built. Root node children: {len(root_node.get('children',[]))}")
        click.echo(f"CLI: Metadata from core: {metadata_from_core}")

    # --- Placeholder for actual output generation (Phase 4) ---
    # This is where formatters will be called with root_node and metadata_from_core
    # For now, let's just print a representation of the tree if verbose
    if core.log_level == "DEBUG": # Only for deep debugging
        import json
        click.echo("CLI: --- Generated Data Tree (Debug) ---")
        click.echo(json.dumps(root_node, indent=2, default=lambda o: '<not serializable>'))
        click.echo("CLI: --- End Generated Data Tree ---")


    if output != sys.stdout and core.log_level in ["INFO", "DEBUG"]:
        click.echo(f"CLI: Digest would be written to {output.name}")

# ... (if __name__ == '__main__':) ...
```
**Changes in `cli.py`:**
*   Passed `max_size` (as `max_size_kb`) and `ignore_errors` (as `ignore_read_errors`) to `core.process_directory_recursive`.
*   Added a call to `core.build_digest_tree` after the generator is created. This consumes the generator.
*   Added some CLI logging around the tree building.
*   Added a `DEBUG`-level conditional print of the generated JSON tree for verification.

**Verification for Phase 3:**

1.  Ensure your virtual environment is active and the package is up-to-date (`uv pip install -e .`).
2.  Use your `my_test_dir` or the `temp_dir_structure` from `conftest.py`. Make sure it includes:
    *   Small text files.
    *   A large file (e.g., > 300KB, or adjust `--max-size` for testing). Name it `large_file.txt`.
        ```bash
        # Example to create a large file of approx 350KB
        python -c "with open('my_test_dir/large_file.txt', 'w') as f: f.write('A' * (350 * 1024))"
        ```
    *   A file that might cause a read error (e.g., a binary file you try to read as text, or a file with restricted permissions if you can create one).
        ```bash
        # Example for a pseudo-binary file (UTF-16 with BOM, might cause issues if read as plain UTF-8 without 'replace')
        # python -c "with open('my_test_dir/pseudo_binary.bin', 'wb') as f: f.write(b'\xff\xfeA\x00B\x00C\x00')"
        # Or a file with mixed encodings.
        ```
3.  Test various scenarios:
    *   `dirdigest ./my_test_dir/` (default max size 300KB)
    *   `dirdigest ./my_test_dir/ -vv` (to see the DEBUG JSON tree output)
    *   `dirdigest ./my_test_dir/ --max-size 1` (should skip most files, including `large_file.txt`)
    *   `dirdigest ./my_test_dir/ --max-size 500` (should include `large_file.txt` if it's ~350KB)
    *   If you have a file that causes read errors:
        *   `dirdigest ./my_test_dir/ -i "pseudo_binary.bin"` (observe error handling, it should be skipped by default if error occurs)
        *   `dirdigest ./my_test_dir/ -i "pseudo_binary.bin" --ignore-errors` (should be included in tree but with `content: null` and a `read_error` field)

    Observe the logs:
    *   Skipping files due to size.
    *   Errors during file reading (and if they are ignored or cause the file to be skipped).
    *   The structure of the JSON tree printed with `-vv`. It should be a nested dictionary.

This phase is a big step! We now have the core logic for selecting files and preparing their data for output. The next phase will be to actually format this data into JSON and Markdown.

Ready for Phase 4 when you are!