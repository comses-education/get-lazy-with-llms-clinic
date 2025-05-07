# src/dirdigest/formatting.py (Removed redundant 'status: included' from JSON)

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, cast

from rich.text import Text
from rich.tree import Tree

from .models import DirectoryInfo, FileInfo, FileStatus, FileSystemItem

log = logging.getLogger(__name__)

# --- Placeholder Messages ---\
# Used for Markdown output when content is skipped
PLACEHOLDERS = {
    FileStatus.SKIPPED_SIZE: "[dirdigest: file skipped, size > max_size KB]",
    FileStatus.SKIPPED_ENCODING: "[dirdigest: binary or non-UTF8 file]",
    FileStatus.SKIPPED_BINARY: "[dirdigest: binary or non-UTF8 file]", # Same as encoding for simplicity
    FileStatus.SKIPPED_PERMISSION: "[dirdigest: permission error reading file]",
}

def _get_placeholder(item: FileInfo) -> str:
    """Gets the appropriate placeholder message for a skipped file (Markdown)."""
    placeholder = PLACEHOLDERS.get(item.status, "[dirdigest: file content skipped]")
    # Add relative path context to the placeholder
    return f"{placeholder} at {item.relative_path}"


# --- JSON Formatting ---\

def _build_json_structure(item: FileSystemItem) -> Dict[str, Any]:
    """Recursively builds the dictionary structure for JSON output."""
    if isinstance(item, FileInfo):
        # Use content if included, otherwise use a placeholder string similar to Markdown
        # Choose a placeholder that clearly indicates skipped content in JSON context
        json_placeholder = f"[dirdigest: content skipped - {item.status.value}]"
        content_value = item.content if item.status == FileStatus.INCLUDED else json_placeholder

        file_dict: Dict[str, Any] = {
            "type": item.type.value,
            "relative_path": item.relative_path,
            "content": content_value,
            # Optionally add size_kb: round(item.size_kb, 2)
            # "size_kb": round(item.size_kb, 2)
        }
        # --- Conditionally add status only if NOT included ---
        if item.status != FileStatus.INCLUDED:
            file_dict["status"] = item.status.value # e.g., "skipped_size", "skipped_encoding"

        return file_dict

    elif isinstance(item, DirectoryInfo):
        # Sort children before processing for consistent output
        item.sort_children()
        children_json = [_build_json_structure(child) for child in item.children]
        return {
            "type": item.type.value,
            "relative_path": item.relative_path,
            "children": children_json,
        }
    else:
         # Should not happen with type hints, but handle defensively
        log.error(f"Unexpected item type encountered during JSON generation: {type(item)}")
        return {"error": "Unknown item type"}


def format_json(root: DirectoryInfo) -> str:
    """Formats the directory structure as a JSON string."""
    #log.info("Formatting output as JSON...")
    json_structure = _build_json_structure(root)
    try:
        # Ensure final newline for POSIX compatibility
        return json.dumps(json_structure, indent=2) + "\n"
    except TypeError as e:
        log.error(f"Error serializing data to JSON: {e}", exc_info=True)
        # Provide a valid JSON error object
        return json.dumps({"error": "Failed to serialize data to JSON", "details": str(e)}, indent=2) + "\n"


# --- Markdown Formatting ---\

def _generate_tree_overview(directory: DirectoryInfo) -> str:
    """Generates a plain text tree structure overview for Markdown."""
    if not directory.children:
        # Represent empty included directory
        return f"{directory.relative_path}/\n(empty)\n"

    tree = Tree(f"{directory.relative_path}/", guide_style="dim")
    directory.sort_children() # Sort for consistent tree view

    def add_nodes(node: Tree, items: List[FileSystemItem]):
        for i, item in enumerate(items):
            is_last = (i == len(items) - 1)
            # Ensure guide style is consistent even for last item unless it's truly the end
            guide_style = "dim" # Default guide style

            if isinstance(item, DirectoryInfo):
                style = "bold bright_blue"
                # Use Path name for display, add trailing slash
                child_node = node.add(f"{Path(item.relative_path).name}/", style=style, guide_style=guide_style)
                # Optional: Recursively add nodes for deeper tree view (currently shallow)
                # add_nodes(child_node, item.children)
            elif isinstance(item, FileInfo):
                name = Path(item.relative_path).name
                status_marker = ""
                style = ""
                if item.status != FileStatus.INCLUDED:
                    # Use a shorter marker for tree view
                    status_marker = f" [skipped]"
                    style = "dim" # Dim skipped files in tree
                node.add(f"{name}{status_marker}", style=style, guide_style=guide_style)

    add_nodes(tree, directory.children)

    # Render the tree to plain text using Rich's console capture
    from rich.console import Console
    # Create a temporary console for capturing tree output
    capture_console = Console(record=True, width=120, force_terminal=False, color_system=None)
    # capture_console.print(tree)
    # Export without styles to keep it plain text for Markdown
    return capture_console.export_text(styles=False)


def _format_markdown_recursive(item: FileSystemItem, output_lines: List[str]):
    """Recursively builds the Markdown output lines."""

    if isinstance(item, DirectoryInfo):
        folder_path = item.relative_path
        # Use slightly more prominent headers
        output_lines.append(f"## FOLDER: `{folder_path}`")
        output_lines.append("") # Add newline

        # Generate and add the tree overview for this directory level
        tree_overview = _generate_tree_overview(item)
        output_lines.append("```text") # Use text code block for tree
        output_lines.append(tree_overview.strip()) # Add tree, remove leading/trailing whitespace
        output_lines.append("```")
        output_lines.append("") # Add newline

        # Process files directly within this folder first
        files_in_folder = [child for child in item.children if isinstance(child, FileInfo)]
        for file_item in files_in_folder:
             _format_markdown_recursive(file_item, output_lines) # Adds FILE section

        # Then recursively process sub-folders
        sub_folders = [child for child in item.children if isinstance(child, DirectoryInfo)]
        for sub_folder_item in sub_folders:
             _format_markdown_recursive(sub_folder_item, output_lines) # Adds FOLDER section

        # Optional: Add explicit end marker, might be too verbose
        # output_lines.append(f"--- END FOLDER: {folder_path} ---")
        # output_lines.append("") # Add newline

    elif isinstance(item, FileInfo):
        file_path = item.relative_path
        # Use slightly more prominent headers
        output_lines.append(f"### FILE: `{file_path}`")

        # Get content or placeholder message
        content = item.content if item.status == FileStatus.INCLUDED else _get_placeholder(item)

        # Determine language for syntax highlighting
        lang = Path(file_path).suffix.lstrip('.') if Path(file_path).suffix else ""
        # Basic check for known non-code types that shouldn't get language hints
        # Allow common text/markup/data formats
        allowed_langs = {"txt", "md", "markdown", "rst", "csv", "tsv", "xml", "html", "css", "json", "yaml", "toml", "py", "js", "java", "c", "cpp", "cs", "go", "rb", "php", "swift", "kt", "rs", "sh", "bash", "sql", "dockerfile", "hcl", "tf"}
        if lang.lower() not in allowed_langs:
             lang = "" # Default to no language hint if suffix unknown/not text-like
        if item.status != FileStatus.INCLUDED:
             lang = "" # No language for placeholders

        # Add content within a fenced code block
        output_lines.append(f"```{lang}")
        if content is not None:
            # Ensure content ends with a newline before the closing fence if it's not empty
            output_lines.append(content.rstrip('\n'))
        output_lines.append("```")
        output_lines.append("") # Add newline after file block


def format_markdown(root: DirectoryInfo) -> str:
    """Formats the directory structure as a Markdown string."""
    #log.info("Formatting output as MARKDOWN...")
    output_lines: List[str] = []
    # Start formatting from the root directory
    _format_markdown_recursive(root, output_lines)
    # Join lines, ensuring a single trailing newline
    return "\n".join(output_lines).strip() + "\n"