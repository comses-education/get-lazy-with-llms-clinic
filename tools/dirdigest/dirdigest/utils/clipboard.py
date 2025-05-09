import pyperclip  # type: ignore[import-untyped]

# Using ignore for import-untyped because pyperclip stubs might not be comprehensive
# or always present, but it's a well-known library.
# Alternatively, add 'pyperclip' to a pyright/mypy include list if using strict type checking.

from dirdigest.utils.logger import logger


def copy_to_clipboard(text: str) -> bool:
    """
    Copies the given text to the system clipboard.

    :param text: The string to copy.
    :return: True if successful, False otherwise.
    """
    if not text:
        logger.debug("Clipboard: No text provided to copy.")
        return False
    try:
        pyperclip.copy(text)
        logger.info("Output copied to clipboard successfully.")
        return True
    except pyperclip.PyperclipException as e:  # Catch specific pyperclip errors
        logger.warning(
            f"Clipboard: Pyperclip could not access the clipboard system: {e}. "
            "This might be due to a missing copy/paste mechanism (e.g., xclip or xsel on Linux). "
            "Please see pyperclip documentation for setup."
        )
        return False
    except Exception as e:  # Catch any other unexpected errors
        logger.warning(
            f"Clipboard: An unexpected error occurred while trying to copy to clipboard: {e}",
            exc_info=True,
        )
        return False


def is_clipboard_available() -> bool:
    """
    Checks if the clipboard functionality seems to be available.
    Tries a benign paste operation.
    """
    try:
        # Pyperclip might raise an error on initialization if no backend is found.
        # Calling a function like paste() is a way to trigger this check.
        pyperclip.paste()  # This might be an empty string or actual content
        return True
    except pyperclip.PyperclipException:
        return False
    except Exception:  # Any other error during this check
        return False
