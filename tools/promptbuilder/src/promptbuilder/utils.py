import os
import logging
import pyperclip
from pathlib import Path
from typing import Optional, Tuple, Any

# Rich imports
from rich.console import Console  # Still needed for passing to functions and warnings

# prompt_toolkit imports
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.completion import (
    WordCompleter,
    Completer,
    PathCompleter,
)  # <-- Added PathCompleter, Completer
from prompt_toolkit.input.defaults import create_input
from prompt_toolkit.output.defaults import create_output
from prompt_toolkit.application.current import get_app

# Use logger configured in cli.py
logger = logging.getLogger(__name__)


# --- Input Session Setup ---
try:
    ptk_session = PromptSession(
        history=InMemoryHistory(),
        auto_suggest=AutoSuggestFromHistory(),
        input=create_input(),
        output=create_output(),
    )
    # Instantiate PathCompleter once
    path_completer = PathCompleter(expanduser=True)  # expanduser=True handles ~
except Exception as e:
    logger.error(
        f"Failed to initialize prompt_toolkit session: {e}. Input might be degraded.",
        exc_info=True,
    )
    ptk_session = None
    path_completer = None  # Ensure it exists even if session fails


# --- Input Functions using prompt_toolkit ---


# MODIFIED: Added completer argument
def get_single_line_input(
    console: Console,
    prompt_message: str = "",
    default: str = "",
    completer: Optional[Completer] = None,  # <-- Added completer argument
) -> str:
    """Gets single-line input using prompt_toolkit. Re-raises KeyboardInterrupt."""
    if not ptk_session:
        try:
            return input(prompt_message)  # Basic fallback
        except (KeyboardInterrupt, EOFError):
            console.print(f"\n[warning]Input cancelled.[/warning]")
            raise KeyboardInterrupt

    try:
        user_input = ptk_session.prompt(
            prompt_message,
            default=default,
            completer=completer,  # <-- Pass completer to prompt
            complete_while_typing=True,  # <-- Enable completion suggestions while typing
        )
        return user_input.strip() if user_input is not None else default
    except (KeyboardInterrupt, EOFError):
        raise KeyboardInterrupt
    except Exception as e:
        # Check if it's an exception often associated with ESC press (AbortAction)
        if "AbortAction" in str(type(e)):
            raise KeyboardInterrupt
        logger.error(
            f"Error during prompt_toolkit single-line input: {e}", exc_info=True
        )
        console.print(
            f"\n[error]An unexpected error occurred during input: {e}[/error]"
        )
        return default  # Return default on unexpected errors


def get_multiline_input(console: Console, prompt_message: str = "> ") -> str:
    """
    Gets multi-line input using prompt_toolkit PromptSession.
    Users typically finish input by pressing Meta+Enter or Esc -> Enter.
    Re-raises KeyboardInterrupt.
    """
    if not ptk_session:
        # Basic fallback (won't have good editing)
        print(prompt_message)
        lines = []
        try:
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
        except (KeyboardInterrupt, EOFError):
            console.print(f"\n[warning]Input cancelled.[/warning]")
            raise KeyboardInterrupt
        return "\n".join(lines)

    try:
        # The prompt_message (e.g., "> ") will be displayed by prompt_toolkit.
        text = ptk_session.prompt(
            prompt_message,
            multiline=True,
            # wrap_lines=True, # Optional: Wrap long lines visually
        )
        # text can be None if ESC is pressed
        return text if text is not None else ""  # Return empty string on ESC/cancel
    except (KeyboardInterrupt, EOFError):
        # Don't print here, let caller handle exit message
        raise KeyboardInterrupt  # Propagate cancellation
    except Exception as e:
        # Check if it's an exception often associated with ESC press (AbortAction)
        if "AbortAction" in str(type(e)):
            raise KeyboardInterrupt
        logger.error(
            f"Error during prompt_toolkit multi-line input: {e}", exc_info=True
        )
        console.print(
            f"\n[error]An unexpected error occurred during input: {e}[/error]"
        )
        return ""  # Return empty on unexpected errors


# Validator for Confirmation (No change needed)
class YesNoValidator(Validator):
    def validate(self, document):
        text = document.text.lower().strip()
        if text not in ("y", "yes", "n", "no", ""):
            raise ValidationError(
                message='Please enter "y" or "n".',
                cursor_position=len(document.text),
            )


# get_yesno_confirmation (No change needed)
def get_yesno_confirmation(
    console: Console, prompt_message: str, default: bool = True
) -> bool:
    """Gets explicit Yes/No confirmation using prompt_toolkit. Use for critical actions."""
    if not ptk_session:
        try:
            response = (
                input(f"{prompt_message} [{'Y/n' if default else 'y/N'}] ")
                .lower()
                .strip()
            )
            if not response:
                return default
            return response.startswith("y")
        except (KeyboardInterrupt, EOFError):
            console.print(
                f"\n[warning]Confirmation cancelled. Assuming default: {'Yes' if default else 'No'}[/warning]"
            )
            raise KeyboardInterrupt

    suffix = " [Y/n]: " if default else " [y/N]: "
    full_prompt = prompt_message + suffix

    while True:
        try:
            user_input = ptk_session.prompt(
                full_prompt,
                validator=YesNoValidator(),
                completer=WordCompleter(["yes", "no"], ignore_case=True),
                complete_while_typing=False,
            )
            # user_input can be None on ESC
            if user_input is None:
                raise KeyboardInterrupt  # Treat ESC as cancel

            text = user_input.lower().strip()

            if not text:
                return default
            elif text.startswith("y"):
                return True
            elif text.startswith("n"):
                return False
            # Validator should prevent reaching here

        except (KeyboardInterrupt, EOFError):
            # Don't print here, let caller handle
            raise KeyboardInterrupt  # Propagate cancellation
        except Exception as e:
            if "AbortAction" in str(type(e)):
                raise KeyboardInterrupt  # Treat ESC as cancel
            logger.error(
                f"Error during prompt_toolkit confirmation: {e}", exc_info=True
            )
            console.print(
                f"\n[error]An unexpected error occurred during confirmation. Assuming default: {'Yes' if default else 'No'}[/error]"
            )
            return default


# --- Other Utils (No Change Needed In Functionality) ---


def read_text_or_path(
    input_val: Optional[str],
    encoding: str = "utf-8",
    param_name: str = "input",
    console: Optional[Console] = None,
) -> Optional[str]:
    """Reads text directly or from a file path. Logs errors/warnings."""
    if not input_val:
        return None
    try:
        path = Path(input_val)
        if path.is_file():
            logger.debug(
                f"Reading content for '{param_name}' from file: [blue]{path}[/blue]"
            )
            try:
                return path.read_text(encoding=encoding)
            except Exception as e:
                logger.error(
                    f"Error reading file [red]{path}[/red] for '{param_name}': {e}",
                    exc_info=True,
                )
                return None
        else:
            is_likely_path = (
                os.path.sep in input_val or "." in path.name
            ) and not path.is_dir()
            if not path.exists() and is_likely_path:
                logger.warning(
                    f"Input for '{param_name}' looks like a path but does not exist: '[yellow]{input_val}[/yellow]'. Treating as literal text."
                )
            else:
                logger.debug(f"Using literal text for '{param_name}'")
            return input_val
    except Exception as e:
        logger.warning(
            f"Could not interpret input for '{param_name}' as path: '[yellow]{input_val}[/yellow]'. Treating as literal text. Error: {e}"
        )
        return input_val


def save_to_disk(content: str, file_path: Path, console: Console) -> bool:
    """Saves content to the specified file path. Logs messages."""
    logger.info(f"Attempting to save prompt to: [blue]{file_path}[/blue]")
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        console.print(
            f"[green]Prompt successfully saved to {file_path}[/green]"
        )
        return True
    except Exception as e:
        logger.error(
            f"Error writing prompt to file [red]{file_path}[/red]: {e}",
            exc_info=True,
        )
        return False


def copy_to_clipboard(content: str, console: Console) -> bool:
    """Copies content to the system clipboard. Logs messages."""
    try:
        pyperclip.copy(content)
        # Only log success at info level, console print is enough for user feedback
        logger.info("Content copied to clipboard.")
        console.print("[green]Prompt copied to clipboard.[/green]")
        return True
    except pyperclip.PyperclipException as e:
        logger.error(
            f"Could not copy to clipboard: {e}. Is a clipboard utility installed (e.g., xclip, xsel, pbcopy)?"
        )
        # Optionally print to console too if it's a common issue
        # console.print("[yellow]Could not copy to clipboard. Ensure xclip/xsel (Linux) or pbcopy (macOS) is installed.[/yellow]")
        return False
    except Exception as e:
        logger.error(
            f"An unexpected error occurred during clipboard copy: {e}",
            exc_info=True,
        )
        return False


def validate_path_input(
    path_str: str, check_exists: bool = True, console: Optional[Console] = None
) -> Optional[Path]:
    """Validates if a string is a potentially valid path, optionally checking existence."""
    if not path_str:
        return None
    try:
        path = Path(path_str.strip())
        if check_exists and not path.exists():
            # Warning is now only logged, not printed directly by this function
            # Let the caller decide whether to print based on context
            logger.warning(
                f"Path does not exist or is not accessible: [yellow]{path}[/yellow]"
            )
            # console.print(f"[warning]Path does not exist or is not accessible: [yellow]{path}[/yellow]")
        return path
    except Exception as e:
        message = (
            f"Error processing path input '[yellow]{path_str}[/yellow]': {e}"
        )
        # Log error, let caller print user-facing message
        logger.error(message)
        # if console: console.print(f"[error]{message}[/error]")
        return None