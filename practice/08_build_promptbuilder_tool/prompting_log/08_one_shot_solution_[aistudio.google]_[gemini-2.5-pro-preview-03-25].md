Okay, let's implement the `promptbuilder` tool according to the improved requirements.

This will involve several files organized into a package structure for maintainability.

**Project Structure:**

```
promptbuilder/
├── __init__.py
├── __main__.py
├── cli.py
├── config.py
├── context.py
├── interactive.py
├── templating.py
├── utils.py
├── templates/
│   └── default_meta_prompt.j2
├── pyproject.toml
└── .promptbuilder.yaml  # Example config
```

**1. `pyproject.toml` (using Poetry)**

```toml
[tool.poetry]
name = "promptbuilder"
version = "0.1.0"
description = "A tool to generate meta-prompts for instructing LLMs to create task-performing prompts."
authors = ["Your Name <you@example.com>"]
readme = "README.md"
packages = [{include = "promptbuilder"}]

[tool.poetry.dependencies]
python = "^3.8"
pyyaml = "^6.0"
jinja2 = "^3.1"
pyperclip = "^1.8"

[tool.poetry.scripts]
promptbuilder = "promptbuilder.cli:main"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

*   Run `poetry install` to create the virtual environment and install dependencies.

**2. `promptbuilder/config.py`**

```python
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

```

**3. `.promptbuilder.yaml` (Example Config)**

```yaml
# Example .promptbuilder.yaml configuration file

# default_meta_prompt_template_path: /path/to/your/custom/template.j2 # Optional override
placeholder_format: "__%s__"
context_max_file_size_mb: 10.0
context_supported_extensions:
  - .py
  - .md
  - .txt
  - .rst
context_encoding: utf-8
copy_to_clipboard_default: true
output_dir: ./generated_prompts
interactive_multiline_end_marker: EOD # End Of Document
```

**4. `promptbuilder/utils.py`**

```python
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

```

**5. `promptbuilder/context.py`**

```python
import logging
from pathlib import Path
from typing import List, Optional, Tuple, Set

from .config import Config

logger = logging.getLogger(__name__)

# Using tuple (path_str, content_summary) for now. Content summary can be filename or content.
ContextInfo = Tuple[str, Optional[str]]

def parse_context_paths(
    paths: List[str],
    config: Config,
    verbose_level: int = 0
) -> Tuple[List[ContextInfo], int, int]:
    """
    Parses context paths (files/directories), applying configuration limits.

    Returns:
        Tuple containing:
        - List of ContextInfo tuples: (path_string, content_or_summary).
        - Total number of files processed.
        - Total number of files skipped.
    """
    context_items: List[ContextInfo] = []
    processed_files = 0
    skipped_files = 0
    max_bytes = int(config.context_max_file_size_mb * 1024 * 1024)
    supported_ext_set = set(config.context_supported_extensions)
    processed_paths: Set[Path] = set() # Keep track of canonical paths to avoid duplicates

    if not paths:
        return [], 0, 0

    files_to_process: List[Path] = []

    # 1. Collect all potential files
    for path_str in paths:
        path = Path(path_str).resolve() # Resolve to canonical path

        if not path.exists():
            logger.warning(f"Context path not found: {path_str}")
            skipped_files += 1 # Count non-existent paths as skipped
            continue

        if path in processed_paths:
             logger.debug(f"Skipping already processed path: {path_str}")
             continue

        if path.is_file():
            files_to_process.append(path)
            processed_paths.add(path)
        elif path.is_dir():
            logger.info(f"Recursively searching directory: {path_str}")
            for item in path.rglob('*'):
                 item_resolved = item.resolve()
                 if item_resolved in processed_paths:
                     continue
                 if item.is_file():
                     files_to_process.append(item_resolved)
                     processed_paths.add(item_resolved)
                 # else: ignore subdirectories explicitly found by rglob

    # 2. Process collected files
    for file_path in files_to_process:
        processed_files += 1
        display_path = str(file_path) # Use resolved path for display/summary
        logger.debug(f"Processing context file: {display_path}")

        # Check extension
        if file_path.suffix.lower() not in supported_ext_set:
            if verbose_level > 0:
                logger.info(f"Skipping file (unsupported extension {file_path.suffix}): {display_path}")
            skipped_files += 1
            continue

        # Check size
        try:
            file_size = file_path.stat().st_size
            if file_size > max_bytes:
                logger.warning(f"Skipping file (size {file_size / (1024*1024):.2f} MB > limit {config.context_max_file_size_mb} MB): {display_path}")
                skipped_files += 1
                continue
            if file_size == 0:
                 logger.info(f"Including empty file: {display_path}")
                 context_items.append((display_path, "")) # Include empty file marker
                 continue

        except OSError as e:
            logger.error(f"Error accessing file metadata {display_path}: {e}")
            skipped_files += 1
            continue

        # Read content (currently full content mode, limited by size check)
        # TODO: Implement other context_modes later (list, snippets)
        try:
            content = file_path.read_text(encoding=config.context_encoding)
            context_items.append((display_path, content))
            if verbose_level > 1:
                 logger.debug(f"Successfully read content from: {display_path}")
        except UnicodeDecodeError:
            logger.warning(f"Skipping file (encoding error with '{config.context_encoding}'): {display_path}")
            skipped_files += 1
        except IOError as e:
            logger.error(f"Error reading file {display_path}: {e}")
            skipped_files += 1

    total_processed = len(files_to_process) # Count of files attempted after initial collection
    actual_included = len(context_items)

    if verbose_level > 0:
         logger.info(f"Context processing summary: Attempted={total_processed}, Included={actual_included}, Skipped={skipped_files}")

    # Return list of (path_str, content) tuples
    return context_items, total_processed, skipped_files
```

**6. `promptbuilder/templating.py`**

```python
import logging
from pathlib import Path
from typing import Dict, Any, Optional

from jinja2 import Environment, FileSystemLoader, TemplateNotFound, select_autoescape

from .config import Config

logger = logging.getLogger(__name__)

def render_meta_prompt(
    template_path: Path,
    data: Dict[str, Any],
    config: Config
) -> Optional[str]:
    """Renders the meta prompt using Jinja2."""
    try:
        # Ensure template_path is absolute or relative to CWD if not found directly
        if not template_path.is_absolute() and not template_path.exists():
             lookup_path = Path.cwd() / template_path
             if lookup_path.exists():
                 template_path = lookup_path

        if not template_path.is_file():
             logger.error(f"Template file not found: {template_path}")
             return None

        logger.info(f"Using template file: {template_path}")
        template_dir = template_path.parent
        template_filename = template_path.name

        env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(), # Basic protection
            trim_blocks=True,
            lstrip_blocks=True
        )

        # Add placeholder format to the data for easy access in the template
        data['placeholder'] = lambda name: config.placeholder_format % name.upper()

        template = env.get_template(template_filename)
        rendered_prompt = template.render(data)
        logger.debug("Template rendering successful.")
        return rendered_prompt

    except TemplateNotFound:
        logger.error(f"Template not found in directory {template_dir}: {template_filename}")
        return None
    except Exception as e:
        logger.error(f"Error rendering template {template_path}: {e}")
        return None

```

**7. `promptbuilder/templates/default_meta_prompt.j2`**

```jinja2
{# ============================================================ #}
{#               META-PROMPT FOR LLM PROMPT GENERATION          #}
{# ============================================================ #}

**Objective:** Generate a high-quality TASK_PERFORMING_PROMPT based on the specifications below. This prompt will be used by a human user to instruct another LLM to perform a specific task.

**Your Role:** You are an expert prompt engineer. Your goal is to create a clear, concise, effective, and robust TASK_PERFORMING_PROMPT.

**Core Task for the Final LLM:**
The ultimate task the final LLM needs to perform is:
{{ task_description }}

{# ================= META-INSTRUCTIONS (How to build the prompt) ================= #}
{% if meta_instructions %}
**Instructions for Generating the TASK_PERFORMING_PROMPT:**
Follow these guidelines when constructing the final prompt:
{{ meta_instructions }}
{% endif %}

{# ================= TASK_PERFORMING_PROMPT STRUCTURE & CONTENT ================= #}
Construct the TASK_PERFORMING_PROMPT adhering to the following structure and including the specified elements:

**1. Clear Directive:** Start with a clear and direct instruction summarizing the main goal for the final LLM.

**2. Persona (Optional but Recommended):** If appropriate for the task, instruct the final LLM to adopt a specific persona (e.g., "Act as a helpful coding assistant," "You are a creative writer specializing in fantasy.").

**3. Context (If Provided):**
{% if context_items %}
The final prompt should inform the LLM that the following context is available to assist with the task. The user will provide this context alongside the prompt.
Summarize or reference the context appropriately within the final prompt.

**Provided Context Summary:**
{# Choose how to display context - just filenames for now #}
The following files/sources were provided as context:
{% for path, content in context_items %}
  - {{ path }}{% if verbose_level > 1 and content is not none %} (Size: {{ content|length }} chars){% endif %}
{% endfor %}
{% if context_files_skipped > 0 %}\
(Note: {{ context_files_skipped }} additional context file(s) were skipped due to size limits or errors.)
{% endif %}
{# Alternative: Include full content if context_mode == 'full' and content is not none #}
{# {% for path, content in context_items %}
--- START CONTEXT FILE: {{ path }} ---
{{ content }}
--- END CONTEXT FILE: {{ path }} ---
{% endfor %} #}

{% endif %}

**4. Input Specification (If Provided):**
{% if input_description %}
The final prompt MUST instruct the LLM on the expected input format.
Description of expected input:
{{ input_description }}
The final prompt MUST include a placeholder `{{ placeholder('INPUT') }}` where the user will insert their specific input for the task.
{% endif %}
{% if input_instructions %}
The final prompt should include instructions for the *user* on how to provide their input. Include the following details:
{{ input_instructions }}
{% if input_description %}It should clearly relate to the `{{ placeholder('INPUT') }}` placeholder.{% endif %}
{% endif %}

**5. Output Specification (If Provided):**
{% if output_description %}
The final prompt MUST instruct the LLM on the desired output format or structure.
Description of desired output:
{{ output_description }}
{% if not output_instructions %}The final prompt might need an `{{ placeholder('OUTPUT') }}` placeholder or a dedicated section describing the output format.{% endif %}
{% endif %}
{% if output_instructions %}
The final prompt MUST include specific instructions for the *LLM* on how to format its output. Include the following formatting requirements:
{{ output_instructions }}
{% if output_description %}This should align with the description: {{ output_description }}.{% endif %}
{% endif %}

**6. Examples (If Provided):**
{% if example_input or example_output %}
Include the following examples in the final prompt to guide the LLM:
{% if example_input %}
**Example Input:**
```
{{ example_input }}
```
{% endif %}
{% if example_output %}
**Example Output:**
```
{{ example_output }}
```
{% endif %}
{% endif %}

**7. Constraints & Tone:** Ensure the final prompt clearly states any constraints, desired tone, or negative constraints (what the LLM *should not* do).

**8. Final Check:** The generated TASK_PERFORMING_PROMPT should be self-contained, unambiguous, and directly usable by a human interacting with an LLM.


{# ================= GENERATE THE TASK_PERFORMING_PROMPT BELOW ================= #}

Now, based on all the above instructions, generate the TASK_PERFORMING_PROMPT.
```

**8. `promptbuilder/interactive.py`**

```python
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

from .config import Config
from .utils import get_multiline_input, validate_path_input

logger = logging.getLogger(__name__)

def run_interactive_mode(cli_args: Any, config: Config) -> Optional[Dict[str, Any]]:
    """Runs the interactive prompting session."""
    collected_data: Dict[str, Any] = {}
    final_actions = {'save_path': None, 'copy_flag': False}

    print("--- PromptBuilder Interactive Mode ---")
    print("Please provide the following details to build the meta-prompt.")
    print("(Leave optional fields blank and press Enter to skip)")

    # 1. Task (Required)
    if cli_args.task:
        print(f"Using Task from command line: {cli_args.task}")
        collected_data['task'] = cli_args.task
    else:
        while not collected_data.get('task'):
            task = input("Enter the ultimate task description (Required): ").strip()
            if task:
                collected_data['task'] = task
            else:
                print("Task description cannot be empty.")

    # 2. Context (Optional, Multiple)
    if cli_args.context:
        print(f"Using Context paths from command line: {', '.join(cli_args.context)}")
        collected_data['context_paths'] = cli_args.context
    else:
        context_paths = []
        print("\n--- Context Files/Folders ---")
        print("Enter paths to files or folders for context. Directories will be searched recursively.")
        print("Supported extensions:", ", ".join(config.context_supported_extensions))
        print("Enter 'done' or leave blank when finished.")
        while True:
            path_str = input("Add context path (or 'done'): ").strip()
            if not path_str or path_str.lower() == 'done':
                break
            # Basic validation - check existence? utils.validate_path_input can do this
            validated_path = validate_path_input(path_str, check_exists=True)
            if validated_path:
                 context_paths.append(str(validated_path)) # Store as string initially
            # else: Error message printed by validate_path_input
        if context_paths:
             collected_data['context_paths'] = context_paths

    # 3. Meta Instructions (Optional)
    if cli_args.meta_instructions:
        print("\nUsing Meta Instructions from command line/file.")
        # Reading happens later in cli.py based on collected path/text
        collected_data['meta_instructions_src'] = cli_args.meta_instructions
    else:
        meta_instr = get_multiline_input(
            "\n[Optional] Enter Meta Instructions (guidance for the prompt *generator*):",
            config.interactive_multiline_end_marker
        ).strip()
        if meta_instr:
            collected_data['meta_instructions_src'] = meta_instr

    # 4. Input Description (Optional)
    if cli_args.input:
        print("\nUsing Input Description from command line/file.")
        collected_data['input_desc_src'] = cli_args.input
    else:
        input_desc = get_multiline_input(
             "\n[Optional] Describe the expected INPUT for the final prompt:",
             config.interactive_multiline_end_marker
        ).strip()
        if input_desc:
            collected_data['input_desc_src'] = input_desc

    # 5. Input Instructions (Optional)
    if cli_args.input_instructions:
         print("\nUsing Input Instructions from command line/file.")
         collected_data['input_instr_src'] = cli_args.input_instructions
    elif collected_data.get('input_desc_src'): # Only ask if input description exists
        input_instr = get_multiline_input(
            "\n[Optional] Enter instructions for the USER on HOW to provide input:",
            config.interactive_multiline_end_marker
        ).strip()
        if input_instr:
            collected_data['input_instr_src'] = input_instr

    # 6. Output Description (Optional)
    if cli_args.output:
        print("\nUsing Output Description from command line/file.")
        collected_data['output_desc_src'] = cli_args.output
    else:
        output_desc = get_multiline_input(
             "\n[Optional] Describe the desired OUTPUT from the final prompt:",
             config.interactive_multiline_end_marker
        ).strip()
        if output_desc:
            collected_data['output_desc_src'] = output_desc

    # 7. Output Instructions (Optional)
    if cli_args.output_instructions:
         print("\nUsing Output Instructions from command line/file.")
         collected_data['output_instr_src'] = cli_args.output_instructions
    elif collected_data.get('output_desc_src'): # Only ask if output description exists
         output_instr = get_multiline_input(
             "\n[Optional] Enter instructions for the LLM on HOW to format output:",
             config.interactive_multiline_end_marker
         ).strip()
         if output_instr:
            collected_data['output_instr_src'] = output_instr

    # 8. Example Input (Optional)
    if cli_args.example_input:
        print("\nUsing Example Input from command line/file.")
        collected_data['example_input_src'] = cli_args.example_input
    else:
        example_input = get_multiline_input(
             "\n[Optional] Provide an EXAMPLE of valid input:",
             config.interactive_multiline_end_marker
        ).strip()
        if example_input:
             collected_data['example_input_src'] = example_input

    # 9. Example Output (Optional)
    if cli_args.example_output:
        print("\nUsing Example Output from command line/file.")
        collected_data['example_output_src'] = cli_args.example_output
    else:
        example_output = get_multiline_input(
             "\n[Optional] Provide an EXAMPLE of desired output:",
             config.interactive_multiline_end_marker
         ).strip()
        if example_output:
             collected_data['example_output_src'] = example_output


    # --- Confirmation ---
    print("\n--- Summary of Collected Information ---")
    print(f"Task: {collected_data.get('task')}")
    print(f"Context Paths: {collected_data.get('context_paths', 'None')}")
    print(f"Meta Instructions Source: {'Provided' if collected_data.get('meta_instructions_src') else 'None'}")
    print(f"Input Description Source: {'Provided' if collected_data.get('input_desc_src') else 'None'}")
    print(f"Input Instructions Source: {'Provided' if collected_data.get('input_instr_src') else 'None'}")
    print(f"Output Description Source: {'Provided' if collected_data.get('output_desc_src') else 'None'}")
    print(f"Output Instructions Source: {'Provided' if collected_data.get('output_instr_src') else 'None'}")
    print(f"Example Input Source: {'Provided' if collected_data.get('example_input_src') else 'None'}")
    print(f"Example Output Source: {'Provided' if collected_data.get('example_output_src') else 'None'}")
    print("-" * 30)

    confirm = input("Proceed with generation? [Y/n]: ").strip().lower()
    if confirm not in ('', 'y', 'yes'):
        print("Generation cancelled.")
        return None

    # --- Final Actions ---
    print("\n--- Final Actions ---")
    # Save to disk
    save_path_str = cli_args.save_on_disk or input("Save prompt to disk? (Enter path or leave blank for stdout): ").strip()
    if save_path_str:
        # Allow relative paths, resolve later in cli.py
        final_actions['save_path'] = save_path_str

    # Copy to clipboard
    copy_default = 'y' if config.copy_to_clipboard_default else 'n'
    copy_prompt = f"Copy prompt to clipboard? [{copy_default.upper()}/{copy_default.lower()}]: "
    copy_choice = cli_args.copy or input(copy_prompt).strip().lower()
    if cli_args.copy: # If flag is set, force copy
         final_actions['copy_flag'] = True
    elif copy_choice in ('y', 'yes'):
        final_actions['copy_flag'] = True
    elif not copy_choice and config.copy_to_clipboard_default: # Default applies if blank
         final_actions['copy_flag'] = True
    else:
         final_actions['copy_flag'] = False


    # Attach final actions to the collected data
    collected_data.update(final_actions)

    return collected_data
```

**9. `promptbuilder/cli.py`**

```python
import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional

from . import config as cfg
from . import context
from . import templating
from . import utils
from . import interactive

# Setup basic logging configuration
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.WARNING, format=log_format)
logger = logging.getLogger(__name__) # Get logger for this module

def setup_logging(verbose_level: int):
    """Configures logging level based on verbosity."""
    if verbose_level == 1:
        logging.getLogger('promptbuilder').setLevel(logging.INFO)
        logger.info("Verbose mode enabled (INFO level)")
    elif verbose_level >= 2:
        logging.getLogger('promptbuilder').setLevel(logging.DEBUG)
        logger.info("Verbose mode enabled (DEBUG level)")
    # Else: keep default (WARNING)


def create_parser() -> argparse.ArgumentParser:
    """Creates the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="Generate META_PROMPTs for instructing LLMs to create task-performing prompts.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Core arguments
    parser.add_argument(
        "--task",
        type=str,
        help="**(Required unless interactive)** Concise description of the ultimate task for the final LLM."
    )
    parser.add_argument(
        "--context",
        type=str,
        nargs='+',  # Allows one or more paths
        help="One or more file or directory paths for context. Dirs parsed recursively for supported types."
    )
    parser.add_argument(
        "--meta-instructions",
        metavar="TEXT_OR_PATH",
        help="Instructions for the META_PROMPT generator (how to build the final prompt). Text or file path."
    )

    # Input/Output Specification
    parser.add_argument(
        "--input",
        metavar="TEXT_OR_PATH",
        help="Description of the expected input for the final prompt. Text or file path."
    )
    parser.add_argument(
        "--output",
        metavar="TEXT_OR_PATH",
        help="Description of the desired output from the final prompt. Text or file path."
    )
    parser.add_argument(
        "--input-instructions",
        metavar="TEXT_OR_PATH",
        help="Instructions for the USER on how to provide input. Text or file path."
    )
    parser.add_argument(
        "--output-instructions",
        metavar="TEXT_OR_PATH",
        help="Instructions for the LLM on how to format output. Text or file path."
    )

    # Examples
    parser.add_argument(
        "--example-input",
        metavar="TEXT_OR_PATH",
        help="An example of valid input for the final prompt. Text or file path."
    )
    parser.add_argument(
        "--example-output",
        metavar="TEXT_OR_PATH",
        help="An example of desired output from the final prompt. Text or file path."
    )

    # Output and Configuration
    parser.add_argument(
        "--save-on-disk",
        metavar="PATH",
        help="Save the generated META_PROMPT to this file path instead of printing to stdout."
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy the generated META_PROMPT to the system clipboard."
    )
    parser.add_argument(
        "--config",
        metavar="PATH",
        help=f"Specify a configuration file path (default search: ./{cfg.DEFAULT_CONFIG_FILENAME}, {cfg.CONFIG_SEARCH_PATHS[1]})."
    )
    parser.add_argument(
        "--template",
        metavar="PATH",
        help="Specify a custom META_PROMPT Jinja2 template file."
    )

    # Modes and Verbosity
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Activate Interactive Mode to gather inputs via prompts."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="count",
        default=0,
        help="Increase output verbosity (-v for INFO, -vv for DEBUG)."
    )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    setup_logging(args.verbose)

    # Load configuration
    config = cfg.Config.load(args.config)
    if args.verbose > 0:
        logger.info(f"Loaded configuration: {config}")


    collected_data: Optional[Dict[str, Any]] = None
    final_actions = {
        'save_path': args.save_on_disk,
         # Determine initial copy flag based on arg and config default
        'copy_flag': args.copy or (config.copy_to_clipboard_default and not args.copy), # Explicit --copy overrides default=false
    }

    if args.interactive:
        logger.info("Starting interactive mode...")
        interactive_results = interactive.run_interactive_mode(args, config)
        if interactive_results is None:
            sys.exit(0) # User cancelled
        # Interactive mode returns all data *including* final actions
        collected_data = interactive_results
        # Override CLI final actions with interactive choices
        final_actions['save_path'] = collected_data.pop('save_path', None)
        final_actions['copy_flag'] = collected_data.pop('copy_flag', False)
    else:
        # CLI Mode - check required args
        if not args.task:
            parser.error("--task is required in non-interactive mode.")
            sys.exit(1) # Should be unreachable due to parser.error

        logger.info("Running in CLI mode...")
        # Gather data directly from args
        collected_data = {
            'task_description': args.task,
            'context_paths': args.context, # Pass paths for context parsing
            'meta_instructions_src': args.meta_instructions,
            'input_desc_src': args.input,
            'input_instr_src': args.input_instructions,
            'output_desc_src': args.output,
            'output_instr_src': args.output_instructions,
            'example_input_src': args.example_input,
            'example_output_src': args.example_output,
        }
        # Final actions already set from args/config

    # --- Common Processing (Both Modes) ---

    # Resolve text/path arguments
    template_data: Dict[str, Any] = {
         'task_description': collected_data.get('task') or collected_data.get('task_description'), # Handle key difference
         'meta_instructions': utils.read_text_or_path(collected_data.get('meta_instructions_src'), config.context_encoding, 'meta-instructions'),
         'input_description': utils.read_text_or_path(collected_data.get('input_desc_src'), config.context_encoding, 'input description'),
         'input_instructions': utils.read_text_or_path(collected_data.get('input_instr_src'), config.context_encoding, 'input instructions'),
         'output_description': utils.read_text_or_path(collected_data.get('output_desc_src'), config.context_encoding, 'output description'),
         'output_instructions': utils.read_text_or_path(collected_data.get('output_instr_src'), config.context_encoding, 'output instructions'),
         'example_input': utils.read_text_or_path(collected_data.get('example_input_src'), config.context_encoding, 'example input'),
         'example_output': utils.read_text_or_path(collected_data.get('example_output_src'), config.context_encoding, 'example output'),
         'verbose_level': args.verbose, # Pass verbosity to template if needed
    }

    # Process context
    context_items = []
    context_files_processed = 0
    context_files_skipped = 0
    context_paths_to_parse = collected_data.get('context_paths', [])
    if context_paths_to_parse:
         logger.info("Processing context paths...")
         context_items, context_files_processed, context_files_skipped = context.parse_context_paths(
             context_paths_to_parse,
             config,
             args.verbose
         )
    template_data['context_items'] = context_items
    template_data['context_files_processed'] = context_files_processed
    template_data['context_files_skipped'] = context_files_skipped


    # Determine template path
    template_path = Path(args.template) if args.template else config.default_meta_prompt_template_path

    # Generate META_PROMPT
    logger.info("Generating META_PROMPT...")
    meta_prompt = templating.render_meta_prompt(template_path, template_data, config)

    if not meta_prompt:
        logger.error("Failed to generate META_PROMPT.")
        sys.exit(1)

    # --- Output Actions ---
    output_performed = False
    # 1. Save to Disk
    save_target_str = final_actions.get('save_path')
    if save_target_str:
        save_path = Path(save_target_str)
        # If path is relative, make it relative to the config's output_dir
        if not save_path.is_absolute():
             save_path = config.output_dir / save_path
        if utils.save_to_disk(meta_prompt, save_path.resolve()):
             output_performed = True
        else:
             logger.warning(f"Proceeding without saving to disk due to error.")


    # 2. Copy to Clipboard
    if final_actions.get('copy_flag'):
        if utils.copy_to_clipboard(meta_prompt):
            output_performed = True
        else:
             logger.warning(f"Proceeding without copying to clipboard due to error.")

    # 3. Print to Stdout (Default if no other output action succeeded or was requested)
    if not output_performed or (not save_target_str and not final_actions.get('copy_flag')):
         if not output_performed: # Add a separator if other actions were attempted but failed
              print("\n--- Generated META_PROMPT ---")
         print(meta_prompt)

    logger.info("PromptBuilder finished.")
    sys.exit(0)


if __name__ == '__main__':
    main()

```

**10. `promptbuilder/__main__.py`**

```python
# This allows running the package using 'python -m promptbuilder'
import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())
```

**11. `promptbuilder/__init__.py`**

```python
# Optional: Define package-level items or leave empty
# You could set up root logger here if desired, but basicConfig in cli.py is fine too.
import logging

# Configure the root logger for the package
# logging.getLogger(__name__).addHandler(logging.NullHandler())
```

**To Run:**

1.  Make sure you have Poetry installed.
2.  Navigate to the directory containing `pyproject.toml`.
3.  Run `poetry install`.
4.  Activate the virtual environment: `poetry shell`.
5.  Run the tool:
    *   **CLI Mode Example:**
        ```bash
        promptbuilder --task "Summarize the key points of a technical document" \
                      --context ./docs/my_document.txt ./src/utils.py \
                      --meta-instructions "Generate a prompt suitable for Claude 3 Sonnet. Keep it concise." \
                      --input "The full text of the technical document." \
                      --output "A bulleted list summary (max 5 points)." \
                      --output-instructions "Format the output strictly as a markdown bulleted list." \
                      --save-on-disk ./generated_prompts/summarizer_meta.txt \
                      --copy \
                      -vv # Very verbose
        ```
    *   **Interactive Mode:**
        ```bash
        promptbuilder --interactive
        ```
        or provide some defaults:
        ```bash
        promptbuilder -i --task "Translate Python code to Javascript" --context ./my_code.py
        ```

This implementation covers the specified requirements, including CLI and interactive modes, configuration files, context handling, templating, output options, and modular structure. Remember to create the `README.md` and potentially add tests for robustness.