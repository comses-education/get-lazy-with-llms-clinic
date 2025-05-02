import logging
from pathlib import Path
from typing import List, Optional, Tuple, Set

from .config import Config

logger = logging.getLogger(__name__)

# Using tuple (path_str, content_summary) for now. Content summary can be filename or content.
ContextInfo = Tuple[str, Optional[str]]

def parse_context_paths(
    paths: List[str],
    config: Config,
    verbose_level: int = 0
) -> Tuple[List[ContextInfo], int, int]:
    """
    Parses context paths (files/directories), applying configuration limits.

    Returns:
        Tuple containing:
        - List of ContextInfo tuples: (path_string, content_or_summary).
        - Total number of files processed.
        - Total number of files skipped.
    """
    context_items: List[ContextInfo] = []
    processed_files = 0
    skipped_files = 0
    max_bytes = int(config.context_max_file_size_mb * 1024 * 1024)
    supported_ext_set = set(config.context_supported_extensions)
    processed_paths: Set[Path] = set() # Keep track of canonical paths to avoid duplicates

    if not paths:
        return [], 0, 0

    files_to_process: List[Path] = []

    # 1. Collect all potential files
    for path_str in paths:
        path = Path(path_str).resolve() # Resolve to canonical path

        if not path.exists():
            logger.warning(f"Context path not found: {path_str}")
            skipped_files += 1 # Count non-existent paths as skipped
            continue

        if path in processed_paths:
             logger.debug(f"Skipping already processed path: {path_str}")
             continue

        if path.is_file():
            files_to_process.append(path)
            processed_paths.add(path)
        elif path.is_dir():
            logger.info(f"Recursively searching directory: {path_str}")
            for item in path.rglob('*'):
                 item_resolved = item.resolve()
                 if item_resolved in processed_paths:
                     continue
                 if item.is_file():
                     files_to_process.append(item_resolved)
                     processed_paths.add(item_resolved)
                 # else: ignore subdirectories explicitly found by rglob

    # 2. Process collected files
    for file_path in files_to_process:
        processed_files += 1
        display_path = str(file_path) # Use resolved path for display/summary
        logger.debug(f"Processing context file: {display_path}")

        # Check extension
        if file_path.suffix.lower() not in supported_ext_set:
            if verbose_level > 0:
                logger.info(f"Skipping file (unsupported extension {file_path.suffix}): {display_path}")
            skipped_files += 1
            continue

        # Check size
        try:
            file_size = file_path.stat().st_size
            if file_size > max_bytes:
                logger.warning(f"Skipping file (size {file_size / (1024*1024):.2f} MB > limit {config.context_max_file_size_mb} MB): {display_path}")
                skipped_files += 1
                continue
            if file_size == 0:
                 logger.info(f"Including empty file: {display_path}")
                 context_items.append((display_path, "")) # Include empty file marker
                 continue

        except OSError as e:
            logger.error(f"Error accessing file metadata {display_path}: {e}")
            skipped_files += 1
            continue

        # Read content (currently full content mode, limited by size check)
        # TODO: Implement other context_modes later (list, snippets)
        try:
            content = file_path.read_text(encoding=config.context_encoding)
            context_items.append((display_path, content))
            if verbose_level > 1:
                 logger.debug(f"Successfully read content from: {display_path}")
        except UnicodeDecodeError:
            logger.warning(f"Skipping file (encoding error with '{config.context_encoding}'): {display_path}")
            skipped_files += 1
        except IOError as e:
            logger.error(f"Error reading file {display_path}: {e}")
            skipped_files += 1

    total_processed = len(files_to_process) # Count of files attempted after initial collection
    actual_included = len(context_items)

    if verbose_level > 0:
         logger.info(f"Context processing summary: Attempted={total_processed}, Included={actual_included}, Skipped={skipped_files}")

    # Return list of (path_str, content) tuples
    return context_items, total_processed, skipped_files