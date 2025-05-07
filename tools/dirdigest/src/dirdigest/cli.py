# src/dirdigest/cli.py (Corrected Argument Parsing)

import logging
import sys
from pathlib import Path
from typing import Optional, Tuple, List # Added List

import click

# To use rich-click for help formatting, uncomment the next line
# import rich_click as click
# And replace @click.command(...) with @click.command(cls=click.RichGroup) # Use RichGroup if using rich-click
# Ensure rich-click is added to pyproject.toml dependencies

from . import __version__
from .config import DEFAULT_CONFIG, get_effective_config
from .core import generate_digest
from .utils import console, copy_to_clipboard, setup_logging, write_to_file

log = logging.getLogger(__name__)

# --- Helper function to split comma-separated args ---
def _split_comma_separated_args(args_tuple: Tuple[str, ...]) -> List[str]:
    """Splits strings within a tuple by commas and flattens the list."""
    final_list = []
    for item in args_tuple:
        # Split by comma, strip whitespace from each part, filter out empty strings
        split_items = [part.strip() for part in item.split(',') if part.strip()]
        final_list.extend(split_items)
    return final_list
# --- End Helper ---


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(__version__, '-V', '--version', package_name='dirdigest')
@click.argument(
    "directory",
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, readable=True, path_type=Path
    ),
    default=".",
)
@click.option(
    "-o", "--output",
    type=click.Path(file_okay=True, dir_okay=False, writable=True, path_type=Path),
    default=None,
    help="File path to write the digest to. Output is *also* copied to clipboard by default.",
)
@click.option(
    "--include",
    type=str,
    multiple=True,
    metavar="PATTERN",
    help="Glob pattern(s) to include. Separate multiple patterns with commas OR use the flag multiple times.", # Updated help
)
@click.option(
    "--exclude",
    type=str,
    multiple=True,
    metavar="PATTERN",
    help="Glob pattern(s) to exclude. Separate multiple patterns with commas OR use the flag multiple times.", # Updated help
)
@click.option(
    "--max-size",
    type=click.IntRange(min=0),
    default=None,
    metavar="KB",
    help=f"Max file size in KB to include content for. Default from config/default: {DEFAULT_CONFIG['max_size']} KB.",
)
@click.option(
    "--no-default-ignore",
    is_flag=True,
    default=False,
    help="Disable default exclusion patterns.",
)
@click.option(
    "-f", "--format",
    type=click.Choice(['markdown', 'json'], case_sensitive=False),
    default=None,
    help=f"Output format for the digest. Default from config/default: {DEFAULT_CONFIG['format']}.",
)
@click.option(
    "--clipboard/--no-clipboard",
    "clipboard_flag",
    is_flag=True,
    default=True, # Default to True (copy to clipboard)
    help="Copy output to clipboard (default) / Disable clipboard copy.",
)
@click.option(
    "-v", "--verbose",
    is_flag=True,
    default=None, # Let config merging handle the final boolean value
    help="Enable verbose (DEBUG level) logging output.",
)
def cli_entry(
    directory: Path,
    output: Optional[Path],
    include: Tuple[str, ...], # Original tuple from click
    exclude: Tuple[str, ...], # Original tuple from click
    max_size: Optional[int],
    no_default_ignore: bool,
    format: Optional[str],
    clipboard_flag: bool, # Will be True or False based on flag/default
    verbose: Optional[bool], # Will be True if -v used, None otherwise
):
    """
    dirdigest: Generate Markdown or JSON digests of directory contents.

    Recursively scans a directory, filters files based on patterns and size,
    reads text content, and outputs a consolidated digest suitable for LLMs.

    Default behavior copies the digest to the clipboard. Use --no-clipboard to disable.
    If -o is specified, writes to file *and* copies to clipboard (unless disabled).

    Example:

        dirdigest . --exclude '*.log,*.tmp' --include '*.py' # Use commas
        dirdigest . --exclude '*.log' --exclude '*.tmp'      # Use multiple flags
    """
    # *** Validation ***
    resolved_dir: Path
    try:
        resolved_dir = directory.resolve(strict=True)
        if not resolved_dir.is_dir():
            # Use click.echo for consistency, respects testing redirects better
            click.echo(f"Error: Path '{directory}' is not a directory.", file=sys.stderr)
            sys.exit(2)
    except FileNotFoundError:
        click.echo(f"Error: Path '{directory}' does not exist.", file=sys.stderr)
        sys.exit(2)
    except PermissionError as e:
        click.echo(f"Error: Permission error accessing directory '{directory}': {e}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        click.echo(f"Error: OS error accessing directory '{directory}': {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: Unexpected error validating directory '{directory}': {e}", file=sys.stderr)
        sys.exit(1)
    # *** END Explicit Validation ***


    # --- Process Include/Exclude Args ---
    # Split comma-separated patterns received from Click
    processed_include = _split_comma_separated_args(include)
    processed_exclude = _split_comma_separated_args(exclude)
    # --- End Processing ---


    # --- Configuration and Logging Setup ---
    # Use the processed lists for configuration
    cli_args = {
        "output": output,
        "include": processed_include or None, # Use None if list is empty after split
        "exclude": processed_exclude or None, # Use None if list is empty after split
        "max_size": max_size,
        "no_default_ignore": no_default_ignore, # Will be True or False
        "format": format,
        "clipboard": clipboard_flag, # Will be True or False
        "verbose": verbose, # Will be True or None
    }

    # Filter out None values *except* for 'output', as None means stdout/clipboard context
    # Flags like 'no_default_ignore' and 'clipboard' are already boolean T/F
    # 'verbose' will be included only if it's True (i.e., -v was used)
    cli_args_filtered = {
        k: v for k, v in cli_args.items()
        if v is not None or k == "output"
    }

    # Get effective config (CLI overrides file overrides defaults)
    effective_config = get_effective_config(cli_args_filtered, Path.cwd())

    # Setup logging based on the FINAL merged configuration
    setup_logging(effective_config.get("verbose", False))
    log.debug(f"dirdigest version: {__version__}")
    log.debug(f"Effective configuration: {effective_config}")
    log.debug(f"Input directory: {resolved_dir}")
    # Log the patterns *after* splitting and merging if desired
    log.debug(f"Effective include patterns: {effective_config.get('include', [])}")
    log.debug(f"Effective exclude patterns: {effective_config.get('exclude', [])} (User provided)")
    if effective_config.get('default_ignore', True):
        log.debug(f"Default exclude patterns are active.")


    # --- Determine Final Clipboard Behavior ---
    # Use the final config value which respects CLI > File > Default
    use_clipboard = effective_config.get("clipboard", True) # Default true if missing
    log.debug(f"Clipboard copy requested/final: {use_clipboard}")

    # --- Generate Digest ---
    # Pass the effective config which now contains correctly split lists
    digest_content = generate_digest(resolved_dir, effective_config)

    if digest_content is None:
        log.error("Digest generation failed (see previous errors).")
        sys.exit(1)

    # --- Handle Output ---
    file_written = False
    clipboard_copied = False
    stdout_printed = False

    # 1. File Output (if requested by CLI - check original 'output' variable)
    if output:
        log.debug(f"Attempting to write to file: {output}")
        if write_to_file(output, digest_content):
            file_written = True
        else:
            # Make file write failure critical if explicitly requested via CLI
            log.error(f"Critical Failure: Failed to write digest to file: {output}")
            sys.exit(1) # Exit if file writing fails when requested

    # 2. Clipboard Output (if not disabled in final config)
    if use_clipboard:
        log.debug("Attempting to copy to clipboard.")
        if copy_to_clipboard(digest_content):
            clipboard_copied = True
        else:
            log.warning("Failed to copy digest to clipboard.")
            # Fallback to stdout ONLY IF no file was written
            if not file_written: # Check if -o was used and successful
                 log.info("Falling back to stdout due to clipboard failure.")
                 # Use console.print which is configured by utils
                 console.print(digest_content)
                 stdout_printed = True

    # 3. Stdout Output (only if no file AND clipboard was disabled)
    # Check if CLI requested a file and if clipboard ended up disabled
    if not output and not use_clipboard:
         log.debug("Printing output to stdout (file not specified and clipboard explicitly disabled).")
         console.print(digest_content)
         stdout_printed = True

    # --- Final Status Logging ---
    if file_written and clipboard_copied:
         log.info(f"Digest written to {output} and copied to clipboard.")
    elif file_written: # Implies clipboard was disabled or failed silently (shouldn't happen with exit logic?)
         log.info(f"Digest written to {output}.") # Assume clipboard was disabled
    elif clipboard_copied: # Implies no -o was used
         # Log message already printed by copy_to_clipboard
         pass
    elif stdout_printed: # Implies fallback or (--no-clipboard and no -o)
         log.info("Digest printed to stdout.")
    else:
        # This case should only be reached if -o was specified but failed (already exited)
        # or if generation failed (already exited).
        # If code reaches here with no action, it's unexpected.
        log.warning("No definitive output action (file write/clipboard copy/stdout print) was completed.")


    log.info("dirdigest finished successfully")
    sys.exit(0)


if __name__ == "__main__":
    cli_entry()