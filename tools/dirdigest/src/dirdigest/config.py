"""Handles configuration loading and merging (defaults, file, CLI)."""

import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib # type: ignore[no-redef]


log = logging.getLogger(__name__)

# --- Default Configuration ---

DEFAULT_EXCLUDE_PATTERNS: List[str] = [
    # Version Control
    ".git/", ".svn/", ".hg/", ".bzr/",
    # Hidden Files/Dirs (Common)
    ".*", ".*/**",
    # Lock files
    "*.lock",
    # Python Artifacts
    "__pycache__/", "*.pyc", "*.pyo", ".venv/", "venv/", "env/", "*.egg-info/",
    ".pytest_cache/", ".mypy_cache/",
    # Node.js
    "node_modules/",
    # Build Outputs
    "build/", "dist/", "target/", "out/",
    # IDE/Editor Config
    ".vscode/", ".idea/", "*.sublime-project", "*.sublime-workspace",
    ".project", ".settings/", ".classpath",
    # OS/System Files
    ".DS_Store", "Thumbs.db",
    # Logs
    "*.log",
    # Temporary Files
    "*.tmp", "*~", "*.bak", "*.swp",
    # Dependencies/Packages
    "vendor/",
    # Caches
    ".cache/",
    # Common Binary/Media/Docs (often large or not useful for LLM context)
    "*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp", "*.tiff", "*.ico", # Images
    # "*.svg", # SVGs can contain XML/text, maybe keep? Decide based on use case.
    "*.mp3", "*.wav", "*.ogg", "*.mp4", "*.avi", "*.mov", "*.wmv", "*.flv", # Audio/Video
    "*.pdf", "*.doc", "*.docx", "*.xls", "*.xlsx", "*.ppt", "*.pptx", # Docs
    "*.odt", "*.ods", "*.odp",
    # Archives/Compressed
    "*.zip", "*.tar", "*.gz", "*.rar", "*.7z", "*.bz2", "*.xz",
    # Executables/Libraries
    "*.exe", "*.dll", "*.so", "*.dylib", "*.jar", "*.class", "*.o", "*.a",
    "*.app", "*.pkg", "*.dmg",
    # Large Data Files (often better skipped by size, but good defaults)
    "*.pkl", "*.h5", "*.hdf5", "*.feather", "*.parquet", "*.avro", "*.orc",
    "*.onnx", "*.pb", "*.pt", "*.pth", # ML Model files
    # Config file itself
    ".diringest",
]

DEFAULT_CONFIG: Dict[str, Any] = {
    "output": None,
    "include": [],
    "exclude": [], # User excludes supplement defaults unless --no-default-ignore
    "max_size": 300, # KB
    "format": "markdown",
    "clipboard": None, # Default depends on presence of --output
    "default_ignore": True, # Corresponds to NOT using --no-default-ignore
    "verbose": False,
    # Internal defaults / options not directly exposed via CLI but configurable
    "config_file_name": ".diringest",
    "follow_symlinks": False, # Default: Do not follow symlinks
    "encoding": "utf-8",
}

# --- Configuration Loading ---

# src/dirdigest/config.py

def find_config_file(
    # Keep start_dir argument for potential future use, but logic searches from cwd
    start_dir: Path,
    filename: str = DEFAULT_CONFIG["config_file_name"]
) -> Optional[Path]:
    """Find the config file by searching up from the current working directory."""
    current_dir = Path.cwd().resolve()

    for directory in [current_dir] + list(current_dir.parents):
        config_path = directory / filename
        log.debug(f"Checking for config file at: {config_path}")
        if config_path.is_file(): # is_file() implies exists() and is a file
            log.info(f"Found configuration file: {config_path}")
            return config_path
        # Stop searching if we hit the root directory's parent explicitly
        # or if the parent is the same as the directory (root edge case)
        if directory.parent == directory:
             break

    log.debug(f"No configuration file '{filename}' found searching from {Path.cwd()}.")
    return None

def load_config_from_file(config_path: Optional[Path]) -> Dict[str, Any]:
    """Load configuration from a TOML file."""
    if not config_path:
        return {}

    try:
        with open(config_path, "rb") as f:
            config_data = tomllib.load(f)
        log.info(f"Loaded configuration from {config_path}")
        # Basic validation could be added here if needed (e.g., check types)
        return config_data
    except tomllib.TOMLDecodeError as e:
        log.warning(f"Error parsing configuration file {config_path}: {e}. Using defaults.")
        return {}
    except OSError as e:
        log.warning(f"Error reading configuration file {config_path}: {e}. Using defaults.")
        return {}

def merge_config(
    cli_args: Dict[str, Any],
    file_config: Dict[str, Any],
    defaults: Dict[str, Any],
) -> Dict[str, Any]:
    """Merge configurations respecting precedence: CLI > File > Defaults."""
    merged = defaults.copy()

    # 1. Apply File Config (overrides defaults)
    for key, value in file_config.items():
        if key in merged:
            # Special handling for list concatenation might be needed if desired,
            # but simple override is often clearer. Here we override.
            merged[key] = value
        else:
            log.warning(f"Unknown key '{key}' in config file ignored.")

    # 2. Apply CLI Args (overrides file config and defaults)
    for key, value in cli_args.items():
        if key == "directory": # Positional arg, not a config option
            continue
        if value is not None: # CLI option was explicitly provided
            if key == "exclude" and merged.get("default_ignore", True):
                # If default ignores are active, CLI excludes *add* to file excludes
                # If default ignores are inactive, CLI excludes *replace* file excludes
                # Let's simplify: CLI always replaces file config for lists.
                # User can manage combined lists in their .diringest if needed.
                merged[key] = list(value) # Ensure it's a list from tuple
            elif key == "include":
                 merged[key] = list(value) # Ensure it's a list from tuple
            elif key == "no_default_ignore":
                merged["default_ignore"] = not value # CLI flag flips the default
            elif key == "no_clipboard":
                # This flag dictates the final clipboard decision logic in cli.py
                # We store it here to pass it along.
                 merged["no_clipboard_flag"] = value
            elif key in merged:
                merged[key] = value
            # Do not warn about unknown keys here, as CLI parsing handles that.

    # Handle clipboard default logic: True if output is None AND --no-clipboard is false
    # We calculate the final decision in the CLI layer after merging is done.

    # Ensure list types for include/exclude if they came from single strings in config
    if isinstance(merged.get("include"), str):
        merged["include"] = [merged["include"]]
    if isinstance(merged.get("exclude"), str):
         merged["exclude"] = [merged["exclude"]]

    log.debug(f"Final merged configuration: {merged}")
    return merged

def get_effective_config(
    cli_args: Dict[str, Any], start_dir: Path
) -> Dict[str, Any]:
    """Loads and merges configuration from all sources."""
    config_file_path = find_config_file(start_dir, DEFAULT_CONFIG["config_file_name"])
    file_config = load_config_from_file(config_file_path)
    final_config = merge_config(cli_args, file_config, DEFAULT_CONFIG)
    return final_config