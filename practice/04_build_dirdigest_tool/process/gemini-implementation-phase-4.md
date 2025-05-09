Fantastic! Let's get to actually *seeing* some beautiful (or beautifully structured) output.

**Phase 4: Output Generation**

This phase involves creating the formatters for JSON and Markdown and integrating them into the CLI.

**Step 4.1: Formatter Interface (`formatter.py`)**

Create/Update `dirdigest/dirdigest/formatter.py`:

```python
# dirdigest/dirdigest/formatter.py
import json
import datetime
from pathlib import Path
from typing import Any, Dict, List # Changed from dict, list to Dict, List

from dirdigest.constants import TOOL_VERSION # Import TOOL_VERSION
from dirdigest.core import DigestItemNode # Import the type hint

# Define a common structure for metadata earlier if not already defined elsewhere
Metadata = Dict[str, Any]


class BaseFormatter:
    """Base class for output formatters."""
    def __init__(self, base_dir_path: Path, cli_metadata: Metadata):
        """
        Initialize the formatter.
        cli_metadata contains stats collected by core.build_digest_tree
        """
        self.base_dir_path = base_dir_path
        self.core_metadata = cli_metadata # Metadata from build_digest_tree
        self.final_metadata: Metadata = self._prepare_final_metadata()

    def _prepare_final_metadata(self) -> Metadata:
        """Prepares the full metadata object for the output."""
        # Start with metadata from core (counts, sizes)
        meta = dict(self.core_metadata) # Make a copy
        meta["tool_version"] = TOOL_VERSION
        meta["created_at"] = datetime.datetime.now().isoformat()
        # base_directory is already in core_metadata
        return meta

    def format(self, data_tree: DigestItemNode) -> str:
        """
        Formats the data_tree into a string representation.
        data_tree is the root node from core.build_digest_tree.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def _get_file_extension(self, file_path: str) -> str:
        """Helper to get file extension for language hints."""
        return Path(file_path).suffix.lstrip('.').lower()

    def _generate_directory_structure_string(self, node: DigestItemNode, indent: str = "", base_path_len: int = 0) -> List[str]:
        """
        Helper to generate a text-based directory tree for Markdown.
        Adjusted to handle the structure from build_digest_tree.
        """
        lines = []
        # For the root node, its 'relative_path' is '.', display it as such.
        # For children, display their actual name part.
        node_display_name = Path(node["relative_path"]).name if node["relative_path"] != "." else "."
        
        lines.append(f"{indent}{node_display_name}")

        if node["type"] == "folder" and "children" in node and node["children"]:
            # Determine prefix for children based on current node
            # For all but the last child, use "├── ", for the last one, use "└── "
            # For the indent of children, use "│   " or "    "
            
            # Sort children to ensure consistent tree output (already sorted by build_digest_tree)
            # children_sorted = sorted(node["children"], key=lambda x: x["relative_path"])
            children_sorted = node["children"]

            for i, child_node in enumerate(children_sorted):
                is_last = (i == len(children_sorted) - 1)
                prefix = "└── " if is_last else "├── "
                child_indent_ pokračovanie = "    " if is_last else "│   " # continuation indent
                
                # The child's display name should be its own name, not the full relative path here
                child_display_name = Path(child_node["relative_path"]).name
                
                if child_node["type"] == "folder":
                    lines.append(f"{indent}{prefix}{child_display_name}/")
                    lines.extend(self._generate_directory_structure_string(child_node, indent + child_indent_pokračovanie))
                else: # file
                    lines.append(f"{indent}{prefix}{child_display_name}")
        return lines

    def _collect_file_contents_for_markdown(self, node: DigestItemNode, files_list: List) -> None:
        """
        Recursively collects file paths and contents for Markdown output.
        Ensures files are collected in a sorted order (traversal order).
        """
        if node["type"] == "file" and "content" in node and node["content"] is not None:
            files_list.append({
                "relative_path": node["relative_path"],
                "content": node["content"],
                "lang_hint": self._get_file_extension(node["relative_path"])
            })
        elif node["type"] == "file" and node.get("read_error"):
            files_list.append({
                "relative_path": node["relative_path"],
                "content": f"Error reading file: {node['read_error']}",
                "lang_hint": "text" # Or no hint
            })


        if node["type"] == "folder" and "children" in node:
            # Children are already sorted by build_digest_tree
            for child in node["children"]:
                self._collect_file_contents_for_markdown(child, files_list)
```
*Self-correction:*
*   `TOOL_VERSION` imported from `constants`.
*   `DigestItemNode` imported from `core`.
*   Changed `dict` and `list` to `Dict` and `List` for type hints.
*   Constructor now takes `base_dir_path` and `cli_metadata` (which is what `build_digest_tree` returns as `metadata_from_core`).
*   `_prepare_final_metadata` populates common metadata fields.
*   `_generate_directory_structure_string` adjusted to better reflect the tree structure with prefixes. Display name logic for nodes is improved.
*   `_collect_file_contents_for_markdown` added to recursively gather file data for the "Contents" section. It handles files with read errors.

**Step 4.2: JSON Formatter (`formatter.py`)**

Add to `dirdigest/dirdigest/formatter.py`:

```python
# ... (after BaseFormatter) ...

class JsonFormatter(BaseFormatter):
    """Formats the directory digest as JSON."""

    def format(self, data_tree: DigestItemNode) -> str:
        """
        Generates a JSON string representation of the directory digest.
        data_tree is the root_node from core.build_digest_tree.
        """
        output_data = {
            "metadata": self.final_metadata,
            "root": data_tree
        }
        
        def default_serializer(obj):
            if isinstance(obj, Path): # Should not be in data_tree, but good for metadata
                return str(obj)
            raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

        return json.dumps(output_data, indent=2, default=default_serializer)

```

**Step 4.3: Markdown Formatter (`formatter.py`)**

Add to `dirdigest/dirdigest/formatter.py`:

```python
# ... (after JsonFormatter) ...

class MarkdownFormatter(BaseFormatter):
    """Formats the directory digest as Markdown."""

    def format(self, data_tree: DigestItemNode) -> str:
        """
        Generates a Markdown string representation of the directory digest.
        data_tree is the root_node from core.build_digest_tree.
        """
        md_lines = []

        # 1. Header Section
        md_lines.append(f"# Directory Digest: {self.final_metadata['base_directory']}")
        md_lines.append(f"\n*Generated by dirdigest v{self.final_metadata['tool_version']} on {self.final_metadata['created_at']}*")
        md_lines.append(f"*Included files: {self.final_metadata['included_files_count']}, Total content size: {self.final_metadata['total_content_size_kb']:.2f} KB*")
        # Add excluded_files_count when available
        md_lines.append("\n---")

        # 2. Directory Structure Visualization
        md_lines.append("\n## Directory Structure")
        # The root node itself ('relative_path': '.') shouldn't have a prefix like '├──'
        # The _generate_directory_structure_string starts with the name of the node.
        # We need to pass the root node directly to the helper.
        structure_lines = self._generate_directory_structure_string(data_tree)
        md_lines.append("\n```text") # Use text to avoid markdown interpreting it
        md_lines.extend(structure_lines)
        md_lines.append("```\n")
        md_lines.append("\n---")


        # 3. File Contents
        md_lines.append("\n## Contents")
        
        collected_files: List[Dict[str, Any]] = []
        self._collect_file_contents_for_markdown(data_tree, collected_files)

        if not collected_files:
            md_lines.append("\n*No files with content to display.*")
        else:
            for file_info in collected_files:
                md_lines.append(f"\n### `./{file_info['relative_path']}`") # Ensure ./ prefix
                lang_hint = file_info['lang_hint'] if file_info['lang_hint'] else ""
                md_lines.append(f"```{lang_hint}")
                md_lines.append(file_info['content'])
                md_lines.append("```")
        
        md_lines.append("\n") # Trailing newline for cleanliness
        return "\n".join(md_lines)

```
*Self-correction in `MarkdownFormatter`:*
*   Added a line for included files count and total size in metadata.
*   The `_generate_directory_structure_string` was slightly complex; simplified its call. It should create a nice text tree. Wrapped it in ` ```text ... ``` `.
*   Used `_collect_file_contents_for_markdown` to gather files and then iterate, ensuring correct order and handling of files with read errors for the content section. Added `./` prefix for file paths.

**Step 4.4: Integrate Formatters in CLI (`cli.py`)**

Modify `dirdigest/dirdigest/cli.py`:

```python
# dirdigest/dirdigest/cli.py
import click
import sys
import pathlib
import datetime # For formatter metadata if not fully handled by formatter

from dirdigest.constants import TOOL_NAME, TOOL_VERSION
from dirdigest import core
from dirdigest import formatter as dirdigest_formatter # Alias to avoid conflict with 'format' variable

# ... (click command and options - no changes here) ...

def main_cli(
    directory: pathlib.Path,
    output: click.utils.LazyFile,
    format: str, # Name of the format (json or markdown)
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    max_size: int,
    max_depth: int | None,
    no_default_ignore: bool,
    follow_symlinks: bool,
    ignore_errors: bool,
    clipboard: bool,
    verbose: int,
    quiet: bool,
    log_file: pathlib.Path | None,
    config: pathlib.Path | None
):
    # ... (parsing include/exclude, temporary logging setup - no changes here) ...
    # ... (CLI parameter echoes - no changes here) ...

    processed_items_generator = core.process_directory_recursive(
        base_dir_path=directory,
        include_patterns=parsed_include_patterns,
        exclude_patterns=parsed_exclude_patterns,
        no_default_ignore=no_default_ignore,
        max_depth=max_depth,
        follow_symlinks=follow_symlinks,
        max_size_kb=max_size,
        ignore_read_errors=ignore_errors
    )

    if core.log_level in ["INFO", "DEBUG"]:
        click.echo(f"CLI: Building digest tree...")
    
    root_node, metadata_from_core = core.build_digest_tree(directory, processed_items_generator)

    if core.log_level in ["INFO", "DEBUG"]:
        click.echo(f"CLI: Digest tree built. Root node children: {len(root_node.get('children',[]))}")
        click.echo(f"CLI: Metadata from core: {metadata_from_core}")

    # --- Actual Output Generation ---
    selected_formatter: dirdigest_formatter.BaseFormatter
    if format.lower() == 'json':
        selected_formatter = dirdigest_formatter.JsonFormatter(directory, metadata_from_core)
    elif format.lower() == 'markdown':
        selected_formatter = dirdigest_formatter.MarkdownFormatter(directory, metadata_from_core)
    else:
        # This case should ideally be prevented by click.Choice
        click.echo(f"CLI: Error: Unknown format '{format}'. Defaulting to Markdown.", err=True)
        selected_formatter = dirdigest_formatter.MarkdownFormatter(directory, metadata_from_core)

    if core.log_level in ["INFO", "DEBUG"]:
        click.echo(f"CLI: Formatting output as {format.upper()}...")
    
    try:
        final_output_str = selected_formatter.format(root_node)
        output.write(final_output_str)
        if output != sys.stdout: # If writing to a file
             if core.log_level in ["INFO", "DEBUG"] or not quiet: # Print if verbose or not quiet
                click.echo(f"CLI: Digest successfully written to {output.name}")
    except Exception as e:
        click.echo(f"CLI: Error during output formatting or writing: {e}", err=True)
        # Potentially re-raise or exit with error code
        # For now, just log and continue to clipboard stage if applicable
        final_output_str = f"Error generating output: {e}" # For clipboard

    # --- Clipboard (Phase 6, but let's put placeholder logic here) ---
    if clipboard:
        if core.log_level in ["INFO", "DEBUG"] and final_output_str and "Error generating output" not in final_output_str :
            click.echo("CLI: Clipboard copy would happen here.")
        # actual clipboard copy will be added in Phase 6 involving utils.clipboard

    # --- Debug print for generated data tree (if -vv) ---
    if core.log_level == "DEBUG":
        import json as json_debugger # Avoid conflict
        def json_default_serializer(obj):
            if isinstance(obj, pathlib.Path): return str(obj)
            return f"<not serializable: {type(obj).__name__}>"
        click.echo("CLI: --- Generated Data Tree (Debug from CLI) ---")
        try:
            click.echo(json_debugger.dumps(root_node, indent=2, default=json_default_serializer))
        except TypeError as e:
            click.echo(f"CLI: Error serializing data tree to JSON for debug: {e}")
        click.echo("CLI: --- End Generated Data Tree ---")


if __name__ == '__main__':
    main_cli()
```
**Changes in `cli.py`:**
*   Imported `formatter` as `dirdigest_formatter`.
*   Instantiated the correct formatter (`JsonFormatter` or `MarkdownFormatter`) based on the `--format` option. It passes `directory` (for `base_dir_path`) and `metadata_from_core` to the formatter constructor.
*   Called `selected_formatter.format(root_node)` to get the output string.
*   Wrote the `final_output_str` to the `output` (which is `sys.stdout` or the specified file).
*   Added a success message if writing to a file.
*   Basic error handling around formatting/writing.
*   Moved the debug JSON print to the end, as it's just for debugging the tree.

**Verification for Phase 4:**

1.  Ensure your environment is up-to-date (`uv pip install -e .`).
2.  Test with your `my_test_dir`:
    *   `dirdigest ./my_test_dir/` (should output Markdown to stdout)
    *   `dirdigest ./my_test_dir/ -o digest.md` (should write Markdown to `digest.md`)
    *   `dirdigest ./my_test_dir/ -f json` (should output JSON to stdout)
    *   `dirdigest ./my_test_dir/ -f json -o digest.json` (should write JSON to `digest.json`)
    *   `dirdigest ./my_test_dir/ -i "pseudo_binary.bin" --ignore-errors -f markdown` (check how the error is displayed in Markdown)
    *   `dirdigest ./my_test_dir/ -i "pseudo_binary.bin" --ignore-errors -f json` (check how the error is represented in JSON)
3.  Inspect the contents of `digest.md` and `digest.json`:
    *   **JSON**: Should match the schema: `metadata` object and `root` object with nested children. Files should have `relative_path`, `type`, `size_kb`, and `content` (or `read_error`).
    *   **Markdown**: Should have the header, directory structure tree, and then file contents in code blocks with language hints. Errored files should indicate the error.

This is a major milestone! The core functionality of producing the digest in both formats should now be working.

After you verify this, we'll move on to Phase 5: Logging and Reporting (making the console output much nicer with Rich, proper log levels, log file, etc.).