# dirdigest/dirdigest/utils/logger.py
import logging
import sys
from pathlib import Path  # Added for type hint of log_file_path
from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme

# Global console instances
stdout_console = Console(file=sys.stdout)
stderr_console = Console(
    stderr=True,
    theme=Theme(
        {
            "logging.level.debug": "dim cyan",
            "logging.level.info": "dim blue",  # Adjusted for better visibility if needed
            "logging.level.warning": "magenta",
            "logging.level.error": "bold red",
            "logging.level.critical": "bold red reverse",
            "log.included": "green",
            "log.excluded": "red",
            "log.reason": "dim yellow",
            "log.path": "cyan",
            "log.summary_key": "bold",
            "log.summary_value_inc": "bold green",
            "log.summary_value_exc": "bold red",
            "log.summary_value_neutral": "bold blue",
        }
    ),
)

# Global logger instance for the application
logger = logging.getLogger("dirdigest")


def setup_logging(
    verbose_level: int, quiet: bool, log_file_path: Path | None = None
) -> None:  # Changed type hint for log_file_path
    """
    Configures logging for the application using RichHandler for console
    and an optional FileHandler for file-based logging.

    The main logger is set to DEBUG, allowing fine-grained control by handlers.

    :param verbose_level: 0 (default for console: WARNING), 1 (-v for console: INFO), 2 (-vv for console: DEBUG)
    :param quiet: If True, suppresses console output below ERROR.
    :param log_file_path: Optional pathlib.Path to a file for logging (will log at DEBUG level).
    """
    # Set the main logger to the lowest level we want to handle globally (DEBUG)
    # Individual handlers will then filter what they output from this stream.
    logger.setLevel(logging.DEBUG)

    # Determine console log level based on verbosity/quietness
    if quiet:
        console_log_level_name = "ERROR"
    elif verbose_level >= 2:  # -vv or more
        console_log_level_name = "DEBUG"
    elif verbose_level >= 1:  # -v
        console_log_level_name = "INFO"
    else:  # Default operation (no -v, no -q)
        console_log_level_name = "WARNING"  # Default console logs warnings and above

    # Remove any existing handlers to prevent duplicate logs if setup_logging is called multiple times
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()  # Close the handler before removing

    # --- Console Handler (Rich) ---
    # This handler's level determines what from the DEBUG-level logger stream gets to the console.
    console_handler = RichHandler(
        console=stderr_console,
        level=logging.getLevelName(
            console_log_level_name
        ),  # Set handler level from determined name
        show_time=False,  # Keep console logs concise
        show_path=False,  # Path is usually part of the message or not needed for console
        markup=True,  # Enable Rich markup in log messages
        rich_tracebacks=True,  # Use Rich for formatting tracebacks
        log_time_format="[%X]",  # Example: [14:30:59] if show_time=True
    )
    logger.addHandler(console_handler)

    # --- File Handler (if log_file_path is provided) ---
    if log_file_path:
        try:
            # Ensure the directory for the log file exists if it's in a subdirectory
            log_file_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(
                str(log_file_path), mode="w", encoding="utf-8"
            )
            # File handler can have its own level, e.g., always DEBUG for the file
            file_handler.setLevel(logging.DEBUG)

            # Use a more standard, detailed format for file logs
            file_formatter = logging.Formatter(
                fmt="%(asctime)s - %(levelname)-8s - %(name)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
            file_logging_status = f"Enabled to '{str(log_file_path)}' at DEBUG level"
        except Exception as e:
            # If file logging setup fails, log an error to the console logger and continue without file logging
            logger.error(
                f"Failed to initialize file logging to '{str(log_file_path)}': {e}",
                exc_info=False,
            )  # exc_info=False to avoid traceback for this specific config error
            file_logging_status = f"FAILED to enable for '{str(log_file_path)}'"

    else:
        file_logging_status = "Disabled"

    # This initial debug message will go to handlers that accept DEBUG
    # (i.e., the file handler by default, and console if -vv)
    logger.debug(
        f"Logging initialized. Main logger level: DEBUG. "
        f"Console handler effective level: {console_log_level_name}. "
        f"File logging: {file_logging_status}"
    )


# No need for example usage here as this module is for setup.
# Other modules will import 'logger' from this file.
