# dirdigest/dirdigest/core.py
import os
import pathlib
from typing import Any, Generator, Tuple, List, Dict

from dirdigest.constants import DEFAULT_IGNORE_PATTERNS
from dirdigest.utils.patterns import matches_patterns, is_path_hidden
from dirdigest.utils.logger import logger  # Import the configured logger

# Type hints for clarity
DigestItemNode = Dict[str, Any]
ProcessedItemPayload = Dict[str, Any]
ProcessedItem = Tuple[pathlib.Path, str, ProcessedItemPayload]
TraversalStats = Dict[str, int]


def process_directory_recursive(
    base_dir_path: pathlib.Path,
    include_patterns: List[str],
    exclude_patterns: List[str],
    no_default_ignore: bool,
    max_depth: int | None,
    follow_symlinks: bool,
    max_size_kb: int,
    ignore_read_errors: bool,
) -> Tuple[Generator[ProcessedItem, None, None], TraversalStats]:
    """
    Recursively traverses a directory, filters files and folders,
    and yields processed file items along with collected traversal statistics.
    """
    stats: TraversalStats = {
        "included_files_count": 0,
        "excluded_items_count": 0,
    }

    max_size_bytes = max_size_kb * 1024
    effective_exclude_patterns = list(
        exclude_patterns
    )  # Start with user-defined excludes
    if not no_default_ignore:
        effective_exclude_patterns.extend(DEFAULT_IGNORE_PATTERNS)

    logger.debug(
        f"Core: Effective exclude patterns count: {len(effective_exclude_patterns)}"
    )
    logger.debug(
        f"Core: Max size KB: {max_size_kb}, Ignore read errors: {ignore_read_errors}"
    )
    logger.debug(
        f"Core: Follow symlinks: {follow_symlinks}, No default ignore: {no_default_ignore}"
    )

    def _traverse() -> Generator[ProcessedItem, None, None]:
        """Nested generator function to handle the actual traversal and yielding."""
        for root, dirs_orig, files_orig in os.walk(
            str(base_dir_path), topdown=True, followlinks=follow_symlinks
        ):
            current_root_path = pathlib.Path(root)
            relative_root_path = current_root_path.relative_to(base_dir_path)
            current_depth = (
                len(relative_root_path.parts)
                if relative_root_path != pathlib.Path(".")
                else 0
            )
            logger.debug(
                f"Walking: [log.path]{current_root_path}[/log.path], "
                f"Rel: [log.path]{relative_root_path}[/log.path], Depth: {current_depth}"
            )

            # --- Depth Filtering ---
            if max_depth is not None and current_depth >= max_depth:
                logger.info(
                    f"Max depth ({max_depth}) reached at [log.path]{relative_root_path}[/log.path], "
                    f"pruning its {len(dirs_orig)} subdirectories."
                )
                if dirs_orig:
                    stats["excluded_items_count"] += len(dirs_orig)
                    for pruned_dir_name in dirs_orig:
                        logger.debug(
                            f"[log.excluded]Excluded (due to depth)[/log.excluded]: "
                            f"[log.path]{relative_root_path / pruned_dir_name}[/log.path] "
                            f"([log.reason]Exceeds max depth[/log.reason])"
                        )
                dirs_orig[:] = []  # Prevent descent

            # --- Directory Filtering ---
            dirs_to_traverse_next = []
            for dir_name in dirs_orig:
                dir_path_obj = current_root_path / dir_name
                relative_dir_path = relative_root_path / dir_name
                relative_dir_path_str = str(relative_dir_path)
                reason_dir_excluded = ""

                if not follow_symlinks and dir_path_obj.is_symlink():
                    reason_dir_excluded = "Is a symlink (symlink following disabled)"
                elif is_path_hidden(relative_dir_path) and not no_default_ignore:
                    reason_dir_excluded = "Is a hidden directory"
                elif matches_patterns(
                    relative_dir_path_str, effective_exclude_patterns
                ):
                    reason_dir_excluded = (
                        "Matches an exclude pattern"  # TODO: Log which pattern
                    )

                if reason_dir_excluded:
                    logger.info(
                        f"[log.excluded]Excluded directory[/log.excluded]: "
                        f"[log.path]{relative_dir_path_str}[/log.path] "
                        f"([log.reason]{reason_dir_excluded}[/log.reason])"
                    )
                    stats["excluded_items_count"] += 1
                    continue
                dirs_to_traverse_next.append(dir_name)
            dirs_orig[:] = dirs_to_traverse_next

            # --- File Filtering and Content Reading ---
            for file_name in files_orig:
                file_path_obj = current_root_path / file_name
                relative_file_path = relative_root_path / file_name
                relative_file_path_str = str(relative_file_path)
                file_attributes: ProcessedItemPayload = {}
                reason_file_excluded = ""

                # Determine exclusion reason
                if not follow_symlinks and file_path_obj.is_symlink():
                    reason_file_excluded = "Is a symlink (symlink following disabled)"
                elif is_path_hidden(relative_file_path) and not no_default_ignore:
                    reason_file_excluded = "Is a hidden file"
                elif matches_patterns(
                    relative_file_path_str, exclude_patterns
                ):  # User excludes
                    reason_file_excluded = "Matches user-specified exclude pattern"  # TODO: specific pattern
                elif not no_default_ignore and matches_patterns(
                    relative_file_path_str, DEFAULT_IGNORE_PATTERNS  # Default excludes
                ):
                    reason_file_excluded = (
                        "Matches default ignore pattern"  # TODO: specific pattern
                    )
                elif include_patterns and not matches_patterns(
                    relative_file_path_str, include_patterns  # User includes
                ):
                    reason_file_excluded = "Does not match any include pattern"

                if reason_file_excluded:
                    logger.info(
                        f"[log.excluded]Excluded file[/log.excluded]: "
                        f"[log.path]{relative_file_path_str}[/log.path] "
                        f"([log.reason]{reason_file_excluded}[/log.reason])"
                    )
                    stats["excluded_items_count"] += 1
                    continue

                # Attempt to process file if not excluded by patterns
                try:
                    file_stat = file_path_obj.stat()  # Stat once
                    file_size_bytes = file_stat.st_size
                    actual_size_kb = round(file_size_bytes / 1024, 3)
                    file_attributes["size_kb"] = actual_size_kb

                    if file_size_bytes > max_size_bytes:
                        reason_max_size = f"Exceeds max size ({actual_size_kb:.1f}KB > {max_size_kb}KB)"
                        logger.info(
                            f"[log.excluded]Excluded file[/log.excluded]: "
                            f"[log.path]{relative_file_path_str}[/log.path] "
                            f"([log.reason]{reason_max_size}[/log.reason])"
                        )
                        stats["excluded_items_count"] += 1
                        continue

                    logger.debug(
                        f"    Reading content for: [log.path]{relative_file_path_str}[/log.path]"
                    )
                    with open(
                        file_path_obj, "r", encoding="utf-8", errors="strict"
                    ) as f:
                        file_attributes["content"] = f.read()
                    file_attributes["read_error"] = None

                except OSError as e:
                    logger.warning(
                        f"Read error for [log.path]{relative_file_path_str}[/log.path]: {e}"
                    )
                    if not ignore_read_errors:
                        reason_os_error = (
                            f"OS read error (and ignore_errors=False): {e}"
                        )
                        logger.info(
                            f"[log.excluded]Excluded file[/log.excluded]: "
                            f"[log.path]{relative_file_path_str}[/log.path] "
                            f"([log.reason]{reason_os_error}[/log.reason])"
                        )
                        stats["excluded_items_count"] += 1
                        continue
                    file_attributes["content"] = None
                    file_attributes["read_error"] = str(e)
                    if "size_kb" not in file_attributes:  # if stat() also failed
                        try:
                            file_attributes["size_kb"] = round(
                                file_path_obj.stat().st_size / 1024, 3
                            )
                        except OSError:
                            file_attributes["size_kb"] = 0.0

                except UnicodeDecodeError as e:
                    logger.warning(
                        f"Unicode decode error for [log.path]{relative_file_path_str}[/log.path]. "
                        f"File may be binary or use an unexpected encoding."
                    )
                    if not ignore_read_errors:
                        reason_unicode_error = (
                            f"UnicodeDecodeError (and ignore_errors=False): {e}"
                        )
                        logger.info(
                            f"[log.excluded]Excluded file[/log.excluded]: "
                            f"[log.path]{relative_file_path_str}[/log.path] "
                            f"([log.reason]{reason_unicode_error}[/log.reason])"
                        )
                        stats["excluded_items_count"] += 1
                        continue
                    file_attributes["content"] = None
                    file_attributes["read_error"] = f"UnicodeDecodeError: {e}"
                    if "size_kb" not in file_attributes:  # if stat() failed
                        try:
                            file_attributes["size_kb"] = round(
                                file_path_obj.stat().st_size / 1024, 3
                            )
                        except OSError:
                            file_attributes["size_kb"] = 0.0

                # If all checks passed and content (or error placeholder) is ready
                logger.info(
                    f"[log.included]Included file[/log.included]: "
                    f"[log.path]{relative_file_path_str}[/log.path] "
                    f"(Size: {file_attributes.get('size_kb', 0):.1f}KB)"
                )
                stats["included_files_count"] += 1
                yield (relative_file_path, "file", file_attributes)

        logger.debug(
            f"Core _traverse generator finished. Final stats collected by _traverse: {stats}"
        )

    return _traverse(), stats


def build_digest_tree(
    base_dir_path: pathlib.Path,
    processed_items_generator: Generator[ProcessedItem, None, None],
    initial_stats: TraversalStats,
) -> Tuple[DigestItemNode, Dict[str, Any]]:
    """
    Builds the hierarchical tree structure from the flat list of processed file items
    and combines traversal statistics into final metadata.
    """
    root_node: DigestItemNode = {"relative_path": ".", "type": "folder", "children": []}
    current_total_content_size_kb = 0.0

    for relative_path, item_type, attributes in processed_items_generator:
        # This function currently only processes "file" items from the generator
        # to build the tree. Directories are implicitly created.
        if item_type == "file":
            if attributes.get("size_kb") is not None:
                current_total_content_size_kb += attributes["size_kb"]

            parts = list(relative_path.parts)
            current_level_children = root_node["children"]
            current_path_so_far = pathlib.Path(".")

            # Create parent directory nodes as needed
            for i, part_name in enumerate(parts[:-1]):
                current_path_so_far = current_path_so_far / part_name
                folder_node = next(
                    (
                        child
                        for child in current_level_children
                        if child["relative_path"] == str(current_path_so_far)
                        and child["type"] == "folder"
                    ),
                    None,
                )
                if not folder_node:
                    folder_node = {
                        "relative_path": str(current_path_so_far),
                        "type": "folder",
                        "children": [],
                    }
                    current_level_children.append(folder_node)
                current_level_children = folder_node["children"]

            # Add the file node
            file_node: DigestItemNode = {
                "relative_path": str(relative_path),
                "type": "file",
                "size_kb": attributes.get("size_kb", 0.0),
            }
            if "content" in attributes:  # Content could be None
                file_node["content"] = attributes["content"]
            if attributes.get("read_error"):
                file_node["read_error"] = attributes["read_error"]

            current_level_children.append(file_node)

    def sort_children_recursive(node: DigestItemNode):
        """Sorts children of a node by relative_path for consistent output."""
        if node.get("type") == "folder" and "children" in node:
            node["children"].sort(key=lambda x: x["relative_path"])
            for child in node["children"]:
                sort_children_recursive(child)

    sort_children_recursive(root_node)

    # Prepare final metadata for output formatters
    final_metadata = {
        "base_directory": str(base_dir_path.resolve()),
        "included_files_count": initial_stats.get("included_files_count", 0),
        "excluded_files_count": initial_stats.get("excluded_items_count", 0),
        "total_content_size_kb": round(current_total_content_size_kb, 3),
    }
    logger.debug(f"build_digest_tree returning metadata: {final_metadata}")

    return root_node, final_metadata
