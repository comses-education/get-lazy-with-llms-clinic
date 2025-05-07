# src/dirdigest/utils.py
import logging
import sys
from pathlib import Path
from typing import Optional

import pyperclip
from rich.console import Console
from rich.logging import RichHandler

log = logging.getLogger(__name__)

console = Console()
log_console = Console(stderr=True)


def setup_logging(verbose: bool):
    """Configures logging using RichHandler, suppressing INFO when testing unless verbose."""
    # --- Test Detection ---
    # Simple check if pytest is running
    is_testing = "pytest" in sys.modules

    # Determine log level
    if verbose:
        log_level = logging.DEBUG
    elif is_testing:
        # Suppress INFO logs during tests unless -v is used
        log_level = logging.WARNING
    else:
        # Default for normal execution
        log_level = logging.INFO
    # --- End Test Detection ---

    # Remove existing handlers to prevent duplicates if called multiple times
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        level=log_level, # Use determined level
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                console=log_console,
                show_level=False,
                show_path=False,
                show_time=False,
                rich_tracebacks=True,
                markup=True,
                # Set level on handler as well to be sure
                level=log_level
            )
        ],
        # Force=True might be needed if basicConfig was called previously implicitly
        # force=True
    )

    if verbose:
        log.debug("Verbose logging enabled.") # This will only show if level is DEBUG


def copy_to_clipboard(text: str) -> bool:
    """Copies text to the system clipboard. Assumes success if no exception."""
    try:
        pyperclip.copy(text)
        # Use log.info - this will be suppressed in tests unless -v
        log.info("Digest copied to clipboard.")
        return True
    except pyperclip.PyperclipException as e:
        log.warning(f"Clipboard access failed: {e}")
        log.warning("Could not copy to clipboard. Ensure 'xclip' or 'xsel' (Linux), "
                    "'pbcopy' (macOS), or appropriate Windows mechanisms are available.")
        return False
    except Exception as e:
        log.error(f"Unexpected error during clipboard operation: {e}", exc_info=True)
        return False


def write_to_file(path: Path, content: str) -> bool:
    """Writes content to the specified file."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        # Use log.info - this will be suppressed in tests unless -v
        log.info(f"Digest written to file: {path}")
        return True
    except OSError as e:
        log.error(f"Error writing to output file {path}: {e}", exc_info=True)
        return False
    except Exception as e:
        log.error(f"Unexpected error writing to file {path}: {e}", exc_info=True)
        return False