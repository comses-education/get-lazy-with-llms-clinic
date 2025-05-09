import os
import logging
import pyperclip
from pathlib import Path
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

def read_text_or_path(input_val: Optional[str], encoding: str = 'utf-8', param_name: str = "input") -> Optional[str]:
    """Reads text directly or from a file path."""
    if not input_val:
        return None
    path = Path(input_val)
    if path.is_file():
        logger.debug(f"Reading content for '{param_name}' from file: {path}")
        try:
            return path.read_text(encoding=encoding)
        except FileNotFoundError:
            logger.error(f"File not found for '{param_name}': {path}")
            return None
        except IOError as e:
            logger.error(f"Error reading file {path} for '{param_name}': {e}")
            return None
        except UnicodeDecodeError as e:
            logger.error(f"Error decoding file {path} with encoding '{encoding}' for '{param_name}': {e}")
            return None
    else:
        # Check if it *looks* like a path but doesn't exist
        # Heuristic: contains path separators or common extensions but isn't a valid file
        if (os.path.sep in input_val or any(input_val.endswith(ext) for ext in ['.txt', '.md', '.py'])) and not path.exists():
             logger.warning(f"Input '{input_val}' for '{param_name}' looks like a path but does not exist. Treating as literal text.")
        logger.debug(f"Using literal text for '{param_name}'")
        return input_val # Treat as literal string

def save_to_disk(content: str, file_path: Path) -> bool:
    """Saves content to the specified file path."""
    logger.info(f"Attempting to save prompt to: {file_path}")
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding='utf-8')
        logger.info(f"Prompt successfully saved to {file_path}")
        return True
    except IOError as e:
        logger.error(f"Error writing prompt to file {file_path}: {e}")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred while saving to {file_path}: {e}")
        return False


def copy_to_clipboard(content: str) -> bool:
    """Copies content to the system clipboard."""
    try:
        pyperclip.copy(content)
        logger.info("Prompt copied to clipboard.")
        return True
    except pyperclip.PyperclipException as e:
        logger.error(f"Could not copy to clipboard: {e}. Is a clipboard utility installed (e.g., xclip, xsel, pbcopy)?")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred during clipboard copy: {e}")
        return False

def get_multiline_input(prompt_message: str, end_marker: str) -> str:
    """Gets multi-line input from the user until end_marker is entered."""
    lines = []
    print(f"{prompt_message} (Enter '{end_marker}' on a new line to finish):")
    while True:
        try:
            line = input()
            if line.strip().upper() == end_marker.upper():
                break
            lines.append(line)
        except EOFError: # Handle Ctrl+D
            break
    return "\n".join(lines)

def validate_path_input(path_str: str, check_exists: bool = True) -> Optional[Path]:
    """Validates if a string is a potentially valid path."""
    if not path_str:
        return None
    try:
        path = Path(path_str.strip())
        if check_exists and not path.exists():
             print(f"Warning: Path does not exist: {path}")
             # Allow non-existent paths for output saving initially
             # return None # Or decide to return the path anyway
        return path
    except Exception as e:
        print(f"Error processing path '{path_str}': {e}")
        return None