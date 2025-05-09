# promptbuilder/context.py
import logging
import os  # <--- Import the os module
from pathlib import Path
from typing import List, Optional, Tuple, Set

from .config import Config

logger = logging.getLogger(__name__)

# ContextInfo still holds (path_string, content)
ContextInfo = Tuple[str, Optional[str]]

def parse_context_paths(
    paths: List[str],
    config: Config,
    verbose_level: int = 0
) -> Tuple[List[ContextInfo], int, int]:
    """
    Parses context paths (files/directories), applying configuration limits.
    Uses absolute paths for processing but returns relative paths for display.

    Returns:
        Tuple containing:
        - List of ContextInfo tuples: (relative_path_string, content_or_summary).
        - Total number of files processed internally.
        - Total number of files skipped.
    """
    context_items: List[ContextInfo] = []
    processed_files = 0
    skipped_files = 0
    max_bytes = int(config.context_max_file_size_mb * 1024 * 1024)
    supported_ext_set = set(config.context_supported_extensions)
    processed_paths: Set[Path] = set() # Keep track of canonical paths to avoid duplicates
    files_to_process: List[Path] = []
    cwd = Path.cwd() # <--- Get Current Working Directory once

    if not paths:
        return [], 0, 0

    # 1. Collect all potential files using absolute paths for reliability
    for path_str in paths:
        # Resolve input path relative to CWD if it's not absolute already
        input_path = Path(path_str)
        try:
            # Resolve symlinks and make absolute
            absolute_path = input_path.resolve(strict=True)
        except FileNotFoundError:
             logger.warning(f"Context path not found: {path_str}")
             skipped_files += 1
             continue
        except Exception as e:
             logger.error(f"Error resolving path {path_str}: {e}")
             skipped_files += 1
             continue


        if not absolute_path.exists(): # Should be redundant after resolve(strict=True) but safe check
            logger.warning(f"Context path resolved but does not exist: {absolute_path} (from {path_str})")
            skipped_files += 1
            continue

        if absolute_path in processed_paths:
             logger.debug(f"Skipping already processed path: {path_str} (resolved: {absolute_path})")
             continue

        if absolute_path.is_file():
            files_to_process.append(absolute_path)
            processed_paths.add(absolute_path)
        elif absolute_path.is_dir():
            logger.info(f"Recursively searching directory: {path_str} (resolved: {absolute_path})")
            try:
                for item in absolute_path.rglob('*'):
                    try:
                        item_resolved = item.resolve(strict=True) # Resolve items found during iteration
                        if item_resolved in processed_paths:
                            continue
                        if item.is_file(): # Check original item type before resolving
                            files_to_process.append(item_resolved)
                            processed_paths.add(item_resolved)
                        # else: ignore subdirectories explicitly found by rglob
                    except Exception as e:
                         logger.warning(f"Skipping item within directory {absolute_path} due to resolve error: {item} ({e})")
                         skipped_files += 1 # Count unresolvable items as skipped

            except OSError as e:
                 logger.error(f"Error scanning directory {absolute_path}: {e}")
                 skipped_files+=1 # Consider dir scan error as skipped potential files


    # 2. Process collected absolute file paths
    for file_path in files_to_process: # file_path is an absolute Path object
        processed_files += 1

        # --- Calculate relative path for display ---
        try:
            # Create path relative to the current working directory
            relative_display_path = os.path.relpath(file_path, cwd)
        except ValueError as e:
            # This might happen if paths are on different drives (Windows)
            logger.warning(f"Could not determine relative path for {file_path} relative to {cwd}: {e}. Using absolute path for display.")
            relative_display_path = str(file_path) # Fallback to absolute path string

        logger.debug(f"Processing context file: {file_path} (displaying as: {relative_display_path})")

        # Check extension (use absolute path's suffix)
        if file_path.suffix.lower() not in supported_ext_set:
            if verbose_level > 0:
                # Log with the path the user will see (relative)
                logger.info(f"Skipping file (unsupported extension {file_path.suffix}): {relative_display_path}")
            skipped_files += 1
            continue

        # Check size (use absolute path's stat)
        try:
            file_size = file_path.stat().st_size
            if file_size > max_bytes:
                logger.warning(f"Skipping file (size {file_size / (1024*1024):.2f} MB > limit {config.context_max_file_size_mb} MB): {relative_display_path}")
                skipped_files += 1
                continue
            if file_size == 0:
                 logger.info(f"Including empty file: {relative_display_path}")
                 # --- Store relative path in results ---
                 context_items.append((relative_display_path, ""))
                 continue

        except OSError as e:
            logger.error(f"Error accessing file metadata {relative_display_path}: {e}")
            skipped_files += 1
            continue

        # Read content (use absolute path's read_text)
        try:
            content = file_path.read_text(encoding=config.context_encoding)
            # --- Store relative path in results ---
            context_items.append((relative_display_path, content))
            if verbose_level > 1:
                 logger.debug(f"Successfully read content from: {relative_display_path}")
        except UnicodeDecodeError:
            logger.warning(f"Skipping file (encoding error with '{config.context_encoding}'): {relative_display_path}")
            skipped_files += 1
        except IOError as e:
            logger.error(f"Error reading file {relative_display_path}: {e}")
            skipped_files += 1

    # Calculate total attempted *after* initial collection and resolution attempts
    total_processed_after_collection = len(files_to_process)
    actual_included = len(context_items)

    if verbose_level > 0:
         # Report based on files actually attempted for reading after collection/filtering
         logger.info(f"Context processing summary: Attempted reads={total_processed_after_collection}, Included={actual_included}, Skipped (filter/read error)={skipped_files}")

    # Return list of (relative_path_str, content) tuples
    return context_items, total_processed_after_collection, skipped_files # Return count of files attempted reads