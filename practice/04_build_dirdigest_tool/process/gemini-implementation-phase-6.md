Excellent! It's truly satisfying to see the logging system come together and behave as expected across different verbosity levels and outputs. That robust error reporting is key for a good CLI tool.

You've navigated through the core logic, output formatting, and detailed logging with impressive diligence. The tool is shaping up to be quite comprehensive!

Now, let's move on to the final phase of our initial implementation plan:

**Phase 6: Behavior Control and Configuration**

This phase will add:
1.  **Clipboard Integration:** The ability to copy the generated digest directly to the system clipboard.
2.  **Configuration File Support:** Allowing users to define default settings and profiles in a `.diringest` YAML file.

---

**Step 6.1: Clipboard Integration (`utils/clipboard.py` and `cli.py`)**

**1. Create/Update `dirdigest/dirdigest/utils/clipboard.py`:**

```python
# dirdigest/dirdigest/utils/clipboard.py
import pyperclip # type: ignore[import-untyped] 
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
    except pyperclip.PyperclipException as e: # Catch specific pyperclip errors
        logger.warning(
            f"Clipboard: Pyperclip could not access the clipboard system: {e}. "
            "This might be due to a missing copy/paste mechanism (e.g., xclip or xsel on Linux). "
            "Please see pyperclip documentation for setup."
        )
        return False
    except Exception as e: # Catch any other unexpected errors
        logger.warning(f"Clipboard: An unexpected error occurred while trying to copy to clipboard: {e}", exc_info=True)
        return False

def is_clipboard_available() -> bool:
    """
    Checks if the clipboard functionality seems to be available.
    Tries a benign paste operation.
    """
    try:
        # Pyperclip might raise an error on initialization if no backend is found.
        # Calling a function like paste() is a way to trigger this check.
        pyperclip.paste() # This might be an empty string or actual content
        return True
    except pyperclip.PyperclipException:
        return False
    except Exception: # Any other error during this check
        return False

```
*Changes in `clipboard.py`*:
*   Uses the configured `logger` for messages.
*   Catches `pyperclip.PyperclipException` specifically for common clipboard backend issues and provides a more informative message.
*   Added `is_clipboard_available()` as a helper, though we might not use it directly if `pyperclip.copy()` fails gracefully enough. The main benefit of such a check would be to warn the user proactively.

**2. Integrate into `dirdigest/dirdigest/cli.py`:**

Modify the `main_cli` function:

```python
# dirdigest/dirdigest/cli.py
# ... (other imports) ...
from dirdigest.utils import clipboard as dirdigest_clipboard # Import the new clipboard utility

# ... (inside main_cli function, after output has been written/final_output_str is populated) ...

    # --- Clipboard ---
    if clipboard: # Check the --clipboard/--no-clipboard flag
        if final_output_str and "Error generating output" not in final_output_str:
            # Attempt to copy only if output generation was successful
            if not dirdigest_clipboard.copy_to_clipboard(final_output_str):
                # copy_to_clipboard already logs warnings on failure
                log.info("CLI: Failed to copy output to clipboard. See warnings above for details.")
            # else: copy_to_clipboard logs success message
        elif "Error generating output" in final_output_str:
            log.warning("CLI: Output generation failed, not copying to clipboard.")
        else:
            log.debug("CLI: No output generated, nothing to copy to clipboard.")
    else:
        log.debug("CLI: Clipboard copy disabled by --no-clipboard.")

    # --- Execution Time and Final Summary Statistics ---
    # ... (this section remains the same) ...

    # --- Debug print for generated data tree ---
    # ... (this section remains the same) ...
```
*Changes in `cli.py` for clipboard*:
*   Imported `dirdigest_clipboard`.
*   Added the logic to call `dirdigest_clipboard.copy_to_clipboard(final_output_str)` if:
    *   The `clipboard` flag is true (default).
    *   `final_output_str` is not empty and doesn't indicate an error during its own generation.
*   The `copy_to_clipboard` function itself now handles logging success or specific `pyperclip` failures. The CLI adds a generic failure notice if needed.

**Verification for Step 6.1:**
1.  Ensure `pyperclip` is installed (`uv pip install pyperclip` if not already via project dependencies).
2.  On Linux, you might need `xclip` or `xsel` installed (`sudo apt install xclip`).
3.  Run commands:
    *   `dirdigest ./my_test_dir/` (default, should try to copy, check clipboard content)
    *   `dirdigest ./my_test_dir/ -o out.txt` (should still try to copy the content that went to `out.txt`)
    *   `dirdigest ./my_test_dir/ --no-clipboard` (should not attempt to copy, check logs for "Clipboard copy disabled")
    *   If possible, simulate a scenario where clipboard access might fail (e.g., on a headless server without a clipboard manager, or by temporarily uninstalling `xclip/xsel` if safe to do so for a test). Check for the warning message from `pyperclip`.

---

**Step 6.2: Configuration File Loading (`utils/config.py`)**

**1. Create `dirdigest/dirdigest/utils/config.py`:**

```python
# dirdigest/dirdigest/utils/config.py
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List

from dirdigest.utils.logger import logger

DEFAULT_CONFIG_FILENAME = ".diringest" # Or .dirdigest, let's stick to requirements

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

    if config_path: # User specified a config file
        if config_path.exists() and config_path.is_file():
            cfg_path_to_load = config_path
        else:
            logger.warning(f"Config: Specified configuration file not found or not a file: [log.path]{config_path}[/log.path]")
            return {} # Return empty if specified config is invalid
    else: # Try default filename in current directory
        default_path = Path.cwd() / DEFAULT_CONFIG_FILENAME
        if default_path.exists() and default_path.is_file():
            cfg_path_to_load = default_path
        # No warning if default config is not found, it's optional.

    if not cfg_path_to_load:
        logger.debug("Config: No configuration file loaded (neither specified nor default found).")
        return {}

    logger.info(f"Config: Loading configuration from [log.path]{cfg_path_to_load}[/log.path]")
    try:
        with open(cfg_path_to_load, 'r', encoding='utf-8') as f:
            full_config_data = yaml.safe_load(f)
            if not isinstance(full_config_data, dict):
                logger.warning(f"Config: Configuration file [log.path]{cfg_path_to_load}[/log.path] is not a valid YAML dictionary.")
                return {}
            
            # As per requirements example, look for a 'default' profile.
            # If other profiles exist, they are ignored for now unless a --profile CLI arg is added later.
            # If 'default' key doesn't exist, but the file is a flat dict, use it as is.
            if 'default' in full_config_data and isinstance(full_config_data['default'], dict):
                logger.debug("Config: Loaded 'default' profile.")
                return full_config_data['default']
            elif 'default' not in full_config_data and all(not isinstance(v, dict) for k, v in full_config_data.items() if k not in ["include", "exclude"]):
                # If no 'default' key and it looks like a flat config (no nested dicts other than include/exclude)
                logger.debug("Config: Loaded as a flat configuration (no 'default' profile found, using root level).")
                return full_config_data
            elif 'default' not in full_config_data and any(isinstance(v, dict) for k, v in full_config_data.items() if k != "default"):
                # Has other profile-like structures but no 'default'
                logger.warning(f"Config: File [log.path]{cfg_path_to_load}[/log.path] has profiles but no 'default' profile. No config loaded. Please specify a profile or add a 'default' section.")
                return {}
            else: # No 'default' and not clearly a flat config (e.g. empty or invalid structure)
                logger.debug(f"Config: No 'default' profile found in [log.path]{cfg_path_to_load}[/log.path] or not a simple flat config. Using empty config.")
                return {}


    except yaml.YAMLError as e:
        logger.warning(f"Config: Error parsing YAML configuration file [log.path]{cfg_path_to_load}[/log.path]: {e}")
        return {}
    except OSError as e:
        logger.warning(f"Config: Error reading configuration file [log.path]{cfg_path_to_load}[/log.path]: {e}")
        return {}
    except Exception as e:
        logger.error(f"Config: Unexpected error loading configuration from [log.path]{cfg_path_to_load}[/log.path]: {e}", exc_info=True)
        return {}

def merge_config(cli_args: Dict[str, Any], config_file_settings: Dict[str, Any], click_context: click.Context) -> Dict[str, Any]:
    """
    Merges CLI arguments with settings from a configuration file.
    CLI arguments take precedence if they were explicitly set (not their default).

    :param cli_args: A dictionary of arguments from Click (ctx.params).
    :param config_file_settings: A dictionary of settings loaded from the config file.
    :param click_context: The Click context object (ctx).
    :return: A dictionary of the final merged settings.
    """
    merged_settings = config_file_settings.copy() # Start with config file settings as base
    logger.debug(f"Config: Initial settings from config file: {config_file_settings}")
    logger.debug(f"Config: CLI args received: {cli_args}")

    for key, cli_value in cli_args.items():
        # Check if the CLI argument was explicitly set by the user,
        # or if it's just the default value defined in Click.
        # We use click.Context.get_parameter_source() for this.
        # This requires Click 8.0+
        source = click_context.get_parameter_source(key)
        
        param_is_explicitly_set = source is not None and source.name != 'DEFAULT' # Default from click itself
        param_is_default_from_context = source is not None and source.name == 'DEFAULT_MAP' # Default from context obj default_map

        # If the CLI value was explicitly provided by user (not a Click default or context default)
        # OR if the key is not in config_file_settings (so CLI default is better than nothing)
        if param_is_explicitly_set or (key not in merged_settings and not param_is_default_from_context):
             # Special handling for 'include' and 'exclude' as they are multiple
             # And CLI can have multiple=True flag, which results in a tuple.
             # Config file might have a list.
            if key in ["include", "exclude"] and isinstance(cli_value, tuple) and not any(cli_value):
                # If CLI provided empty tuple (e.g. flag not used), and config has value, prefer config.
                # This might need refinement: if user explicitly says --include '' (empty), it should override.
                # Click's multiple=True gives empty tuple if flag not used.
                # If flag used with empty val, that's different. This logic is tricky.
                # For now: if CLI is empty tuple (flag not used), don't let it override a config list.
                if key in merged_settings: # If config has this key, let it be.
                    logger.debug(f"Config: CLI {key} is empty tuple (flag not used), keeping config value: {merged_settings[key]}")
                else: # Config doesn't have it, CLI is empty tuple, so effectively no value.
                    merged_settings[key] = [] if cli_value == () else cli_value
                    logger.debug(f"Config: CLI {key} is empty tuple, config also no value. Setting to empty list or cli_value.")
            else:
                merged_settings[key] = cli_value
                logger.debug(f"Config: Overriding '{key}' with CLI value: {cli_value} (Source: {source.name if source else 'N/A'})")

    # Normalize include/exclude to always be lists, handling comma-separated strings from config
    for key in ["include", "exclude"]:
        if key in merged_settings:
            current_val = merged_settings[key]
            normalized_patterns: List[str] = []
            if isinstance(current_val, str): # Single comma-separated string from config
                normalized_patterns.extend(p.strip() for p in current_val.split(',') if p.strip())
            elif isinstance(current_val, (list, tuple)): # List from config or tuple from CLI
                for item in current_val:
                    if isinstance(item, str):
                        normalized_patterns.extend(p.strip() for p in item.split(',') if p.strip())
                    # else: ignore non-string items in list/tuple
            merged_settings[key] = normalized_patterns
            logger.debug(f"Config: Normalized '{key}' to: {merged_settings[key]}")


    logger.debug(f"Config: Final merged settings: {merged_settings}")
    return merged_settings

```
*Changes in `config.py`*:
*   `DEFAULT_CONFIG_FILENAME` is set to `.diringest`.
*   `load_config_file` attempts to load the specified file or the default. It looks for a `default:` key in the YAML as per requirements. If not found, and the YAML is a flat dictionary, it uses that.
*   `merge_config` is the core logic:
    *   It iterates through CLI parameters.
    *   Uses `click_context.get_parameter_source(key)` (requires Click 8.0+) to determine if a CLI option was explicitly set by the user or is just a Click default. CLI explicit settings override config.
    *   If a CLI option was *not* explicitly set, the config file value (if any) is used.
    *   If neither CLI nor config file has a value, then Click's internal default for the option applies.
    *   Special handling for `include`/`exclude`: normalizes them into flat lists of patterns, processing comma-separated strings if they come from the config file.

**Step 6.3: Merge CLI Arguments with Configuration (`cli.py`)**

Modify `dirdigest/dirdigest/cli.py` at the beginning of the `main_cli` function:

```python
# dirdigest/dirdigest/cli.py
# ... (other imports) ...
from dirdigest.utils import config as dirdigest_config # Import the new config utility
# ...

@click.command(...)
@click.pass_context # Add this decorator to get the Click context
# ... (all options) ...
def main_cli(
    ctx: click.Context, # Add ctx parameter
    directory: pathlib.Path,
    # ... other parameters ...
    config: pathlib.Path | None, # This is the --config FILE path from CLI
    # ... rest of parameters
):
    start_time = time.monotonic()

    # --- Load Config File and Merge with CLI Args ---
    # cfg_file_values are settings from the .diringest file (e.g. from its 'default' profile)
    cfg_file_values = dirdigest_config.load_config_file(config) # config is the path from --config option

    # ctx.params contains all params passed to this command, including CLI args and their defaults
    # We need to determine final settings based on precedence:
    # 1. CLI explicit value
    # 2. Config file value
    # 3. Click option default
    
    # Create a dictionary of actual CLI parameters that were set or have defaults
    # This includes the --config option itself, which we don't want to merge as a setting
    current_cli_params = ctx.params.copy() 
    
    # The 'config' key in current_cli_params is the Path to the config file,
    # not a setting to be applied. We've already used it.
    # It's fine if it's passed to merge_config, as it won't match config file keys.
    
    # merged_settings will hold the final values for options
    final_settings = dirdigest_config.merge_config(current_cli_params, cfg_file_values, ctx)

    # --- Setup Logging (using final 'verbose', 'quiet', 'log_file' from merged_settings) ---
    # Get logging-related settings from the merged final_settings
    final_verbose = final_settings.get('verbose', 0) # Default to 0 if not found
    final_quiet = final_settings.get('quiet', False)
    final_log_file = final_settings.get('log_file') # Will be None if not set
    # Ensure final_log_file is Path object if it came from config as string
    if isinstance(final_log_file, str):
        final_log_file = pathlib.Path(final_log_file)

    dirdigest_logger.setup_logging(
        verbose_level=final_verbose, 
        quiet=final_quiet, 
        log_file_path=final_log_file
    )
    log = dirdigest_logger.logger

    # --- Use final_settings for application logic ---
    # Update local variables from final_settings to be used by the rest of the function
    directory = final_settings.get('directory', directory) # Should be pathlib.Path
    if isinstance(directory, str): directory = pathlib.Path(directory)
    
    output_file_name = final_settings.get('output', sys.stdout) # Output might be a path string from config
    # The 'output' option in Click is type=click.File.
    # If it comes from config as a string, we need to handle it.
    # For simplicity, merge_config should ideally return values that match Click's expected types,
    # or we handle type conversion here. Let's assume output from config is a string path for now.
    # This part is tricky because Click handles file opening.
    # If 'output' is from config, 'output' in ctx.params is already a LazyFile (stdout).
    # We need to be careful here. Let's assume for now that 'output' is handled by Click,
    # and config file cannot easily override it to a file path without more complex Click context manipulation.
    # For now, we'll use the 'output' LazyFile object that Click prepared.
    # Config file overriding output file path will be an advanced topic.
    # For this iteration: config file cannot set output file. CLI -o flag is king for files.

    format_type = final_settings.get('format', 'markdown') # format is already a string
    
    # include/exclude are already parsed into lists of strings by merge_config
    parsed_include_patterns = final_settings.get('include', [])
    parsed_exclude_patterns = final_settings.get('exclude', [])
    
    max_size_kb = final_settings.get('max_size', 300) # default from click if not in config/cli
    max_depth_val = final_settings.get('max_depth') # could be None
    no_default_ignore_flag = final_settings.get('no_default_ignore', False)
    follow_symlinks_flag = final_settings.get('follow_symlinks', False)
    ignore_errors_flag = final_settings.get('ignore_errors', False)
    clipboard_flag = final_settings.get('clipboard', True) # Reflects the --clipboard/--no-clipboard default

    log.debug(f"CLI: Final effective settings after merge: {final_settings}")
    log.info(f"CLI: Processing directory: [log.path]{directory}[/log.path]")
    # ... (rest of the logging of parameters using final_settings values)

    # --- Core Processing (using final_settings values) ---
    processed_items_generator, stats_from_core = core.process_directory_recursive(
        base_dir_path=directory, # Use final 'directory'
        include_patterns=parsed_include_patterns,
        exclude_patterns=parsed_exclude_patterns,
        no_default_ignore=no_default_ignore_flag,
        max_depth=max_depth_val,
        follow_symlinks=follow_symlinks_flag,
        max_size_kb=max_size_kb,
        ignore_read_errors=ignore_errors_flag
    )

    # ... (rest of build_digest_tree call, metadata handling) ...
    root_node, metadata_for_output = core.build_digest_tree(
        directory, # Use final 'directory' for base_directory in metadata
        processed_items_generator, 
        stats_from_core
    )
    # ... (formatter selection based on final 'format_type') ...
    selected_formatter: dirdigest_formatter.BaseFormatter
    if format_type.lower() == 'json': # Use 'format_type'
        selected_formatter = dirdigest_formatter.JsonFormatter(directory, metadata_for_output)
    elif format_type.lower() == 'markdown':
        selected_formatter = dirdigest_formatter.MarkdownFormatter(directory, metadata_for_output)
    # ... (formatter.format call) ...
    
    # --- Clipboard (using final 'clipboard_flag') ---
    if clipboard_flag: # Use final 'clipboard_flag'
    # ... (rest of clipboard logic) ...

    # ... (Summary statistics, Debug JSON tree)
```
*Changes in `cli.py` for config*:
*   Added `@click.pass_context` decorator and `ctx: click.Context` parameter.
*   Calls `dirdigest_config.load_config_file(config)` where `config` is the `--config <path>` value.
*   Calls `dirdigest_config.merge_config(ctx.params, cfg_file_values, ctx)` to get `final_settings`.
*   **Crucially**: The rest of the `main_cli` function now uses values from `final_settings` (e.g., `final_verbose`, `final_quiet`, `parsed_include_patterns` from `final_settings.get('include')`, etc.) instead of directly from the function parameters. This ensures the merged config is used.
*   The handling of `output` when it comes from a config file is noted as tricky and deferred for deeper Click context manipulation. For now, config cannot set the output file path if it's not stdout.

**Verification for Step 6.2 & 6.3:**
1.  **Create a `.diringest` file** in your project's root or `my_test_dir` (or specify a custom path with `--config`):
    ```yaml
    # .diringest
    default:
      format: json
      max_size: 10  # Small max size in KB
      # No default ignore true means default ignores ARE active
      # follow_symlinks: false (default)
      # ignore_errors: false (default)
      clipboard: false # Override default clipboard behavior
      verbose: 1 # -v equivalent
      
      exclude:
        - "*.md"       # Exclude all markdown files
        - "script.py"
      
      # Example of include, though if used, only these would be processed
      # include: 
      #  - "file1.txt" 
    ```
2.  **Test Scenarios:**
    *   `dirdigest ./my_test_dir/`
        *   *Expected*: Should use settings from `.diringest`. Output format JSON, max_size 10KB, clipboard off, verbose (-v) logging. Markdown files and `script.py` should be excluded.
    *   `dirdigest ./my_test_dir/ --format markdown`
        *   *Expected*: CLI `--format markdown` overrides config's `json`. Other settings from config still apply.
    *   `dirdigest ./my_test_dir/ --max-size 50`
        *   *Expected*: CLI `--max-size 50` overrides config's `10`.
    *   `dirdigest ./my_test_dir/ --no-clipboard`
        *   *Expected*: CLI `--no-clipboard` matches config's `clipboard: false`. No change from config.
    *   `dirdigest ./my_test_dir/ --config path/to/custom.yaml` (if you create another YAML elsewhere).
    *   `dirdigest ./my_test_dir/ --exclude "*.txt"`
        *   *Expected*: CLI `--exclude "*.txt"` should override the `exclude` list from the config file. Config excludes `*.md` and `script.py`, CLI adds `*.txt`. The `merge_config` for list-like items (include/exclude) needs to define if it appends or replaces. Current `merge_config` has CLI override.
3.  Check logs (console and file if `--log-file` is used or in config) for:
    *   Messages about loading the config file.
    *   Debug messages showing initial config, CLI args, and final merged settings.

This phase is complex due to the interaction of CLI defaults, config file values, and explicit CLI arguments. The `click.Context.get_parameter_source()` is key to correctly determining precedence.

Good luck testing this! It's the final major piece of functionality from the requirements. After this, it's mostly polish and the "emotional unpredictability" part for me. 😉