Fantastic! Let's embark on **Phase 5: Logging and Reporting**.

This phase is all about enhancing the user experience by providing clear, informative, and visually appealing feedback during the tool's execution. We'll leverage the `rich` library for this.

**Key Requirements for Phase 5:**
*   Use `rich` for terminal output.
*   Properly implement verbosity levels (`-v`, `-vv`, `-q`).
*   Log included files (green) and excluded files/folders (red) with specific reasons.
*   Report summary statistics (total included/excluded counts, total size, execution time).
*   Implement `--log-file` option.
*   Display progress indicators for large directories (this might be a stretch goal for the first pass of Phase 5, depending on complexity, but we'll aim for it).

---

**Step 5.1: Setup Rich Logging (`cli.py` and new `utils/logging.py`)**

It's good practice to centralize logging setup. Let's create a new utility for it.

**1. Create `dirdigest/dirdigest/utils/logger.py`:**

```python
# dirdigest/dirdigest/utils/logger.py
import logging
import sys
from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme

# Global console instances
# Console for general CLI output (like the final digest if to stdout, or progress)
# Using force_terminal=None to let Rich decide based on environment.
# If output is piped, it won't use colors, which is good.
# However, for --output to a file, we might want explicit control if using console for other messages.
# For now, assume stdout_console is for main output, stderr_console for logs/errors.
stdout_console = Console(file=sys.stdout) 
stderr_console = Console(stderr=True, theme=Theme({
    "logging.level.debug": "dim cyan",
    "logging.level.info": "dim blue",
    "logging.level.warning": "magenta",
    "logging.level.error": "bold red",
    "logging.level.critical": "bold red reverse",
    "log.included": "green",
    "log.excluded": "red",
    "log.reason": "dim yellow",
    "log.path": "cyan",
    "log.summary_key": "bold",
    "log.summary_value_inc": "bold green",
    "log.summary_value_exc": "bold red",
    "log.summary_value_neutral": "bold blue",
}))

# Global logger instance
# We will configure this logger in setup_logging
logger = logging.getLogger("dirdigest")

def setup_logging(verbose_level: int, quiet: bool, log_file_path: str | None = None) -> None:
    """
    Configures logging for the application using RichHandler.

    :param verbose_level: 0 (default), 1 (-v for INFO), 2 (-vv for DEBUG)
    :param quiet: If True, suppresses console output below ERROR.
    :param log_file_path: Optional path to a file for logging.
    """
    log_level_name = "INFO" # Default
    if quiet:
        log_level_name = "ERROR"
    elif verbose_level >= 2:
        log_level_name = "DEBUG"
    elif verbose_level >= 1:
        log_level_name = "INFO"
    else: # Default if no -v and no -q
        log_level_name = "WARNING" # Default operation logs warnings and above

    logger.setLevel(log_level_name)
    
    # Remove any existing handlers to avoid duplicate logs if called multiple times (e.g. in tests)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()


    # --- Console Handler (Rich) ---
    # Only add console handler if not completely silenced or if a certain level is met
    # The RichHandler will respect the logger's level.
    # We control what gets to the console via the logger's level.
    # Quiet flag should mean only ERROR and CRITICAL go to console.
    
    # The RichHandler should always use the stderr_console we defined
    # Format for RichHandler can be simplified as Rich handles level styling
    # We can customize markup in messages themselves e.g. logger.info("[log.path]%s[/log.path]", path)
    console_handler = RichHandler(
        console=stderr_console,
        level=log_level_name, # Handler also has a level
        show_time=False,      # Keep logs concise
        show_path=False,      # Path is usually part of the message
        markup=True,          # Enable Rich markup in log messages
        rich_tracebacks=True, # Nicer tracebacks
        log_time_format="[%X]" # Example time format if show_time=True
    )
    # Example format string for the handler, if not relying on Rich's default level display
    # console_formatter = logging.Formatter(fmt="%(message)s", datefmt="[%X]")
    # console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # --- File Handler (if log_file_path is provided) ---
    if log_file_path:
        file_handler = logging.FileHandler(log_file_path, mode='w', encoding='utf-8')
        # File logs can be more verbose by default, or match console, or be configured
        file_handler.setLevel(logging.DEBUG) # Capture all levels in file by default
        
        # Use a more standard format for file logs
        file_formatter = logging.Formatter(
            fmt="%(asctime)s - %(levelname)-8s - %(name)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    # Ensure propagation is True if you have parent loggers, but for a simple app, not critical.
    # logger.propagate = False 

    if not quiet: # Only print this initial log if not in quiet mode
        logger.debug(f"Logging initialized. Console level: {log_level_name}, File logging: {'Enabled to ' + str(log_file_path) if log_file_path else 'Disabled'}")

# Example usage (will be used in other modules):
# from .logger import logger
# logger.debug("A debug message with [bold magenta]markup[/bold magenta]!")
# logger.info("An info message.")
# logger.warning("A warning.")
# logger.error("An error.")
```
*Self-correction/Refinements in `logger.py`*:
*   Created two `Console` instances: `stdout_console` (for main digest output if to stdout) and `stderr_console` (for logs). This helps separate concerns.
*   Defined a custom theme for `stderr_console` to pre-style log levels and custom tags.
*   `setup_logging` now configures a global `logger = logging.getLogger("dirdigest")`.
*   `RichHandler` is configured to use `stderr_console` and `markup=True`.
*   `FileHandler` setup is included if `log_file_path` is given, with a more traditional log format.
*   Removed `core.log_level` global variable; we'll use the standard `logging` module now.

**2. Update `dirdigest/dirdigest/cli.py` to use the new logger:**

```python
# dirdigest/dirdigest/cli.py
import click
import sys
import pathlib
import datetime
import time # For execution time

from dirdigest.constants import TOOL_NAME, TOOL_VERSION
from dirdigest import core
from dirdigest import formatter as dirdigest_formatter
from dirdigest.utils import logger as dirdigest_logger # Import the new logger setup

# ... (click command and options - no changes here) ...

def main_cli(
    directory: pathlib.Path,
    output: click.utils.LazyFile,
    format: str,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    max_size: int,
    max_depth: int | None,
    no_default_ignore: bool,
    follow_symlinks: bool,
    ignore_errors: bool,
    clipboard: bool,
    verbose: int, # This is Click's count for -v
    quiet: bool,
    log_file: pathlib.Path | None,
    config: pathlib.Path | None
):
    """
    dirdigest: Recursively processes directories and files,
    creating a structured digest in markdown or JSON format.
    """
    start_time = time.monotonic()

    # --- Setup Logging ---
    dirdigest_logger.setup_logging(verbose_level=verbose, quiet=quiet, log_file_path=log_file)
    log = dirdigest_logger.logger # Get the configured logger instance

    # --- Argument Parsing for include/exclude ---
    parsed_include_patterns = []
    for item in include:
        parsed_include_patterns.extend(p.strip() for p in item.split(',') if p.strip())

    parsed_exclude_patterns = []
    for item in exclude:
        parsed_exclude_patterns.extend(p.strip() for p in item.split(',') if p.strip())

    log.debug(f"CLI: Parsed include patterns: {parsed_include_patterns}")
    log.debug(f"CLI: Parsed exclude patterns: {parsed_exclude_patterns}")
    log.info(f"CLI: Processing directory: [log.path]{directory}[/log.path]")
    log.debug(f"CLI: Output to: {output.name if output != sys.stdout else 'stdout'}")
    log.debug(f"CLI: Format: {format}")
    # ... log other CLI params at DEBUG level if desired ...

    # --- Core Processing ---
    # The core module will also use dirdigest_logger.logger
    processed_items_generator, stats_from_core = core.process_directory_recursive(
        base_dir_path=directory,
        include_patterns=parsed_include_patterns,
        exclude_patterns=parsed_exclude_patterns,
        no_default_ignore=no_default_ignore,
        max_depth=max_depth,
        follow_symlinks=follow_symlinks,
        max_size_kb=max_size,
        ignore_read_errors=ignore_errors
    )

    log.info(f"CLI: Building digest tree...")
    
    # Pass the base_dir_path and the partial stats from core (which now includes excluded_count)
    # to build_digest_tree, which can then augment them for the final metadata.
    root_node, metadata_for_output = core.build_digest_tree(
        base_dir_path=directory, 
        processed_items_generator=processed_items_generator,
        initial_stats=stats_from_core # Pass stats from traversal
    )
    
    log.debug(f"CLI: Digest tree built. Root node children: {len(root_node.get('children',[]))}")
    log.debug(f"CLI: Metadata for output: {metadata_for_output}")


    # --- Actual Output Generation ---
    selected_formatter: dirdigest_formatter.BaseFormatter
    # metadata_for_output now contains included_files_count, total_content_size_kb, and excluded_files_count
    if format.lower() == 'json':
        selected_formatter = dirdigest_formatter.JsonFormatter(directory, metadata_for_output)
    elif format.lower() == 'markdown':
        selected_formatter = dirdigest_formatter.MarkdownFormatter(directory, metadata_for_output)
    else:
        log.error(f"CLI: Unknown format '{format}'. This should not happen due to Click.Choice.")
        # Fallback or error out; for now, let's assume Click prevents this.
        # If it did happen, you'd probably exit.
        return 

    log.info(f"CLI: Formatting output as {format.upper()}...")
    
    final_output_str = "" # Initialize
    try:
        final_output_str = selected_formatter.format(root_node)
        # Use the stdout_console for writing the main digest if it's going to stdout
        if output == sys.stdout:
            dirdigest_logger.stdout_console.print(final_output_str, end="") # end="" to avoid double newline if output has one
        else:
            output.write(final_output_str)
            # Log to stderr_console (via logger)
            log.info(f"CLI: Digest successfully written to [log.path]{output.name}[/log.path]")
    except Exception as e:
        log.error(f"CLI: Error during output formatting or writing: {e}", exc_info=True)
        final_output_str = f"Error generating output: {e}" 

    # --- Execution Time and Final Summary Statistics ---
    execution_time = time.monotonic() - start_time
    # These stats are now in metadata_for_output from build_digest_tree
    inc_count = metadata_for_output.get("included_files_count", 0)
    exc_count = metadata_for_output.get("excluded_files_count", 0) # Should be populated now
    total_size = metadata_for_output.get("total_content_size_kb", 0.0)

    # Log summary to stderr (via logger, which uses stderr_console)
    log.info("-" * 30 + " SUMMARY " + "-" * 30) # Use logger.info for consistent output handling
    log.info(f"[log.summary_key]Total files included:[/log.summary_key] [log.summary_value_inc]{inc_count}[/log.summary_value_inc]")
    log.info(f"[log.summary_key]Total items excluded (files/dirs):[/log.summary_key] [log.summary_value_exc]{exc_count}[/log.summary_value_exc]")
    log.info(f"[log.summary_key]Total content size:[/log.summary_key] [log.summary_value_neutral]{total_size:.2f} KB[/log.summary_value_neutral]")
    log.info(f"[log.summary_key]Execution time:[/log.summary_key] [log.summary_value_neutral]{execution_time:.2f} seconds[/log.summary_value_neutral]")
    log.info("-" * (60 + len(" SUMMARY ")))


    # --- Clipboard (Phase 6 - placeholder) ---
    if clipboard:
        if final_output_str and "Error generating output" not in final_output_str :
            log.debug("CLI: Clipboard copy would happen here.")
        # Actual clipboard copy will be added in Phase 6

    # --- Debug print for generated data tree (if -vv) ---
    if verbose >=2 : # Check verbose level for this debug output
        import json as json_debugger
        def json_default_serializer(obj):
            if isinstance(obj, pathlib.Path): return str(obj)
            return f"<not serializable: {type(obj).__name__}>"
        log.debug("CLI: --- Generated Data Tree (Debug from CLI) ---")
        try:
            log.debug(json_debugger.dumps(root_node, indent=2, default=json_default_serializer))
        except TypeError as e:
            log.debug(f"CLI: Error serializing data tree to JSON for debug: {e}")
        log.debug("CLI: --- End Generated Data Tree ---")

if __name__ == '__main__':
    main_cli()
```
*Changes in `cli.py`*:
*   Imported `time` and `dirdigest.utils.logger`.
*   Called `dirdigest_logger.setup_logging()` at the beginning.
*   Replaced all `click.echo` calls used for logging/feedback with `log.debug()`, `log.info()`, `log.error()`, etc., using Rich markup (e.g., `[log.path]...[/log.path]`).
*   The main digest output (if to `sys.stdout`) now uses `dirdigest_logger.stdout_console.print()` to ensure it's separate from log messages on stderr.
*   **Crucially**, `core.process_directory_recursive` will now need to return traversal statistics (like `excluded_items_count`).
*   **Crucially**, `core.build_digest_tree` will now take these initial stats and incorporate them into the final metadata.
*   Added execution time calculation and a final summary log section.

**Step 5.2: Implement Detailed Logging in `core.py` (and return stats)**

Modify `dirdigest/dirdigest/core.py` to use the new logger and return exclusion counts.

```python
# dirdigest/dirdigest/core.py
import os
import pathlib
from typing import Any, Generator, Tuple, List, Dict

from dirdigest.constants import DEFAULT_IGNORE_PATTERNS
from dirdigest.utils.patterns import matches_patterns, is_path_hidden
from dirdigest.utils.logger import logger # Import the configured logger

# Remove old log_level and log_* functions, use 'logger' instance now

# Type hints
DigestItemNode = Dict[str, Any] 
ProcessedItemPayload = Dict[str, Any]
ProcessedItem = Tuple[pathlib.Path, str, ProcessedItemPayload]
TraversalStats = Dict[str, int] # For included_files, excluded_items

def process_directory_recursive(
    base_dir_path: pathlib.Path,
    include_patterns: List[str],
    exclude_patterns: List[str],
    no_default_ignore: bool,
    max_depth: int | None,
    follow_symlinks: bool,
    max_size_kb: int,
    ignore_read_errors: bool
) -> Tuple[Generator[ProcessedItem, None, None], TraversalStats]: # Now returns stats
    
    # Stats to be collected during traversal
    stats: TraversalStats = {
        "included_files_count": 0, # Specifically files successfully prepared for digest
        "excluded_items_count": 0  # Files and directories skipped
    }

    max_size_bytes = max_size_kb * 1024
    effective_exclude_patterns = list(exclude_patterns)
    if not no_default_ignore:
        effective_exclude_patterns.extend(DEFAULT_IGNORE_PATTERNS)
    
    # Using a nested function for the generator part to easily manage stats
    def _traverse() -> Generator[ProcessedItem, None, None]:
        for root, dirs_orig, files_orig in os.walk(str(base_dir_path), topdown=True, followlinks=follow_symlinks):
            current_root_path = pathlib.Path(root)
            relative_root_path = current_root_path.relative_to(base_dir_path)
            current_depth = len(relative_root_path.parts)
            if relative_root_path == pathlib.Path("."): current_depth = 0
            logger.debug(f"Walking: [log.path]{current_root_path}[/log.path], Rel: [log.path]{relative_root_path}[/log.path], Depth: {current_depth}")

            if max_depth is not None and current_depth >= max_depth:
                logger.info(f"Max depth ({max_depth}) reached at [log.path]{relative_root_path}[/log.path], pruning further subdirectory traversal.")
                if dirs_orig: # If there were dirs to prune
                    stats["excluded_items_count"] += len(dirs_orig) # Count pruned dirs
                    logger.debug(f"Pruned {len(dirs_orig)} subdirectories due to max_depth.")
                dirs_orig[:] = []
            
            dirs_to_traverse_next = []
            for dir_name in dirs_orig:
                dir_path_obj = current_root_path / dir_name
                relative_dir_path = relative_root_path / dir_name
                relative_dir_path_str = str(relative_dir_path)
                reason = ""
                
                if not follow_symlinks and dir_path_obj.is_symlink():
                    reason = "Is a symlink (symlink following disabled)"
                elif is_path_hidden(relative_dir_path) and not no_default_ignore:
                    reason = "Is a hidden directory"
                elif matches_patterns(relative_dir_path_str, effective_exclude_patterns):
                    reason = "Matches exclude pattern" # TODO: Log which pattern
                
                if reason:
                    logger.info(f"[log.excluded]Excluded directory[/log.excluded]: [log.path]{relative_dir_path_str}[/log.path] ([log.reason]{reason}[/log.reason])")
                    stats["excluded_items_count"] += 1
                    continue
                dirs_to_traverse_next.append(dir_name)
            dirs_orig[:] = dirs_to_traverse_next

            for file_name in files_orig:
                file_path_obj = current_root_path / file_name
                relative_file_path = relative_root_path / file_name
                relative_file_path_str = str(relative_file_path)
                file_attributes: ProcessedItemPayload = {}
                reason = ""
                
                if not follow_symlinks and file_path_obj.is_symlink():
                    reason = "Is a symlink (symlink following disabled)"
                elif is_path_hidden(relative_file_path) and not no_default_ignore:
                    reason = "Is a hidden file"
                elif matches_patterns(relative_file_path_str, effective_exclude_patterns):
                    reason = "Matches an exclude pattern" # TODO: Log which pattern
                elif include_patterns and not matches_patterns(relative_file_path_str, include_patterns):
                    reason = "Does not match any include patterns"
                
                if reason:
                    logger.info(f"[log.excluded]Excluded file[/log.excluded]: [log.path]{relative_file_path_str}[/log.path] ([log.reason]{reason}[/log.reason])")
                    stats["excluded_items_count"] += 1
                    continue

                try:
                    file_size_bytes = file_path_obj.stat().st_size
                    actual_size_kb = round(file_size_bytes / 1024, 3)
                    file_attributes["size_kb"] = actual_size_kb

                    if file_size_bytes > max_size_bytes:
                        reason = f"Exceeds max size ({actual_size_kb:.1f}KB > {max_size_kb}KB)"
                        logger.info(f"[log.excluded]Excluded file[/log.excluded]: [log.path]{relative_file_path_str}[/log.path] ([log.reason]{reason}[/log.reason])")
                        stats["excluded_items_count"] += 1
                        continue
                    
                    with open(file_path_obj, 'r', encoding='utf-8', errors='strict') as f:
                        file_attributes["content"] = f.read()
                    file_attributes["read_error"] = None
                except OSError as e:
                    reason = f"OS error reading file: {e}"
                    logger.warning(f"Read error for [log.path]{relative_file_path_str}[/log.path]: {e}")
                    if not ignore_read_errors:
                        logger.info(f"[log.excluded]Excluded file[/log.excluded]: [log.path]{relative_file_path_str}[/log.path] ([log.reason]OS read error, ignore_errors=False[/log.reason])")
                        stats["excluded_items_count"] += 1
                        continue
                    file_attributes["content"] = None
                    file_attributes["read_error"] = str(e)
                    if "size_kb" not in file_attributes: file_attributes["size_kb"] = 0.0
                except UnicodeDecodeError as e:
                    reason = f"Unicode decode error: {e}"
                    logger.warning(f"Unicode decode error for [log.path]{relative_file_path_str}[/log.path]. File may be binary.")
                    if not ignore_read_errors:
                        logger.info(f"[log.excluded]Excluded file[/log.excluded]: [log.path]{relative_file_path_str}[/log.path] ([log.reason]UnicodeDecodeError, ignore_errors=False[/log.reason])")
                        stats["excluded_items_count"] += 1
                        continue
                    file_attributes["content"] = None
                    file_attributes["read_error"] = f"UnicodeDecodeError: {e}"
                    if "size_kb" not in file_attributes:
                        try: file_attributes["size_kb"] = round(file_path_obj.stat().st_size / 1024, 3)
                        except OSError: file_attributes["size_kb"] = 0.0
                
                logger.info(f"[log.included]Included file[/log.included]: [log.path]{relative_file_path_str}[/log.path] (Size: {file_attributes.get('size_kb', 0):.1f}KB)")
                stats["included_files_count"] += 1
                yield (relative_file_path, "file", file_attributes)
        
        # After loop finishes
        logger.debug(f"Core traversal finished. Stats: {stats}")
        # The generator itself doesn't directly return stats, its enclosing function does.

    return _traverse(), stats # Return the generator and the collected stats


def build_digest_tree(
    base_dir_path: pathlib.Path,
    processed_items_generator: Generator[ProcessedItem, None, None], # Renamed for clarity
    initial_stats: TraversalStats # New argument for stats from traversal
) -> Tuple[DigestItemNode, Dict[str, Any]]: # Returns final metadata
    
    root_node: DigestItemNode = {"relative_path": ".", "type": "folder", "children": []}
    
    # Statistics for metadata - start with those from traversal
    # included_files_count is already tallied by process_directory_recursive for *yielded* files
    # total_content_size_kb will be calculated from yielded items here.
    current_total_content_size_kb = 0.0

    for relative_path, item_type, attributes in processed_items_generator:
        if item_type == "file":
            # included_files_count already incremented by producer for yielded files
            if attributes.get("size_kb"):
                current_total_content_size_kb += attributes["size_kb"]
            # ... (rest of the tree building logic for file_node - no changes) ...
            parts = list(relative_path.parts)
            current_level_children = root_node["children"]
            current_path_so_far = pathlib.Path(".") 

            for i, part_name in enumerate(parts[:-1]): 
                current_path_so_far = current_path_so_far / part_name
                folder_node = next((child for child in current_level_children if child["relative_path"] == str(current_path_so_far) and child["type"] == "folder"), None)
                if not folder_node:
                    folder_node = {
                        "relative_path": str(current_path_so_far),
                        "type": "folder",
                        "children": []
                    }
                    current_level_children.append(folder_node)
                current_level_children = folder_node["children"]
            
            file_node: DigestItemNode = {
                "relative_path": str(relative_path),
                "type": "file",
                "size_kb": attributes.get("size_kb", 0.0),
            }
            if "content" in attributes : 
                file_node["content"] = attributes["content"]
            if attributes.get("read_error"):
                file_node["read_error"] = attributes["read_error"]
            if attributes.get("skipped_reason"): 
                file_node["skipped_reason"] = attributes["skipped_reason"]
            current_level_children.append(file_node)

    def sort_children_recursive(node: DigestItemNode):
        if node["type"] == "folder" and "children" in node:
            node["children"].sort(key=lambda x: x["relative_path"])
            for child in node["children"]:
                sort_children_recursive(child)
    sort_children_recursive(root_node)

    # Combine initial_stats with calculated stats
    final_metadata = {
        "base_directory": str(base_dir_path.resolve()),
        "included_files_count": initial_stats.get("included_files_count", 0),
        "excluded_items_count": initial_stats.get("excluded_items_count", 0), # Use from traversal
        "total_content_size_kb": round(current_total_content_size_kb, 3)
    }
    
    return root_node, final_metadata
```
*Changes in `core.py`*:
*   Removed old global `log_level` and print-based log functions. Imported and now uses the `logger` from `dirdigest.utils.logger`.
*   All `print()` calls for logging replaced with `logger.debug()`, `logger.info()`, `logger.warning()`, using Rich markup tags defined in the `stderr_console`'s theme (e.g., `[log.included]`, `[log.path]`, `[log.reason]`).
*   `process_directory_recursive` now initializes and updates a `stats` dictionary (`included_files_count`, `excluded_items_count`).
*   It now returns a tuple: `(generator_function_call, stats)`. The actual generator is created by calling `_traverse()`.
*   Logging for excluded files/dirs now includes the reason, using the new Rich tags.
*   `build_digest_tree` now accepts `initial_stats` (from `process_directory_recursive`) and uses them to populate `excluded_items_count` in the `final_metadata`. It still calculates `total_content_size_kb` from the yielded items. `included_files_count` also comes from `initial_stats`.

**Step 5.3 & 5.4 (Summary Stats, Log File, Progress):**
*   Summary statistics logging is now implemented in `cli.py` using the logger and the metadata returned.
*   Log file support is integrated into `utils/logger.py` and enabled via `cli.py`.
*   Progress Indicator: This is a more involved Rich feature. We'll add a basic placeholder for now and can enhance it later if time permits or as a separate step.
    For a simple progress, you might count total files first (if feasible without too much overhead) or just show a spinner. `rich.progress.track` is easy for iterables.

**Placeholder for Progress in `cli.py` (Optional for now):**
If `processed_items_generator` was a list, you could do:
```python
# In cli.py, before the loop that consumes processed_items_generator for build_digest_tree
# from rich.progress import track
# collected_items = list(processed_items_generator) # Consume generator into a list
# if not quiet and output != sys.stdout: # Only show progress if not quiet and not piping digest
#    processed_for_tree = track(collected_items, description="Building structure...", console=dirdigest_logger.stderr_console)
# else:
#    processed_for_tree = iter(collected_items)
# root_node, metadata_from_core = core.build_digest_tree(directory, processed_for_tree, stats_from_core)
```
However, `process_directory_recursive` returns the generator and stats separately now. The generator should be consumed by `build_digest_tree`. A progress bar would ideally wrap the *traversal itself* inside `core.py`. This is more complex. Let's skip interactive progress for this iteration and focus on the logging.

**Verification for Phase 5:**

1.  Run `dirdigest ./my_test_dir/`. Observe:
    *   Default log level (WARNINGS and above on console).
    *   Final summary statistics printed to stderr.
2.  Run `dirdigest ./my_test_dir/ -v`. Observe:
    *   INFO level logs (included/excluded files in color with reasons).
    *   Final summary.
3.  Run `dirdigest ./my_test_dir/ -vv`. Observe:
    *   DEBUG level logs (more detailed, e.g., "Walking..." lines).
    *   Final summary.
4.  Run `dirdigest ./my_test_dir/ -q`. Observe:
    *   Only ERROR level logs (if any occur) and the final digest (if to stdout). No summary stats on console.
5.  Run `dirdigest ./my_test_dir/ -v --log-file app.log`.
    *   Check `app.log`. It should contain DEBUG level logs by default (as configured in `utils/logger.py` for the file handler) with timestamps and detailed formatting.
    *   Console output should still respect `-v`.
6.  Test with errors (e.g., `pseudo_binary.bin` without `--ignore-errors`). Ensure warnings/errors are logged correctly.

This is a big update. Let me know how the tests go! We're making `dirdigest` much more user-friendly.