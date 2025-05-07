# src/dirdigest/core.py (Removed redundant formatting log message)

import logging
from pathlib import Path
from typing import List, Optional, Tuple

from .filtering import PathFilter
from .formatting import format_json, format_markdown
from .models import DirectoryInfo, FileInfo, FileStatus, FileSystemItem

log = logging.getLogger(__name__)


# Statistics counters
class ProcessingStats:
    def __init__(self):
        # --- Counters ---
        self.files_included = 0
        self.files_excluded_default = 0
        self.files_excluded_user = 0
        self.files_excluded_size = 0
        self.files_excluded_include = 0
        self.files_excluded_output = 0
        self.files_skipped_permission = 0
        self.files_skipped_encoding = 0
        self.dirs_included = 0
        self.dirs_excluded = 0
        self.symlinks_skipped = 0
        # --- Path Lists (Restructured) ---
        self.included_folder_paths: List[str] = []
        self.included_file_paths: List[str] = []
        self.excluded_folder_paths: List[Tuple[str, str]] = [] # (path, reason)
        self.excluded_file_paths: List[Tuple[str, str]] = []   # (path, reason)

    def add_included_path(self, relative_path: str, is_dir: bool):
        """Records an included item's relative path."""
        if is_dir:
            self.included_folder_paths.append(relative_path)
        else:
            self.included_file_paths.append(relative_path)

    def add_excluded_path(self, relative_path: str, reason: str, is_dir: Optional[bool] = None):
        """Records an excluded item's relative path and reason."""
        # Increment specific counters based on reason
        # Note: Some counters are updated more accurately in _build_digest_structure
        if "output file" in reason:
            self.files_excluded_output += 1
        elif "size" in reason and not is_dir: # Only count size for files
            self.files_excluded_size += 1

        # Add to the correct list
        if is_dir:
            self.excluded_folder_paths.append((relative_path, reason))
        else: # Treat as file if is_dir is False or None
            self.excluded_file_paths.append((relative_path, reason))

    def excluded_by_pattern(self, reason: str):
       # This method is largely redundant now as counters are updated elsewhere
       pass

    @property
    def total_files_processed(self) -> int:
        # Note: This counts attempts, including skipped content
        return (
            self.files_included
            + self.files_excluded_default
            + self.files_excluded_user
            + self.files_excluded_size
            + self.files_excluded_include
            + self.files_excluded_output
            + self.files_skipped_permission
            + self.files_skipped_encoding
        )

    @property
    def total_files_excluded_by_filter(self) -> int:
        # Sum of specific file exclusion counters updated in _build_digest_structure
        return (
            self.files_excluded_default
            + self.files_excluded_user
            + self.files_excluded_size
            + self.files_excluded_include
            + self.files_excluded_output
        )

    @property
    def total_dirs_processed(self) -> int:
        return self.dirs_included + self.dirs_excluded

    def log_path_details(self):
        """Logs the collected paths categorized by type and status (included/excluded)."""

        def log_section(title: str, paths: list, color: str, show_reason: bool = False):
            # Use f-string for title formatting consistency
            section_title = f"--- {title} ---"
            log.info(f"[bold]{section_title}[/bold]")
            if paths:
                for item in sorted(paths):
                    if show_reason:
                        path_str, reason = item
                        reason_short = reason.split(" (")[0]
                        log.info(f"  [{color}]- {path_str}[/{color}] ([dim]{reason_short}[/dim])")
                    else:
                        path_str = item
                        log.info(f"  [{color}]+ {path_str}[/{color}]")
            else:
                log.info("  (None)")
            # Make footer match title length
            log.info(f"[bold]{'-' * len(section_title)}[/bold]")
            log.info("") # Add spacing after section

        # Print in the desired order
        log_section("Excluded Folders", self.excluded_folder_paths, "red", show_reason=True)
        log_section("Excluded Files", self.excluded_file_paths, "red", show_reason=True)
        log_section("Included Folders", self.included_folder_paths, "green")
        log_section("Included Files", self.included_file_paths, "green")


    def log_summary(self):
        """Logs the summary statistics."""
        log.info("[bold]--- Processing Summary ---[/bold]")
        log.info(f"Included Files (Content Read): {self.files_included}")
        log.info(f"Included Directories:          {self.dirs_included}")
        # Calculate total excluded dirs count for summary
        total_dirs_excluded = len(self.excluded_folder_paths) + self.symlinks_skipped # Include symlinks if they are counted as excluded dirs elsewhere? Check logic.
        log.info(f"Excluded Directories:          {self.dirs_excluded}") # Use counter updated in _build_digest_structure
        log.info(f"Excluded Files (By Filter):    {self.total_files_excluded_by_filter}")
        log.info(f"  - By Output File Target:     {self.files_excluded_output}")
        log.info(f"  - By Default Pattern:        {self.files_excluded_default}")
        log.info(f"  - By User Pattern:           {self.files_excluded_user}")
        log.info(f"  - By Max Size:               {self.files_excluded_size}")
        log.info(f"  - By Include Pattern:        {self.files_excluded_include}")
        log.info("Skipped File Content (Included Files):")
        log.info(f"  - Permission Errors:         {self.files_skipped_permission}")
        log.info(f"  - Encoding Errors:           {self.files_skipped_encoding}")
        log.info(f"Skipped Symlinks:              {self.symlinks_skipped}")
        log.info("[bold]--------------------------[/bold]")
        log.info("")


def _read_file_content(
    file_path: Path, encoding: str, stats: ProcessingStats
) -> Tuple[Optional[str], FileStatus, float]:
    """Attempts to read file content, handling errors and size."""
    status = FileStatus.INCLUDED
    content = None
    size_bytes = 0
    size_kb = 0.0
    try:
        size_bytes = file_path.stat().st_size
        size_kb = size_bytes / 1024.0
        content = file_path.read_text(encoding=encoding, errors="strict")
        log.debug(f"Read {file_path.name} ({size_kb:.1f} KB)")

    except UnicodeDecodeError:
        log.warning(f"Could not decode {file_path} as {encoding}. Treating as binary/non-text.")
        status = FileStatus.SKIPPED_ENCODING
        stats.files_skipped_encoding += 1
    except PermissionError:
        log.warning(f"Permission error reading {file_path}. Skipping content.")
        status = FileStatus.SKIPPED_PERMISSION
        stats.files_skipped_permission += 1
    except OSError as e:
        log.warning(f"OS error reading {file_path}: {e}. Skipping content.")
        status = FileStatus.SKIPPED_PERMISSION
        stats.files_skipped_permission += 1
    except Exception as e:
        log.error(f"Unexpected error reading {file_path}: {e}", exc_info=True)
        status = FileStatus.SKIPPED_PERMISSION
        stats.files_skipped_permission += 1

    size_kb = (size_bytes / 1024.0) if size_bytes else 0.0
    return content, status, size_kb


def _build_digest_structure(
    current_path: Path,
    root_dir: Path,
    path_filter: PathFilter,
    stats: ProcessingStats,
    config: dict,
) -> Optional[FileSystemItem]:
    """
    Recursively traverses the directory, filters items, and builds the data structure.
    Also collects included/excluded paths in the stats object for logging.
    """
    relative_path_repr = ""
    resolved_current_path = current_path
    is_dir_known = None

    try: resolved_current_path = current_path.resolve()
    except (OSError, FileNotFoundError) as e:
        try: relative_path_repr = str(current_path.relative_to(root_dir).as_posix()) if current_path != root_dir else "."
        except ValueError: relative_path_repr = str(current_path)
        reason = f"Could not resolve path: {e}"
        log.warning(f"{reason}. Skipping {current_path}.")
        stats.add_excluded_path(relative_path_repr, reason, is_dir=None)
        return None

    resolved_root_dir = root_dir

    try:
        if resolved_current_path == resolved_root_dir: relative_path_repr = "."
        else: relative_path_repr = str(resolved_current_path.relative_to(resolved_root_dir).as_posix())
    except ValueError:
        reason = f"Path outside root directory {resolved_root_dir}"
        log.warning(f"{resolved_current_path}: {reason}. Skipping.")
        is_dir_known = None
        try: is_dir_known = resolved_current_path.is_dir()
        except OSError: pass
        stats.add_excluded_path(str(resolved_current_path), reason, is_dir=is_dir_known)
        return None

    pathspec_match_path = ("" if relative_path_repr == "." else relative_path_repr)

    follow_symlinks = config.get("follow_symlinks", False)
    if current_path.is_symlink():
        is_dir_known = None
        if not follow_symlinks:
            reason = "Skipping symlink (follow_symlinks=False)"
            log.debug(f"{relative_path_repr}: {reason} (points to {resolved_current_path})")
            stats.symlinks_skipped += 1
            try: is_dir_known = resolved_current_path.is_dir()
            except OSError: pass
            stats.add_excluded_path(relative_path_repr, reason, is_dir=is_dir_known)
            return None
        else:
            if resolved_current_path == resolved_root_dir:
                reason = "Symlink loop detected: -> root"
                log.warning(f"{relative_path_repr}: {reason}. Skipping.")
                stats.symlinks_skipped += 1
                stats.add_excluded_path(relative_path_repr, reason, is_dir=True)
                return None

    try:
        if not resolved_current_path.exists():
            reason = "Path does not exist after resolution/symlink check"
            log.warning(f"{relative_path_repr}: {reason}. Skipping.")
            stats.add_excluded_path(relative_path_repr, reason, is_dir=None)
            return None

        is_dir = resolved_current_path.is_dir()
        is_dir_known = True

        include_item, reason = path_filter.check(resolved_current_path, pathspec_match_path)

        if not include_item:
            stats.add_excluded_path(relative_path_repr, reason, is_dir=is_dir)
            if is_dir:
                stats.dirs_excluded += 1
                # Update detailed counters if needed based on reason for dir exclusion
                if "default pattern" in reason: stats.files_excluded_default += 0 # Example: No specific counter for default excluded dirs yet
                elif "user pattern" in reason: stats.files_excluded_user += 0
                elif "include pattern" in reason: stats.files_excluded_include += 0
            else: # Is file
                # Counters updated in add_excluded_path for size/output
                # Update pattern counters here
                if "default pattern" in reason: stats.files_excluded_default += 1
                elif "user pattern" in reason: stats.files_excluded_user += 1
                elif "include pattern" in reason: stats.files_excluded_include += 1
                else: stats.files_excluded_user += 1 # Fallback
            return None

        stats.add_included_path(relative_path_repr, is_dir=is_dir)

        if is_dir:
            stats.dirs_included += 1
            log.debug(f"Processing directory: {relative_path_repr}")
            dir_info = DirectoryInfo(relative_path=relative_path_repr, absolute_path=resolved_current_path, children=[])
            try: items_in_dir = sorted(list(resolved_current_path.iterdir()))
            except PermissionError:
                reason = "Permission error listing contents"
                log.warning(f"{relative_path_repr}: {reason}. Skipping directory children.")
                return dir_info
            except OSError as e:
                reason = f"OS error listing contents: {e}"
                log.warning(f"{relative_path_repr}: {reason}. Skipping directory children.")
                return dir_info

            for item_path in items_in_dir:
                child_item = _build_digest_structure(item_path, resolved_root_dir, path_filter, stats, config)
                if child_item: dir_info.children.append(child_item)
            return dir_info

        else: # Item is a file
            content, status, size_kb = _read_file_content(resolved_current_path, config.get("encoding", "utf-8"), stats)
            if status == FileStatus.INCLUDED: stats.files_included += 1
            file_info = FileInfo(relative_path=relative_path_repr, absolute_path=resolved_current_path, content=content, status=status, size_kb=size_kb)
            return file_info

    except PermissionError:
        reason = "Permission error accessing item"
        log.warning(f"{relative_path_repr}: {reason} (Resolved: {resolved_current_path}). Skipping.")
        stats.add_excluded_path(relative_path_repr, reason, is_dir=is_dir_known)
        if is_dir_known is True: stats.dirs_excluded += 1
        else: stats.files_skipped_permission += 1
        return None
    except (OSError, FileNotFoundError) as e:
        reason = f"OS error processing item: {e}"
        log.warning(f"{relative_path_repr}: {reason} (Resolved: {resolved_current_path}). Skipping.")
        stats.add_excluded_path(relative_path_repr, reason, is_dir=is_dir_known)
        if is_dir_known is True: stats.dirs_excluded += 1
        else: stats.files_skipped_permission += 1
        return None
    except Exception as e:
        reason = f"Unexpected error processing item: {e}"
        log.error(f"{relative_path_repr}: {reason} (Resolved: {resolved_current_path})", exc_info=True)
        stats.add_excluded_path(relative_path_repr, reason, is_dir=is_dir_known)
        if is_dir_known is True: stats.dirs_excluded += 1
        else: stats.files_skipped_permission += 1
        return None


def generate_digest(directory: Path, config: dict) -> Optional[str]:
    """Generates the digest for the specified directory based on the configuration."""
    log.info(f"Starting dirdigest scan for directory: {directory}")
    log.info(f"Output format: {config['format']}")
    log.info(f"Max file size: {config['max_size']} KB")
    log.info("")

    try: resolved_root = directory.resolve()
    except (OSError, FileNotFoundError) as e:
        log.error(f"Input directory {directory} cannot be resolved or accessed: {e}", exc_info=True)
        return None

    output_file = config.get("output")
    path_filter = PathFilter(
        root_dir=resolved_root,
        include_patterns=config.get("include"),
        exclude_patterns=config.get("exclude"),
        use_default_excludes=config.get("default_ignore", True),
        max_file_size_kb=config.get("max_size"),
        output_file_path=output_file,
    )

    stats = ProcessingStats()
    root_item = _build_digest_structure(resolved_root, resolved_root, path_filter, stats, config)

    stats.log_path_details()
    stats.log_summary()

    if root_item is None:
        root_was_processed_and_excluded = any(p == "." for p, r in stats.excluded_folder_paths + stats.excluded_file_paths)
        if root_was_processed_and_excluded: log.error("Root directory '.' was excluded. No output generated.")
        else: log.error("Failed to build the directory structure (root item is None). No output generated.")
        return None

    if isinstance(root_item, DirectoryInfo) and not root_item.children:
         if not stats.included_file_paths and not stats.included_folder_paths and (stats.excluded_file_paths or stats.excluded_folder_paths):
             log.warning("The scanned directory appears empty or fully excluded based on filters. Generating empty digest.")
         elif not stats.included_file_paths and not stats.included_folder_paths and not stats.excluded_file_paths and not stats.excluded_folder_paths:
             log.warning("The scanned directory appears empty or contained only unprocessable items. Generating empty digest.")

    if not isinstance(root_item, DirectoryInfo):
         log.error(f"Built structure is not a DirectoryInfo object ({type(root_item)}). Cannot format.")
         return None

    # --- Format output ---
    output_format = config.get("format", "markdown").lower()
    try:
        # --- Removed redundant log message here ---
        # log.info(f"Formatting output as {output_format.upper()}...")
        if output_format == "json": 
            digest_content = format_json(root_item)
        elif output_format == "markdown": 
            digest_content = format_markdown(root_item)
        else:
            log.error(f"Invalid output format specified: {output_format}. Defaulting to Markdown.")
            digest_content = format_markdown(root_item)
        # Keep the specific log messages inside format_json/format_markdown
        #log.info("Formatting complete.")
        # log.info("")
        return digest_content
    except Exception as e:
         log.error(f"Error during output formatting ({output_format}): {e}", exc_info=True)
         return None