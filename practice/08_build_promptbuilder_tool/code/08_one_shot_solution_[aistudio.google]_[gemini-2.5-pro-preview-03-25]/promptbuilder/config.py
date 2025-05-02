import os
import yaml
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

logger = logging.getLogger(__name__)

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
    context_max_file_size_mb: float = 5.0
    context_supported_extensions: List[str] = field(default_factory=lambda: [".txt", ".md", ".py", ".json", ".yaml", ".xml", ".csv", ".html", ".css", ".js"])
    context_encoding: str = "utf-8"
    copy_to_clipboard_default: bool = False
    output_dir: Path = Path(".")
    interactive_multiline_end_marker: str = "END"
    # Add context_mode later if needed
    # context_mode: str = "list" # Example: list, full

    @classmethod
    def load(cls, config_path_override: Optional[str] = None) -> 'Config':
        """Loads configuration from file, merging with defaults."""
        config_path = None
        if config_path_override:
            path = Path(config_path_override)
            if path.is_file():
                config_path = path
            else:
                logger.warning(f"Specified config file not found: {config_path_override}")

        if not config_path:
            for potential_path in CONFIG_SEARCH_PATHS:
                if potential_path.is_file():
                    config_path = potential_path
                    break

        config_data: Dict[str, Any] = {}
        if config_path:
            logger.info(f"Loading configuration from: {config_path}")
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    loaded_yaml = yaml.safe_load(f)
                    if loaded_yaml and isinstance(loaded_yaml, dict):
                         config_data = loaded_yaml
                    else:
                         logger.warning(f"Config file is empty or not a dictionary: {config_path}")
            except yaml.YAMLError as e:
                logger.error(f"Error parsing YAML config file {config_path}: {e}")
            except IOError as e:
                logger.error(f"Error reading config file {config_path}: {e}")
        else:
            logger.info("No config file found, using default settings.")

        # Convert path strings to Path objects and handle potential type errors
        processed_config_data = {}
        for key, value in config_data.items():
            if key in ["default_meta_prompt_template_path", "output_dir"]:
                try:
                    processed_config_data[key] = Path(value) if value else None
                except TypeError:
                     logger.warning(f"Invalid path format for '{key}' in config: {value}. Using default.")
            elif key == "context_supported_extensions":
                 if isinstance(value, list) and all(isinstance(item, str) for item in value):
                     processed_config_data[key] = [ext if ext.startswith('.') else f".{ext}" for ext in value]
                 else:
                     logger.warning(f"Invalid format for 'context_supported_extensions' in config. Expected list of strings. Using default.")
            else:
                processed_config_data[key] = value

        # Create config object, letting dataclass defaults fill in missing keys
        # and overriding defaults with loaded values
        return cls(**processed_config_data)