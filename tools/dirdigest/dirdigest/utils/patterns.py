# dirdigest/utils/patterns.py
import fnmatch
from pathlib import Path
import os
from typing import List # Ensure List is imported

def matches_pattern(path_str: str, pattern_str: str) -> bool:
    """
    Checks if the given path_str matches the pattern_str.
    Handles common cases like 'dirname/', '**/dirname/', '*.ext', '**/file.ext'.
    """
    path_obj = Path(path_str)
    # Normalize pattern: replace os.sep with /, then process.
    norm_pattern = pattern_str.replace(os.sep, "/")

    # Case 1: Pattern targets a directory (e.g., "node_modules/", "**/__pycache__/", "*.egg-info/")
    # These patterns identify a directory name/pattern that, if present anywhere in the path_obj's components,
    # should cause a match for the directory or any file/subdir within it.
    if norm_pattern.endswith("/"):
        # Extract the core directory name/pattern to match against path components.
        # e.g., "node_modules/", "**/__pycache__/", "*.egg-info/"
        dir_target_name_pattern = norm_pattern.rstrip("/") # "node_modules", "**/__pycache__", "*.egg-info"
        
        if dir_target_name_pattern.startswith("**/"):
            # If "**/dirname", the part to match against components is "dirname"
            dir_target_name_pattern = dir_target_name_pattern[3:] # "__pycache__" or "dirname"

        # Now, dir_target_name_pattern is something like "node_modules", "__pycache__", "*.egg-info"
        # Check if any component (directory name) in path_obj.parts matches this dir_target_name_pattern.
        # path_obj.parts for "a/b/c.txt" is ("a", "b", "c.txt")
        # path_obj.parts for "a/b/c" (dir) is ("a", "b", "c")
        for part in path_obj.parts:
            if fnmatch.fnmatch(part, dir_target_name_pattern):
                return True
        return False

    # Case 2: Pattern targets a file or a path not explicitly ending in "/"
    # (e.g., "*.py", ".DS_Store", "**/specific.log", "LICENSE")
    else:
        if norm_pattern.startswith("**/"):
            # For patterns like "**/*.log" or "**/exact_filename.txt"
            # These should match against the base name of the path_obj.
            file_target_basename_pattern = norm_pattern[3:] # "*.log" or "exact_filename.txt"
            return fnmatch.fnmatch(path_obj.name, file_target_basename_pattern)
        else:
            # For patterns like "*.py", "README.md", or "data/*.csv".
            # These are typically matched against the full relative path string.
            # (fnmatch behavior: "*.py" matches "file.py" but not "dir/file.py")
            path_str_normalized_for_fnmatch = str(path_obj).replace(os.sep, "/")
            return fnmatch.fnmatch(path_str_normalized_for_fnmatch, norm_pattern)

def matches_patterns(path_str: str, patterns: List[str]) -> bool: # Changed from list[str] to List[str] for older Pythons if needed
    """Checks if the path_str matches any of the provided patterns."""
    for pattern_item in patterns:
        if matches_pattern(path_str, pattern_item):
            return True
    return False

def is_path_hidden(path_obj: Path) -> bool:
    """
    Checks if any part of the path starts with a '.' character,
    excluding the root '.' itself if path_obj is Path(".").
    """
    # Path(".").parts is ('.',), Path(".git").parts is ('.git',)
    # Path("src/.config").parts is ("src", ".config")
    return any(part.startswith(".") for part in path_obj.parts if part not in ('.', os.sep))