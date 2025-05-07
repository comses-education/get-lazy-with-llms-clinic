import os
import yaml
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

# Use the root logger configured in cli.py
logger = logging.getLogger(__name__) # Get logger for this module

DEFAULT_CONFIG_FILENAME = ".promptbuilder.yaml" # Changed to YAML
CONFIG_SEARCH_PATHS = [
    Path(".") / DEFAULT_CONFIG_FILENAME,
    Path.home() / ".config" / "promptbuilder" / DEFAULT_CONFIG_FILENAME,
]

DEFAULT_TEMPLATE_DIR = Path(__file__).parent / "templates"
DEFAULT_TEMPLATE_NAME = "default_meta_prompt.j2"

@dataclass
class Config:
    """Holds configuration settings."""
    default_meta_prompt_template_path: Path = DEFAULT_TEMPLATE_DIR / DEFAULT_TEMPLATE_NAME
    placeholder_format: str = "{{%s}}"
    context_max_file_size_mb: float = 0.3
    context_supported_extensions: List[str] = field(default_factory=lambda: [".txt", ".md", ".py", ".json", ".yaml", ".xml", ".csv", ".html", ".css", ".js"])
    context_encoding: str = "utf-8"
    copy_to_clipboard_default: bool = True
    output_dir: Path = Path(".")

    @classmethod
    def load(cls, config_path_override: Optional[str] = None) -> 'Config':
        """Loads configuration from file, merging with defaults."""
        config_path = None
        if config_path_override:
            path = Path(config_path_override)
            if path.is_file():
                config_path = path
            else:
                logger.warning(f"Specified config file not found: [yellow]{config_path_override}[/yellow]") # Use Rich markup

        if not config_path:
            for potential_path in CONFIG_SEARCH_PATHS:
                if potential_path.is_file():
                    config_path = potential_path
                    break

        config_data: Dict[str, Any] = {}
        if config_path:
            logger.info(f"Loading configuration from: [blue]{config_path}[/blue]") # Use Rich markup
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    loaded_yaml = yaml.safe_load(f)
                    if loaded_yaml and isinstance(loaded_yaml, dict):
                         config_data = loaded_yaml
                         # Remove the old marker if it exists in the loaded config
                         config_data.pop('interactive_multiline_end_marker', None)
                    elif loaded_yaml is not None: # Check if file is not empty but invalid
                         logger.warning(f"Config file is not a dictionary: [yellow]{config_path}[/yellow]")
            except yaml.YAMLError as e:
                logger.error(f"Error parsing YAML config file [red]{config_path}[/red]: {e}")
            except IOError as e:
                logger.error(f"Error reading config file [red]{config_path}[/red]: {e}")
            except Exception as e:
                logger.error(f"Unexpected error loading config [red]{config_path}[/red]: {e}", exc_info=True)
        else:
            logger.info("No config file found or specified, using default settings.")

        # Convert path strings to Path objects and handle potential type errors
        processed_config_data = {}
        for key, value in config_data.items():
            if key in ["default_meta_prompt_template_path", "output_dir"]:
                if value is not None: # Allow empty paths to use default
                    try:
                        processed_config_data[key] = Path(value)
                    except TypeError:
                        logger.warning(f"Invalid path format for '{key}' in config: {value}. Using default.")
                else:
                     processed_config_data[key] = None # Explicitly handle None if needed downstream, else defaults apply

            elif key == "context_supported_extensions":
                 if isinstance(value, list) and all(isinstance(item, str) for item in value):
                     # Ensure extensions start with '.'
                     processed_config_data[key] = list(set([f".{ext.lstrip('.')}" for ext in value])) # Use set for uniqueness
                 else:
                     logger.warning(f"Invalid format for 'context_supported_extensions' in config. Expected list of strings. Using default.")
            # Add checks for other types if needed
            elif key == "context_max_file_size_mb":
                try:
                    processed_config_data[key] = float(value)
                except (ValueError, TypeError):
                    logger.warning(f"Invalid numeric format for 'context_max_file_size_mb': {value}. Using default.")
            elif key == "copy_to_clipboard_default":
                if isinstance(value, bool):
                    processed_config_data[key] = value
                else:
                    logger.warning(f"Invalid boolean format for 'copy_to_clipboard_default': {value}. Using default.")
            else:
                # Include other valid keys directly
                 if key in cls.__annotations__: # Check if it's a known field before adding
                     processed_config_data[key] = value
                 else:
                     logger.debug(f"Ignoring unknown configuration key: '{key}'")


        # Create config object, letting dataclass defaults fill in missing keys
        # and overriding defaults with loaded values
        # Filter processed data to only include keys defined in the dataclass
        valid_keys = {k for k in cls.__annotations__}
        filtered_config_data = {k: v for k, v in processed_config_data.items() if k in valid_keys}

        return cls(**filtered_config_data)