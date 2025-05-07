# promptbuilder/context.py
import logging
import os
from pathlib import Path
from typing import List, Optional, Tuple, Set

# Rich imports (only needed if direct printing is done here, logger handles most)
# from rich.console import Console

from .config import Config

# Use the logger configured in cli.py
logger = logging.getLogger(__name__)

ContextInfo = Tuple[str, Optional[str]]

def parse_context_paths(
    paths: List[str],
    config: Config,
    console: 'Console', # Type hint for console (forward reference)
    verbose_level: int = 0
) -> Tuple[List[ContextInfo], int, int]:
    """
    Parses context paths (files/directories), applying configuration limits.
    Uses absolute paths for processing but returns relative paths for display.

    Returns:
        Tuple containing:
        - List of ContextInfo tuples: (relative_path_string, content_or_summary).
        - Total number of files processed internally (attempted reads).
        - Total number of files skipped (filtered out or read errors).
    """
    context_items: List[ContextInfo] = []
    processed_files_count = 0 # Files actually read or attempted to read
    skipped_files_count = 0   # Files skipped due to filters, errors, not found etc.
    max_bytes = int(config.context_max_file_size_mb * 1024 * 1024)
    supported_ext_set = set(config.context_supported_extensions)
    # Use case-insensitive matching for extensions on case-insensitive filesystems like Windows
    is_case_insensitive_fs = os.path.normcase('A') == os.path.normcase('a')
    if is_case_insensitive_fs:
        supported_ext_set = {ext.lower() for ext in supported_ext_set}

    processed_real_paths: Set[Path] = set() # Keep track of canonical paths to avoid duplicates
    files_to_process: List[Tuple[Path, str]] = [] # Store (absolute_path, original_user_path_str)
    cwd = Path.cwd()

    if not paths:
        return [], 0, 0

    # 1. Collect all potential files using absolute paths for reliability
    for path_str in paths:
        input_path = Path(path_str)
        try:
            # Resolve symlinks and make absolute. strict=True raises error if not found.
            absolute_path = input_path.resolve(strict=True)
            # Use realpath to get the canonical path for duplicate checking
            real_path = absolute_path.resolve() # Or Path(os.path.realpath(absolute_path)) for older python? resolve should be enough.
        except FileNotFoundError:
             logger.warning(f"Context path not found: [yellow]{path_str}[/yellow]")
             skipped_files_count += 1
             continue
        except Exception as e:
             logger.error(f"Error resolving path [red]{path_str}[/red]: {e}")
             skipped_files_count += 1
             continue

        if real_path in processed_real_paths:
             logger.debug(f"Skipping already processed path: {path_str} (resolved: {absolute_path})")
             continue
        processed_real_paths.add(real_path) # Add the canonical path

        if absolute_path.is_file():
            files_to_process.append((absolute_path, path_str)) # Keep track of original input path string too
        elif absolute_path.is_dir():
            logger.info(f"Recursively searching directory: [blue]{path_str}[/blue] (resolved: {absolute_path})")
            try:
                items_in_dir = 0
                skipped_in_dir = 0
                # Use Path.rglob for robust recursive globbing
                for item in absolute_path.rglob('*'):
                    items_in_dir += 1
                    try:
                        # Check if item exists and is a file before resolving (performance)
                        if item.is_file():
                            item_resolved = item.resolve(strict=True) # Resolve items found during iteration
                            item_real_path = item_resolved.resolve()
                            if item_real_path not in processed_real_paths:
                                files_to_process.append((item_resolved, str(item))) # Use item path as 'original' here
                                processed_real_paths.add(item_real_path)
                            # else: ignore duplicate file found via recursive search
                        # else: ignore subdirectories explicitly found by rglob
                    except FileNotFoundError:
                        # File might have been deleted between rglob and resolve
                         logger.debug(f"Item no longer exists, skipping: {item}")
                         skipped_in_dir += 1
                         skipped_files_count += 1
                    except Exception as e:
                         logger.warning(f"Skipping item within directory [yellow]{absolute_path}[/yellow] due to resolve error: {item} ({e})")
                         skipped_in_dir += 1
                         skipped_files_count += 1
                if verbose_level > 0:
                    logger.info(f"Directory scan [blue]{path_str}[/blue]: Found {items_in_dir} items, skipped {skipped_in_dir} during scan.")

            except OSError as e:
                 logger.error(f"Error scanning directory [red]{absolute_path}[/red]: {e}")
                 # Hard to estimate how many files were missed, maybe add 1 skipped?
                 skipped_files_count +=1


    # 2. Process collected absolute file paths
    for file_path, original_path_str in files_to_process: # file_path is an absolute Path object
        processed_files_count += 1 # Increment for every file we attempt to process

        # --- Calculate relative path for display ---
        try:
            relative_display_path = os.path.relpath(file_path, cwd)
        except ValueError:
            # Fallback to absolute path string if relative path fails (e.g., different drives)
            logger.debug(f"Could not determine relative path for {file_path}. Using absolute path for display.")
            relative_display_path = str(file_path)

        logger.debug(f"Processing context file: {file_path} (displaying as: {relative_display_path})")

        # Check extension
        file_suffix = file_path.suffix
        check_suffix = file_suffix.lower() if is_case_insensitive_fs else file_suffix
        if check_suffix not in supported_ext_set:
            if verbose_level > 0:
                logger.info(f"Skipping file (unsupported extension '[dim]{file_suffix}[/dim]'): [yellow]{relative_display_path}[/yellow]")
            skipped_files_count += 1
            processed_files_count -= 1 # Don't count skipped files in the *processed* count
            continue

        # Check size
        try:
            file_size = file_path.stat().st_size
            if max_bytes > 0 and file_size > max_bytes: # Allow max_bytes=0 for no limit? Add config option?
                logger.warning(f"Skipping file (size {file_size / (1024*1024):.2f} MB > limit {config.context_max_file_size_mb} MB): [yellow]{relative_display_path}[/yellow]")
                skipped_files_count += 1
                processed_files_count -= 1 # Don't count skipped files in the *processed* count
                continue
            if file_size == 0:
                 logger.info(f"Including empty file: [dim]{relative_display_path}[/dim]")
                 context_items.append((relative_display_path, ""))
                 # processed_files_count remains incremented, it was processed.
                 continue

        except OSError as e:
            logger.error(f"Error accessing file metadata [red]{relative_display_path}[/red]: {e}")
            skipped_files_count += 1
            processed_files_count -= 1 # Don't count error files in the *processed* count
            continue

        # Read content
        try:
            content = file_path.read_text(encoding=config.context_encoding)
            # Store relative path in results
            context_items.append((relative_display_path, content))
            if verbose_level > 1:
                 logger.debug(f"Successfully read content from: [green]{relative_display_path}[/green]")
            # processed_files_count remains incremented
        except UnicodeDecodeError:
            logger.warning(f"Skipping file (encoding error with '[cyan]{config.context_encoding}[/cyan]'): [yellow]{relative_display_path}[/yellow]")
            skipped_files_count += 1
            processed_files_count -= 1
        except IOError as e:
            logger.error(f"Error reading file [red]{relative_display_path}[/red]: {e}")
            skipped_files_count += 1
            processed_files_count -= 1
        except Exception as e:
            logger.error(f"Unexpected error reading file [red]{relative_display_path}[/red]: {e}", exc_info=True)
            skipped_files_count += 1
            processed_files_count -= 1


    actual_included = len(context_items)
    # Adjust final counts: total_attempts is the size of files_to_process
    total_attempts = len(files_to_process)
    # Skipped count should reflect filters + errors encountered during processing phase
    # The initial skipped_files_count covers path resolution errors etc.
    final_skipped_count = skipped_files_count + (total_attempts - actual_included)

    if verbose_level > 0 or final_skipped_count > 0 : # Report summary if verbose or if files were skipped
         logger.info(f"Context processing summary: Files attempted={total_attempts}, Included=[green]{actual_included}[/green], Skipped=[yellow]{final_skipped_count}[/yellow]")

    # Return list of (relative_path_str, content) tuples
    # Return the count of files successfully included, and the count of files skipped
    return context_items, actual_included, final_skipped_count