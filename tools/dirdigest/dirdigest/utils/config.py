import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
import click
from dirdigest.utils.logger import logger

DEFAULT_CONFIG_FILENAME = ".diringest"  # Or .dirdigest, let's stick to requirements


def load_config_file(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Loads configuration from a YAML file.
    If config_path is None, tries to load DEFAULT_CONFIG_FILENAME from the current directory.

    Returns the 'default' profile from the config file, or an empty dict if not found or error.
    The requirements mention profiles, but the CLI doesn't have a --profile flag yet.
    For now, we'll assume the loaded config is either flat or we take the 'default' section.
    Let's assume for now it loads the entire file and CLI args will override.
    The spec says "Command line arguments should override config file settings".
    And example structure has a 'default:' key. Let's prioritize that.
    """
    cfg_path_to_load: Optional[Path] = None

    if config_path:  # User specified a config file
        if config_path.exists() and config_path.is_file():
            cfg_path_to_load = config_path
        else:
            logger.warning(
                f"Config: Specified configuration file not found or not a file: [log.path]{config_path}[/log.path]"
            )
            return {}  # Return empty if specified config is invalid
    else:  # Try default filename in current directory
        default_path = Path.cwd() / DEFAULT_CONFIG_FILENAME
        if default_path.exists() and default_path.is_file():
            cfg_path_to_load = default_path
        # No warning if default config is not found, it's optional.

    if not cfg_path_to_load:
        logger.debug(
            "Config: No configuration file loaded (neither specified nor default found)."
        )
        return {}

    logger.info(
        f"Config: Loading configuration from [log.path]{cfg_path_to_load}[/log.path]"
    )
    try:
        with open(cfg_path_to_load, "r", encoding="utf-8") as f:
            full_config_data = yaml.safe_load(f)
            if not isinstance(full_config_data, dict):
                logger.warning(
                    f"Config: Configuration file [log.path]{cfg_path_to_load}[/log.path] is not a valid YAML dictionary."
                )
                return {}

            # As per requirements example, look for a 'default' profile.
            # If other profiles exist, they are ignored for now unless a --profile CLI arg is added later.
            # If 'default' key doesn't exist, but the file is a flat dict, use it as is.
            if "default" in full_config_data and isinstance(
                full_config_data["default"], dict
            ):
                logger.debug("Config: Loaded 'default' profile.")
                return full_config_data["default"]
            elif "default" not in full_config_data and all(
                not isinstance(v, dict)
                for k, v in full_config_data.items()
                if k not in ["include", "exclude"]
            ):
                # If no 'default' key and it looks like a flat config (no nested dicts other than include/exclude)
                logger.debug(
                    "Config: Loaded as a flat configuration (no 'default' profile found, using root level)."
                )
                return full_config_data
            elif "default" not in full_config_data and any(
                isinstance(v, dict)
                for k, v in full_config_data.items()
                if k != "default"
            ):
                # Has other profile-like structures but no 'default'
                logger.warning(
                    f"Config: File [log.path]{cfg_path_to_load}[/log.path] has profiles but no 'default' profile. No config loaded. Please specify a profile or add a 'default' section."
                )
                return {}
            else:  # No 'default' and not clearly a flat config (e.g. empty or invalid structure)
                logger.debug(
                    f"Config: No 'default' profile found in [log.path]{cfg_path_to_load}[/log.path] or not a simple flat config. Using empty config."
                )
                return {}

    except yaml.YAMLError as e:
        logger.warning(
            f"Config: Error parsing YAML configuration file [log.path]{cfg_path_to_load}[/log.path]: {e}"
        )
        return {}
    except OSError as e:
        logger.warning(
            f"Config: Error reading configuration file [log.path]{cfg_path_to_load}[/log.path]: {e}"
        )
        return {}
    except Exception as e:
        logger.error(
            f"Config: Unexpected error loading configuration from [log.path]{cfg_path_to_load}[/log.path]: {e}",
            exc_info=True,
        )
        return {}


def merge_config(
    cli_args: Dict[str, Any],
    config_file_settings: Dict[str, Any],
    click_context: click.Context,
) -> Dict[str, Any]:
    """
    Merges CLI arguments with settings from a configuration file.
    CLI arguments take precedence if they were explicitly set (not their default).

    :param cli_args: A dictionary of arguments from Click (ctx.params).
    :param config_file_settings: A dictionary of settings loaded from the config file.
    :param click_context: The Click context object (ctx).
    :return: A dictionary of the final merged settings.
    """
    merged_settings = (
        config_file_settings.copy()
    )  # Start with config file settings as base
    logger.debug(f"Config: Initial settings from config file: {config_file_settings}")
    logger.debug(f"Config: CLI args received: {cli_args}")

    for key, cli_value in cli_args.items():
        # Check if the CLI argument was explicitly set by the user,
        # or if it's just the default value defined in Click.
        # We use click.Context.get_parameter_source() for this.
        # This requires Click 8.0+
        source = click_context.get_parameter_source(key)

        param_is_explicitly_set = (
            source is not None and source.name != "DEFAULT"
        )  # Default from click itself
        param_is_default_from_context = (
            source is not None and source.name == "DEFAULT_MAP"
        )  # Default from context obj default_map

        # If the CLI value was explicitly provided by user (not a Click default or context default)
        # OR if the key is not in config_file_settings (so CLI default is better than nothing)
        if param_is_explicitly_set or (
            key not in merged_settings and not param_is_default_from_context
        ):
            # Special handling for 'include' and 'exclude' as they are multiple
            # And CLI can have multiple=True flag, which results in a tuple.
            # Config file might have a list.
            if (
                key in ["include", "exclude"]
                and isinstance(cli_value, tuple)
                and not any(cli_value)
            ):
                # If CLI provided empty tuple (e.g. flag not used), and config has value, prefer config.
                # This might need refinement: if user explicitly says --include '' (empty), it should override.
                # Click's multiple=True gives empty tuple if flag not used.
                # If flag used with empty val, that's different. This logic is tricky.
                # For now: if CLI is empty tuple (flag not used), don't let it override a config list.
                if key in merged_settings:  # If config has this key, let it be.
                    logger.debug(
                        f"Config: CLI {key} is empty tuple (flag not used), keeping config value: {merged_settings[key]}"
                    )
                else:  # Config doesn't have it, CLI is empty tuple, so effectively no value.
                    merged_settings[key] = [] if cli_value == () else cli_value
                    logger.debug(
                        f"Config: CLI {key} is empty tuple, config also no value. Setting to empty list or cli_value."
                    )
            else:
                merged_settings[key] = cli_value
                logger.debug(
                    f"Config: Overriding '{key}' with CLI value: {cli_value} (Source: {source.name if source else 'N/A'})"
                )

    # Normalize include/exclude to always be lists, handling comma-separated strings from config
    for key in ["include", "exclude"]:
        if key in merged_settings:
            current_val = merged_settings[key]
            normalized_patterns: List[str] = []
            if isinstance(
                current_val, str
            ):  # Single comma-separated string from config
                normalized_patterns.extend(
                    p.strip() for p in current_val.split(",") if p.strip()
                )
            elif isinstance(
                current_val, (list, tuple)
            ):  # List from config or tuple from CLI
                for item in current_val:
                    if isinstance(item, str):
                        normalized_patterns.extend(
                            p.strip() for p in item.split(",") if p.strip()
                        )
                    # else: ignore non-string items in list/tuple
            merged_settings[key] = normalized_patterns
            logger.debug(f"Config: Normalized '{key}' to: {merged_settings[key]}")

    logger.debug(f"Config: Final merged settings: {merged_settings}")
    return merged_settings
