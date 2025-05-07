# src/dirdigest/filtering.py (Added output file exclusion)

import logging
from pathlib import Path
from typing import List, Optional, Tuple

import pathspec

from .config import DEFAULT_EXCLUDE_PATTERNS

log = logging.getLogger(__name__)


class PathFilter:
    """Applies include/exclude filters to paths."""

    def __init__(
        self,
        root_dir: Path,
        include_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
        use_default_excludes: bool = True,
        max_file_size_kb: Optional[int] = None,
        output_file_path: Optional[Path] = None, # <<< Added output file path parameter
    ):
        """
        Initializes the PathFilter.

        Args:
            root_dir: The root directory relative to which patterns are matched.
            include_patterns: List of glob patterns to include. If None or empty,
                              all non-excluded items are implicitly included.
            exclude_patterns: List of user-provided glob patterns to exclude.
            use_default_excludes: Whether to use the built-in default exclude patterns.
            max_file_size_kb: Maximum file size in KB to include. Files larger
                              than this will be excluded by the size check.
            output_file_path: The Path object representing the output file, if specified.
        """
        self.root_dir = root_dir.resolve()
        self.include_patterns = include_patterns or []
        self.user_exclude_patterns = exclude_patterns or []
        self.use_default_excludes = use_default_excludes
        self.max_file_size_bytes = (
            max_file_size_kb * 1024 if max_file_size_kb is not None else None
        )

        # Store the resolved absolute path of the output file for comparison
        # Resolve relative paths against the current working directory where the CLI runs
        try:
            self.output_file_abs_path = output_file_path.resolve() if output_file_path else None
        except OSError as e:
            log.warning(f"Could not resolve output file path {output_file_path}: {e}. Output file exclusion might not work correctly.")
            self.output_file_abs_path = None

        # Compile pathspec matchers
        self.default_spec = pathspec.PathSpec.from_lines(
            'gitwildmatch', DEFAULT_EXCLUDE_PATTERNS
        ) if self.use_default_excludes else None
        self.user_exclude_spec = pathspec.PathSpec.from_lines(
            'gitwildmatch', self.user_exclude_patterns
        ) if self.user_exclude_patterns else None
        self.include_spec = pathspec.PathSpec.from_lines(
            'gitwildmatch', self.include_patterns
        ) if self.include_patterns else None

        log.debug(f"Filter initialized. Root context: {self.root_dir}")
        log.debug(f"  Default excludes active: {self.use_default_excludes}")
        if self.output_file_abs_path:
             log.debug(f"  Output file exclusion target: {self.output_file_abs_path}")
        if self.user_exclude_patterns:
             log.debug(f"  User excludes: {self.user_exclude_patterns}")
        if self.include_patterns:
             log.debug(f"  Includes: {self.include_patterns}")
        if self.max_file_size_bytes is not None:
            log.debug(f"  Max file size: {max_file_size_kb} KB ({self.max_file_size_bytes} B)")


    def check(self, path: Path, relative_path_str: str) -> Tuple[bool, str]:
        """
        Checks if a path should be included based on the filter rules.
        Order of checks: Output File -> Default Excludes -> User Excludes -> Include Patterns -> Size.
        """
        try:
            # Resolve path here for reliable stat checks
            abs_path = path.resolve()
            if not abs_path.exists():
                 reason = f"Excluded: Path does not exist after resolving '{path}' -> '{abs_path}'"
                 log.warning(reason)
                 return False, reason

            is_dir = abs_path.is_dir()
            display_path = relative_path_str or "."

            # --- 1. Output File Check ---
            if self.output_file_abs_path and abs_path == self.output_file_abs_path:
                reason = f"Excluded: Matches output file path '{display_path}'"
                log.debug(f"{display_path}: {reason}")
                return False, reason

            # Prepare path string for pattern matching
            match_str = relative_path_str
            if is_dir and match_str != ".":
                match_str += '/'

            # --- 2. Default Exclusions ---
            if self.default_spec and self.default_spec.match_file(match_str):
                reason = f"Excluded by default pattern matching '{display_path}'"
                log.debug(f"{display_path}: {reason}")
                return False, reason

            # --- 3. User Exclusions ---
            if self.user_exclude_spec and self.user_exclude_spec.match_file(match_str):
                reason = f"Excluded by user pattern matching '{display_path}'"
                log.debug(f"{display_path}: {reason}")
                return False, reason

            # --- 4. Inclusion Checks (Only if --include patterns are specified) ---
            # <<< Refined include logic >>>
            if self.include_spec:
                # Files MUST match include spec
                if not is_dir and not self.include_spec.match_file(match_str):
                    reason = f"Excluded: File does not match any '--include' pattern ('{display_path}')"
                    log.debug(f"{display_path}: {reason}")
                    return False, reason
                # Directories are allowed if they don't match excludes (handled above)
                # They don't strictly need to match an include pattern themselves to allow traversal
                # Note: If a dir *does* match an include, it's still included.
                # If the directory itself was excluded by steps 2 or 3, we wouldn't reach here.

            # --- 5. File Size Check (Only for files) ---
            if not is_dir and self.max_file_size_bytes is not None:
                try:
                    file_size = abs_path.stat().st_size
                    if file_size > self.max_file_size_bytes:
                        reason = (f"Excluded by size ({file_size / 1024:.1f} KB "
                                  f"> max {self.max_file_size_bytes / 1024:.1f} KB)")
                        log.debug(f"{display_path}: {reason}")
                        return False, reason
                except OSError as e:
                    reason = f"Warning: Could not get size for {abs_path.name}, skipping size check ({e})"
                    log.warning(reason)

            # --- If not excluded by any rule ---
            log.debug(f"{display_path}: Included")
            return True, "Included"

        # ... (Exception handling remains the same) ...
        except FileNotFoundError:
             reason = f"Error during filtering: File not found {path}"
             log.warning(reason)
             return False, reason
        except OSError as e:
            reason = f"OS error during filtering {path}: {e}"
            log.warning(reason)
            return False, reason
        except Exception as e:
            reason = f"Unexpected error during filtering {path}: {e}"
            log.error(reason, exc_info=True)
            return False, reason