import fnmatch
from pathlib import Path
import os
from typing import List


def matches_pattern(path_str: str, pattern: str) -> bool:
    # Normalize path separators to / for consistent matching
    # This helps with cross-platform compatibility if paths use \
    path_str_n = path_str.replace(os.sep, "/")
    pattern_n = pattern.replace(os.sep, "/")

    if pattern_n.endswith("/"):
        # Pattern is a directory pattern, e.g., "foo/"
        # It should match the directory "foo" itself if path_str_n is "foo"
        if path_str_n == pattern_n.rstrip("/"):
            return True
        # It should also match paths inside that directory, e.g., "foo/bar.txt"
        # This is achieved by checking if the path starts with the directory pattern.
        if path_str_n.startswith(pattern_n):
            return True
        return False # Not the directory itself and not starting with the directory path
    else:
        # Pattern is a file pattern (e.g., "*.txt", "file.py") 
        # or a pattern that could match a directory name without a trailing slash (e.g., "build").
        # fnmatch will handle these cases.
        return fnmatch.fnmatch(path_str_n, pattern_n)


def matches_patterns(path_str: str, patterns: List[str]) -> bool:
    """Checks if the path_str matches any of the provided patterns."""
    for pattern_item in patterns:
        if matches_pattern(path_str, pattern_item):
            return True
    return False


def is_path_hidden(path_obj: Path) -> bool:
    """Checks if any part of the path starts with a '.' character."""
    return any(part.startswith(".") for part in path_obj.parts)