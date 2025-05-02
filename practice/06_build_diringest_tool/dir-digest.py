#!/usr/bin/env python3

import argparse
import sys
import os
import json
from pathlib import Path
import fnmatch
import logging
from typing import Optional, Dict, List
import traceback

# Configure logging - make it more visible
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    stream=sys.stderr
)

# --- Default Configuration ---
DEFAULT_MAX_SIZE_KB = 100
# Patterns matching directories or files to ignore by default
# Uses fnmatch syntax (similar to .gitignore)
DEFAULT_IGNORE_PATTERNS = [
    # Hidden files and directories (starting with dot)
    ".*",  # Match all hidden files
    ".*/",  # Match all hidden directories

    # Specific directories to ignore
    ".git/",
    ".svn/",
    ".hg/",
    ".vscode/",
    ".idea/",
    "__pycache__/",
    "node_modules/",
    "build/",
    "dist/",
    "target/",

    # Specific file types to ignore
    "*.pyc",
    "*.log",
    "*.swp",
    "*.swo",
    "*~", # Vim backup files
    ".DS_Store",
]
# Heuristic for binary file detection
MAX_BINARY_CHECK_BYTES = 1024 # Read first KB to check for null bytes

# --- Helper Functions ---

def is_likely_binary(file_path: Path) -> bool:
    """
    Check if a file is likely binary by looking for null bytes
    in the first MAX_BINARY_CHECK_BYTES.
    """
    try:
        with open(file_path, "rb") as f:
            chunk = f.read(MAX_BINARY_CHECK_BYTES)
        return b"\x00" in chunk
    except OSError:
        # Could be a broken symlink, permission error, etc. Treat as binary.
        return True
    except Exception as e:
        print(f"Warning: Error checking binary status for {file_path}: {e}", file=sys.stderr)
        return True # Be cautious

def matches_pattern(path: str, patterns: list[str]) -> bool:
    """Check if the given path matches any of the provided patterns."""
    if not patterns:
        return False

    # Normalize path for matching (use forward slashes)
    normalized_path = path.replace(os.sep, '/')

    for pattern in patterns:
        # Direct fnmatch for simple patterns
        if fnmatch.fnmatch(normalized_path, pattern):
            # print(f"DEBUG MATCH: '{normalized_path}' matched pattern '{pattern}'")
            return True

        # Handle directory patterns ending with /
        if pattern.endswith('/'):
            pattern_without_slash = pattern[:-1]
            # Match if path is exactly the pattern_without_slash or starts with pattern_without_slash/
            if normalized_path == pattern_without_slash or normalized_path.startswith(pattern_without_slash + '/'):
                # print(f"DEBUG MATCH (dir): '{normalized_path}' matched pattern '{pattern}'")
                return True

    # print(f"DEBUG NO MATCH: '{normalized_path}' did not match patterns: {patterns}")
    return False

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a concatenated text digest of a local codebase, suitable for LLMs.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "directory", type=str, help="The path to the local directory to process."
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Path to a file where the output digest should be saved. If not provided, output goes to stdout.",
    )
    # --- NEW FLAGS ---
    parser.add_argument(
        "--exclude",
        type=str,
        default="",
        help='Comma-separated list of fnmatch patterns to exclude (e.g., "*.log,build/,docs/*.md").',
    )
    parser.add_argument(
        "--include",
        type=str,
        default="",
        help='Comma-separated list of fnmatch patterns to include (e.g., "*.py,src/,*.c"). If used, only matching files/dirs are processed.',
    )
    # --- END NEW FLAGS ---
    parser.add_argument(
        "--max-size",
        type=int,
        default=DEFAULT_MAX_SIZE_KB,
        help="Maximum file size in Kilobytes (KB) to include. Use 0 or -1 for no limit.",
    )
    parser.add_argument(
        "--no-ignore-binary",
        action="store_false",
        dest="ignore_binary", # store_false means the flag presence sets it to False
        default=True, # Default is True (ignore binary files)
        help="Include files detected as binary (use with caution).",
    )
    parser.add_argument(
        "--no-default-ignore",
        action="store_true",
        default=False,
        help="If set, disables the default exclusion of common VCS, build, and config directories/files.",
    )
    parser.add_argument(
        "--encoding",
        type=str,
        default="utf-8",
        help="Specify the encoding to use when reading text files.",
    )
    parser.add_argument(
        "--errors",
        type=str,
        default="replace",
        choices=['strict', 'ignore', 'replace', 'surrogateescape', 'xmlcharrefreplace', 'backslashreplace'],
        help="How to handle encoding errors when reading files.",
    )

    args = parser.parse_args()

    # --- VALIDATION ---
    if args.exclude and args.include:
        parser.error("Cannot use both --exclude and --include flags simultaneously.")
    # --- END VALIDATION ---

    return args

def get_file_content(file_path: Path, encoding: str, max_size: int, errors_handling: str, ignore_binary: bool = True) -> Optional[str]:
    """Get file content with proper error handling."""
    # Skip if file exceeds max size (if max_size limit is enabled)
    # Size check moved to process_directory for better logging context

    try:
        # Check if it's a binary file (using the helper)
        is_binary = is_likely_binary(file_path)

        # Skip binary files if we should ignore them
        if is_binary and ignore_binary:
            # Logging moved to process_directory
            # logging.info(f"Skipping binary file: {file_path}")
            return None

        # Read content based on whether it's binary or text
        if not is_binary:
            # Read as text
            try:
                with open(file_path, 'r', encoding=encoding, errors=errors_handling) as f:
                    return f.read()
            except UnicodeDecodeError as e:
                logging.warning(f"Warning: Encoding error reading {file_path}: {str(e)}")
                return None
        else: # We are reading a binary file (because ignore_binary is False)
            # Read as bytes and decode with replacement for representation
            with open(file_path, 'rb') as f:
                content_bytes = f.read()
                try:
                    # Attempt to decode, replacing errors. This might not be perfect.
                    return content_bytes.decode(encoding, errors='replace')
                except Exception:
                    # Fallback if decoding itself fails catastrophically
                    return f"[Binary content - {len(content_bytes)} bytes, decode failed]"

    except Exception as e:
        # Logging moved to process_directory
        logging.warning(f"Error reading {file_path}: {str(e)}")
        return None


def get_default_ignore_patterns() -> list[str]:
    """Return default patterns to ignore."""
    return DEFAULT_IGNORE_PATTERNS

def process_directory(
    root_dir: Path,
    encoding: str,
    max_size_bytes: int,
    default_ignore_patterns: List[str],
    include_patterns: List[str],
    exclude_patterns: List[str],
    errors_handling: str,
    ignore_binary: bool,
    no_default_ignore: bool,
    output_path: Optional[Path]
) -> Dict[str, str]:
    """Process directory recursively and gather contents of files that match criteria."""
    file_contents = {}
    excluded_files_count = 0
    excluded_dirs_count = 0
    processed_files_count = 0

    # Determine mode based on which patterns are provided
    mode = "include" if include_patterns else "exclude"
    user_patterns = include_patterns if mode == "include" else exclude_patterns

    logging.info(f"Starting directory scan: {root_dir}\n\n")
    
    for current_path_str, dirs, files in os.walk(root_dir, topdown=True):
        current_path = Path(current_path_str)
        rel_current_path_str = os.path.relpath(current_path, root_dir).replace(os.sep, '/')
        if rel_current_path_str == '.':
            rel_current_path_str = '' # Use empty string for root

        # Modify dirs in-place to prevent descending into excluded directories
        dirs_to_remove = []
        for i, d in enumerate(dirs):
            dir_path = current_path / d
            rel_dir_path_str = os.path.join(rel_current_path_str, d).replace(os.sep, '/') if rel_current_path_str else d

            # 1. Check Default Ignores (Hidden & Patterns)
            if not no_default_ignore:
                # Skip hidden directories (component starts with '.')
                if any(part.startswith('.') for part in rel_dir_path_str.split('/')):
                    logging.info(f"EXCLUDED DIR (hidden): {rel_dir_path_str}")
                    dirs_to_remove.append(d)
                    excluded_dirs_count += 1
                    continue
                # Skip default ignore patterns
                if matches_pattern(rel_dir_path_str + '/', default_ignore_patterns) or \
                   matches_pattern(rel_dir_path_str, default_ignore_patterns):
                    logging.info(f"EXCLUDED DIR (default pattern): {rel_dir_path_str}")
                    dirs_to_remove.append(d)
                    excluded_dirs_count += 1
                    continue

            # 2. Check User Patterns (Exclude Mode)
            if mode == "exclude" and user_patterns:
                if matches_pattern(rel_dir_path_str + '/', user_patterns) or \
                   matches_pattern(rel_dir_path_str, user_patterns):
                    logging.info(f"EXCLUDED DIR (user exclude pattern): {rel_dir_path_str}")
                    dirs_to_remove.append(d)
                    excluded_dirs_count += 1
                    continue

            # 3. Check User Patterns (Include Mode) - Tricky!
            # We CANNOT prune a directory in include mode just because it doesn't match,
            # as it might contain matching files/subdirs. We filter files later.
            # However, if a directory *explicitly matches* an include pattern, we keep it.
            # If it *doesn't* match, we still need to descend.
            # The `build_directory_structure` will handle pruning empty branches later.
            pass # No directory pruning based on non-matching include patterns here

        # Remove marked directories from traversal
        for d in dirs_to_remove:
            dirs.remove(d)

        # Process files in the current directory
        for file_name in files:
            file_path = current_path / file_name
            rel_file_path_str = os.path.join(rel_current_path_str, file_name).replace(os.sep, '/') if rel_current_path_str else file_name

            # --- Filtering Logic ---
            exclude_reason = None

            # 0. Exclude output file explicitly
            if output_path and file_path.resolve() == output_path:
                exclude_reason = "output file"

            # 1. Check Default Ignores (Hidden & Patterns)
            if not exclude_reason and not no_default_ignore:
                if any(part.startswith('.') for part in rel_file_path_str.split('/')):
                    exclude_reason = "hidden"
                elif matches_pattern(rel_file_path_str, default_ignore_patterns):
                    exclude_reason = "default pattern"

            # 2. Check User Patterns (Exclude Mode)
            if not exclude_reason and mode == "exclude" and user_patterns:
                if matches_pattern(rel_file_path_str, user_patterns):
                    exclude_reason = "user exclude pattern"

            # 3. Check User Patterns (Include Mode)
            if not exclude_reason and mode == "include" and user_patterns:
                if not matches_pattern(rel_file_path_str, user_patterns):
                    # Check if any *parent directory* matches an include pattern ending in '/'
                    # This allows including all files within an included directory
                    included_by_parent = False
                    for pattern in user_patterns:
                         if pattern.endswith('/'):
                              dir_pattern = pattern[:-1]
                              if rel_file_path_str.startswith(dir_pattern + '/'):
                                   included_by_parent = True
                                   break
                    if not included_by_parent:
                         exclude_reason = "not matching include pattern"


            # 4. Check Size Limit
            if not exclude_reason and max_size_bytes > 0:
                try:
                    file_size = file_path.stat().st_size
                    if file_size > max_size_bytes:
                        exclude_reason = f"size limit ({file_size} > {max_size_bytes} bytes)"
                except OSError as e:
                    exclude_reason = f"size check failed ({e})"

            # 5. Check Binary (if ignore_binary is True)
            if not exclude_reason and ignore_binary:
                try:
                    if is_likely_binary(file_path):
                        exclude_reason = "binary content"
                except Exception as e:
                    exclude_reason = f"binary check failed ({e})"

            # --- Exclusion or Processing ---
            if exclude_reason:
                logging.info(f"EXCLUDED FILE ({exclude_reason}): {rel_file_path_str}")
                excluded_files_count += 1
                continue
            else:
                # Get file content
                content = get_file_content(file_path, encoding, max_size_bytes, errors_handling, ignore_binary)
                if content is not None:
                    logging.info(f"INCLUDED FILE: {rel_file_path_str}")
                    file_contents[rel_file_path_str] = content
                    processed_files_count += 1
                else:
                    # Reason for skipping (e.g., read error, caught binary) logged inside get_file_content or binary check
                    logging.info(f"EXCLUDED FILE (content read failed/skipped): {rel_file_path_str}")
                    excluded_files_count += 1 # Count as excluded if content is None

    logging.info("-" * 120)
    logging.info(f"Scan complete. Processed {processed_files_count} files.")
    logging.info(f"Excluded {excluded_dirs_count} directories and {excluded_files_count} files.")
    logging.info("=" * 120 + "\n")
    return file_contents

def is_hidden_path(path: str) -> bool:
    """Check if a path contains any hidden directory components (starting with dot)."""
    # Ensure we handle paths starting with ./ correctly
    parts = path.strip('/').split('/')
    return any(part.startswith('.') for part in parts if part and part != '.')


def build_directory_structure(
    root_dir: Path,
    file_contents: dict,
    default_ignore_patterns: List[str],
    include_patterns: List[str],
    exclude_patterns: List[str],
    no_default_ignore: bool,
    output_path: Optional[Path]
):
    """Build a nested JSON structure representing the directory."""
    mode = "include" if include_patterns else "exclude"
    user_patterns = include_patterns if mode == "include" else exclude_patterns

    return _build_recursive_structure(
        root_dir=root_dir,
        current_rel_path=".", # Start with relative path '.' for root
        file_contents=file_contents,
        default_ignore_patterns=default_ignore_patterns,
        user_patterns=user_patterns,
        mode=mode,
        no_default_ignore=no_default_ignore,
        output_path=output_path
    )

def _build_recursive_structure(
    root_dir: Path,
    current_rel_path: str, # Relative path from root_dir
    file_contents: dict,
    default_ignore_patterns: List[str],
    user_patterns: List[str],
    mode: str,
    no_default_ignore: bool,
    output_path: Optional[Path]
):
    """Helper to recursively build the JSON structure."""
    current_full_path = root_dir / current_rel_path if current_rel_path != "." else root_dir
    current_rel_path_str = current_rel_path.replace(os.sep, '/') if current_rel_path != "." else ""

    # Basic filtering for the current directory itself (only applied if not root)
    if current_rel_path != ".":
        # Default ignore check (hidden path or pattern)
        if not no_default_ignore:
             # Check if path itself or any component is hidden
             if any(part.startswith('.') for part in current_rel_path_str.split('/')):
                 logging.debug(f"STRUCTURE SKIP (hidden path): {current_rel_path_str}")
                 return None
             # Check default patterns (match directory pattern or exact match)
             if matches_pattern(current_rel_path_str + '/', default_ignore_patterns) or \
                matches_pattern(current_rel_path_str, default_ignore_patterns):
                 logging.debug(f"STRUCTURE SKIP (default pattern): {current_rel_path_str}")
                 return None
        # User exclude check
        if mode == "exclude" and user_patterns:
            if matches_pattern(current_rel_path_str + '/', user_patterns) or \
               matches_pattern(current_rel_path_str, user_patterns):
                 logging.debug(f"STRUCTURE SKIP (user exclude): {current_rel_path_str}")
                 return None
        # User include check (A directory only survives if it matches or contains included items)
        # This is implicitly handled by only returning structure if it has children below

    # Get children
    folder_nodes = []
    file_nodes = []
    try:
        # Iterate over items, create full path and relative path for each
        items = sorted(list(current_full_path.iterdir()), key=lambda p: p.name) # Sort for consistent output

        for item in items:
            item_name = item.name
            item_rel_path = os.path.join(current_rel_path, item_name) if current_rel_path != "." else item_name
            item_rel_path_str = item_rel_path.replace(os.sep, '/')

            # Skip output file
            if output_path and item.resolve() == output_path:
                continue

            if item.is_dir():
                # Recurse into subdirectory
                subfolder_node = _build_recursive_structure(
                    root_dir, item_rel_path, file_contents, default_ignore_patterns,
                    user_patterns, mode, no_default_ignore, output_path
                )
                if subfolder_node: # Only add if the recursive call returned a structure (meaning it wasn't skipped/empty)
                    folder_nodes.append(subfolder_node)
            elif item.is_file():
                # Check if this file's content was included during process_directory
                if item_rel_path_str in file_contents:
                    file_nodes.append({
                        "type": "file",
                        "relative_path": item_rel_path_str,
                        "content": file_contents[item_rel_path_str]
                    })
                else:
                    # This file existed but was filtered out earlier (size, binary, pattern, etc.)
                    # We don't include it in the final structure.
                    logging.debug(f"STRUCTURE SKIP (file not in content dict): {item_rel_path_str}")
                    pass

    except (PermissionError, OSError) as e:
        logging.warning(f"Cannot access: {current_full_path} ({str(e)}) - skipping in structure.")
        return None # Skip directories we can't read

    # Combine folders and files, with folders first
    children_nodes = folder_nodes + file_nodes

    # Only return a node for this folder if it's the root or if it has children
    if children_nodes or current_rel_path == ".":
        return {
            "type": "folder",
            "relative_path": current_rel_path_str,
            "children": children_nodes
        }
    else:
        # This directory is empty or all its contents were filtered out
        logging.debug(f"STRUCTURE SKIP (empty/filtered): {current_rel_path_str}")
        return None


def print_crawling_rules(args, default_ignore_patterns, include_patterns, exclude_patterns, output_path=None):
    """Print a summary of the crawling rules that will be applied."""
    print("\n======================================== DIRECTORY DIGEST - CRAWLING RULES =============================================", file=sys.stderr)
    print(f"Target directory: {args.directory}", file=sys.stderr)

    # Determine mode
    mode = "include" if args.include else "exclude"
    print(f"Mode: {mode.upper()}", file=sys.stderr)

    # Default ignore patterns
    if args.no_default_ignore:
        print("\n- Default ignore patterns: DISABLED", file=sys.stderr)
    else:
        print("\n- Default ignore patterns: ENABLED", file=sys.stderr)
        print("  Default Exclusions:", file=sys.stderr)
        for pattern in default_ignore_patterns:
            print(f"    - {pattern}", file=sys.stderr)

    # User patterns
    if exclude_patterns:
        print("\n- User Exclude Patterns:", file=sys.stderr)
        for pattern in exclude_patterns:
            # Check if it's the output file path for clarity
            if output_path and pattern == str(output_path.resolve()).replace(os.sep, '/'):
                 print(f"    - {pattern} (output file)", file=sys.stderr)
            else:
                 print(f"    - {pattern}", file=sys.stderr)
    elif include_patterns:
        print("\n- User Include Patterns:", file=sys.stderr)
        for pattern in include_patterns:
            print(f"    - {pattern}", file=sys.stderr)
    else:
        print("\n- User patterns: NONE", file=sys.stderr)


    # Size limits
    if args.max_size <= 0:
        print("\n- File size limit: NONE", file=sys.stderr)
    else:
        print(f"\n- File size limit: {args.max_size} KB", file=sys.stderr)

    # Binary files
    if args.ignore_binary:
        print("\n- Binary files: EXCLUDED (heuristic check)", file=sys.stderr)
    else:
        print("\n- Binary files: INCLUDED", file=sys.stderr)

    # Hidden files/directories (Covered by default ignores, clarify interaction)
    if args.no_default_ignore:
         print("\n- Hidden files/directories (.name): INCLUDED (unless matched by user patterns)", file=sys.stderr)
    else:
         print("\n- Hidden files/directories (.name): EXCLUDED (by default ignores)", file=sys.stderr)

    # Encoding
    print(f"\n- Encoding: {args.encoding} (Errors: {args.errors})", file=sys.stderr)

    # if output_path:
    #     print(f"\n- Output file: {output_path} (will be excluded)", file=sys.stderr)

    print("=" * 120 + "\n", file=sys.stderr)


def main():
    """Main execution function."""
    args = parse_arguments()

    try:
        # Validate encoding
        try:
            "test".encode(args.encoding)
        except LookupError:
            print(f"Warning: Invalid encoding '{args.encoding}', falling back to 'utf-8'", file=sys.stderr)
            args.encoding = "utf-8"

        # Validate the target directory exists
        source_dir = Path(args.directory).resolve()
        if not source_dir.exists() or not source_dir.is_dir():
            print(f"Error: Input directory '{args.directory}' not found or is not a directory", file=sys.stderr)
            return 1

        # Prepare ignore patterns
        default_ignore_patterns = [] if args.no_default_ignore else get_default_ignore_patterns()

        # Prepare user patterns
        exclude_patterns = [p.strip().replace(os.sep, '/') for p in args.exclude.split(',') if p.strip()] if args.exclude else []
        include_patterns = [p.strip().replace(os.sep, '/') for p in args.include.split(',') if p.strip()] if args.include else []

        # Determine output path and ensure it's excluded
        output_path = None
        if args.output:
            output_path = Path(args.output).resolve()
            output_rel_path_str = None
            try:
                # Calculate relative path from source_dir if possible
                output_rel_path = output_path.relative_to(source_dir)
                output_rel_path_str = str(output_rel_path).replace(os.sep, '/')
            except ValueError:
                # Output path is outside the source directory, no need to add relative pattern
                pass

            # Add the relative output path to exclude patterns if it's inside the source dir
            # This ensures it's filtered correctly by matches_pattern
            if output_rel_path_str and output_rel_path_str not in exclude_patterns:
                 if not exclude_patterns and not include_patterns: # If using default exclude mode
                     exclude_patterns.append(output_rel_path_str)
                     logging.info(f"Automatically adding output file to exclusions: {output_rel_path_str}")
                 elif exclude_patterns: # If already using exclude patterns
                      exclude_patterns.append(output_rel_path_str)
                      logging.info(f"Automatically adding output file to exclusions: {output_rel_path_str}")
                 # Cannot automatically add to include_patterns - user must handle exclusion if using include


        # Print crawling rules before starting
        print_crawling_rules(args, default_ignore_patterns, include_patterns, exclude_patterns, output_path)

        max_size_bytes = args.max_size * 1024 if args.max_size > 0 else -1

        # 1. Process the directory and gather contents of included files
        file_contents = process_directory(
            root_dir=source_dir,
            encoding=args.encoding,
            max_size_bytes=max_size_bytes,
            default_ignore_patterns=default_ignore_patterns,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
            errors_handling=args.errors,
            ignore_binary=args.ignore_binary,
            no_default_ignore=args.no_default_ignore,
            output_path=output_path
        )

        # 2. Build the hierarchical structure based on processed files
        # Pass the same patterns again so structure builder knows what to exclude
        structure = build_directory_structure(
            root_dir=source_dir,
            file_contents=file_contents,
            default_ignore_patterns=default_ignore_patterns,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
            no_default_ignore=args.no_default_ignore,
            output_path=output_path
        )

        # Output the JSON structure
        if structure is None:
            # This can happen if the root directory itself was excluded or inaccessible
            print("Error: No structure generated. Root directory might be excluded or inaccessible.", file=sys.stderr)
            return 1

        try:
            output_json = json.dumps(structure, indent=2)
        except TypeError as e:
             print(f"Error: Failed to serialize structure to JSON: {e}", file=sys.stderr)
             print("This might happen if binary file content caused issues.", file=sys.stderr)
             return 1


        if args.output:
            # Write to file
            try:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "w", encoding="utf-8") as outfile:
                    outfile.write(output_json)
                print(f"\nOutput successfully written to: {output_path}", file=sys.stderr)
            except Exception as e:
                print(f"Error writing to file {output_path}: {str(e)}", file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
                return 1
        else:
            # Write to stdout
            print(output_json)

        # Summary already printed by process_directory
        # files_in_structure = len(file_contents) # Count files actually included
        # print(f"\nDigest generation complete. Included {files_in_structure} files in the output.", file=sys.stderr)

        return 0

    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())