# src/dirdigest/__main__.py (Modified)
"""Allows running the CLI via `python -m dirdigest`."""

import sys
from .cli import cli_entry # Import the new combined function

if __name__ == "__main__":
    # Execute the main Click command/entry point
    # Pass prog_name if needed by Click for help messages, though often inferred
    sys.exit(cli_entry(prog_name="dirdigest"))