## FOLDER: `.`

```text

```

### FILE: `README.md`
```md
# Promptbuilder CLI Tool 🦾

**`promptbuilder` is a command-line tool designed to help you generate effective "meta-prompts". These meta-prompts instruct Large Language Models (LLMs) on how to create high-quality, task-specific prompts (`TASK_PERFORMING_PROMPTs`) based on your requirements.**

Instead of manually crafting complex prompts for an LLM to perform a task, you describe the task, provide context, and specify input/output formats to `promptbuilder`. It then generates a detailed set of instructions (the META_PROMPT) for *another* LLM (like GPT-4, Claude, Gemini, etc.) to write the final, polished `TASK_PERFORMING_PROMPT` for you.

**Core Workflow:**

1.  **You:** Define task, context, I/O needs, persona, constraints, etc. for `promptbuilder`.
2.  **`promptbuilder`:** Generates a META_PROMPT using a template.
3.  **You:** Copy the META_PROMPT and give it to your preferred LLM.
4.  **LLM:** Generates the final TASK_PERFORMING_PROMPT based on the META_PROMPT instructions.
5.  **You:** Use the generated TASK_PERFORMING_PROMPT for your original task. Replace placeholders (like `{{INPUT}}` or `__INPUT__`) if necessary.

## Features

*   **CLI & Interactive Modes:** Use via command-line arguments or guided interactive prompts.
*   **Rich Console Output:** Enhanced user experience with formatted text, colors, and structure via the [Rich](https://rich.readthedocs.io/) library.
*   **Context Aware:** Include content from local files and directories (recursively) as context.
*   **Structured Input/Output:** Define expected inputs, outputs, and formatting instructions.
*   **Prompt Characteristics:** Specify persona, tone, constraints, and negative constraints for the final prompt.
*   **Examples:** Provide input/output examples to guide the final prompt generation.
*   **Customizable Templates:** Use the default meta-prompt template or provide your own Jinja2 template.
*   **Configurable:** Set defaults via a `.promptbuilder.yaml` configuration file.
*   **Output Options:** Print to console, save to file, copy to clipboard.

## Example Call
```bash
# Example generating a meta-prompt for evaluating Agent-Based Models
# Make sure you have the necessary context files (docs, code) in ./test_docs/abm_odd_evaluator/
# and the output directory ./generated_prompts/ exists or can be created.
# Assumes you have activated your virtual environment first!

promptbuilder \
    --task "Create a high-quality scientific evaluation report of an agent-based model based on its documentation and code, following the ODD+D protocol structure." \
    --context ./test_docs/abm_odd_evaluator/ \
    --input "The model's codebase and documentation (e.g., ODD description, README)." \
    --input-instructions "Ensure context includes all relevant model files. Provide the context as text or refer to specific files within the provided context." \
    --output "A detailed evaluation report in Markdown format, structured according to the ODD+D checklist provided in the CONTEXT. The report should critically assess the model's adherence to best practices and clarity based *only* on the provided materials." \
    --output-instructions "Return the evaluation report in Markdown format. Use headings for each ODD+D section. Clearly state findings and provide justifications based *strictly* on the provided context files. Identify any missing information or ambiguities." \
    --persona "An expert reviewer in agent-based modeling and social simulation, meticulous about documentation standards like ODD+D. Familiar with scientific writing conventions." \
    --tone "Objective, critical, constructive, and formal." \
    --constraints "Base the evaluation *solely* on the provided context files. Adhere strictly to the ODD+D structure given in the context. Do not invent information or make assumptions beyond the provided material." \
    --negative-constraints "Do not include personal opinions not directly supported by the context. Avoid overly conversational language. Do not evaluate the model's scientific validity, only its documentation quality and completeness according to ODD+D." \
    --save-on-disk ./generated_prompts/abm_odd_evaluator_meta_prompt.md \
    --copy \
    -v
```

## Installation

**Prerequisites:**

*   Python (3.8+ recommended)
*   [uv](https://github.com/astral-sh/uv) (for environment and package management)

**Steps:**

1.  **Install `uv`:**
    Follow the official installation instructions for `uv` for your operating system (e.g., `pip install uv`, `brew install uv`, etc.).

2.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

3.  **Create a virtual environment:**
    Use `uv` to create a virtual environment (e.g., in a directory named `.venv`).
    ```bash
    uv venv
    ```

4.  **Activate the virtual environment:**
    Activate the environment you just created. The command differs based on your shell:
    *   **Bash/Zsh:** `source .venv/bin/activate`
    *   **Fish:** `source .venv/bin/activate.fish`
    *   **Cmd (Windows):** `.venv\Scripts\activate.bat`
    *   **PowerShell (Windows):** `.venv\Scripts\Activate.ps1`

5.  **Install dependencies and the tool:**
    Use `uv` to install the package and its dependencies defined in `pyproject.toml` into the active virtual environment.
    ```bash
    # Installs the package 'promptbuilder' and dependencies from pyproject.toml
    uv pip install .
    ```
    *(Optional: If you have development dependencies defined under `[project.optional-dependencies]`, you might install them using `uv pip install .[dev]`)*

6.  **Verify installation:**
    With the virtual environment still active, run the help command:
    ```bash
    promptbuilder --help
    ```
    You should see the command-line help output.

## Usage Examples

**(Ensure you have activated the virtual environment created during installation before running these commands: e.g., `source .venv/bin/activate`)**

**1. Basic Task (Minimum Required for CLI):**
Generate a meta-prompt for creating a task prompt that summarizes text.

```bash
promptbuilder --task "Summarize the provided text into three key bullet points."
```
*(Output: The generated META_PROMPT will be printed to the console with Rich formatting.)*

**2. Adding Context from Files/Folders:**
Include the content of specific files or all supported files within a directory as context.

```bash
# Context from a specific file
promptbuilder --task "Explain the main function in this Python code." \
              --context ./src/main.py

# Context from all supported files (.txt, .md, .py, etc.) in a directory and subdirectories
promptbuilder --task "Summarize the key topics covered in these project documents." \
              --context ./project_docs/ \
              -v # Show verbose output about context processing
```
*(Output: META_PROMPT printed, instructing the LLM to consider the content of the specified files/folders. Verbose output shows files processed/skipped.)*

**3. Specifying Input and Output:**
Define what the final `TASK_PERFORMING_PROMPT` should expect as input and produce as output.

```bash
promptbuilder --task "Translate the user's input text from English to French." \
              --input "A single paragraph of English text." \
              --output "The French translation of the input paragraph." \
              --output-instructions "Provide only the French translation, no extra commentary. Ensure correct French grammar and accents."
```
*(Output: META_PROMPT printed, instructing the LLM to create a TASK_PERFORMING_PROMPT that includes placeholders/sections and format instructions.)*

**4. Defining Prompt Characteristics:**
Specify the persona, constraints, tone, and negative constraints for the final prompt generated by the LLM.

```bash
promptbuilder --task "Rewrite the provided paragraph to be suitable for a 5th-grade reading level." \
              --context ./complex_paragraph.txt \
              --persona "An experienced elementary school teacher explaining a concept." \
              --tone "Simple, encouraging, and clear." \
              --constraints "Use short sentences (average 10 words or less). Define any technical terms simply using analogies suitable for children aged 10-11." \
              --negative-constraints "Do not use analogies involving pop culture after 2010. Avoid passive voice. Do not exceed 150 words."
```
*(Output: META_PROMPT printed, instructing the LLM to generate a final prompt incorporating these specific characteristics.)*

**5. Using Files for Long Instructions or Examples:**
Provide detailed instructions or examples from files instead of directly on the command line. The tool will read the content of these files.

```bash
# Create instruction files first (e.g., meta_guide.txt, tone_guide.txt, example_in.txt, example_out.txt)
# meta_guide.txt: "Generate a prompt for converting code snippets. The final prompt should be very explicit about expecting only code output."
# tone_guide.txt: "Strictly technical and concise."
# example_in.txt: "def add(a, b):\n  return a + b"
# example_out.txt: "function add(a, b) {\n  return a + b;\n}"

promptbuilder --task "Convert simple Python functions to Javascript." \
              --meta-instructions ./meta_guide.txt \
              --tone ./tone_guide.txt \
              --example-input ./example_in.txt \
              --example-output ./example_out.txt \
              --context ./src/my_python_code.py
```

**6. Saving to File and Copying to Clipboard:**

```bash
promptbuilder --task "Generate five creative blog post titles about sustainable gardening." \
              --save-on-disk ./generated_prompts/gardening_meta.txt \
              --copy
```
*(Output: META_PROMPT saved to the specified file AND copied to the clipboard. Confirmation messages shown in console.)*

**7. Interactive Mode:**
Let `promptbuilder` guide you through gathering the necessary information with clear, formatted prompts. For multi-line text fields (like descriptions or examples), **press Esc then Enter to finish** that field and move to the next prompt.

```bash
promptbuilder --interactive
```
*(Output: A welcome message explains the process. Follow the interactive prompts, using double-Enter for multi-line inputs.)*

You can also combine interactive mode with pre-filled arguments:
```bash
promptbuilder -i --task "Debug Python code snippet" --context ./my_buggy_code.py
```
*(Output: Interactive mode starts, skipping prompts for `--task` and `--context` as they were provided, and guides you through the remaining fields.)*

## Command-Line Reference

```
usage: promptbuilder [OPTIONS]

Generate META_PROMPTs for instructing LLMs to create task-performing prompts.

options:
  -h, --help            show this help message and exit

Core arguments:
  --task TEXT           **(Required unless interactive)** Concise description of the ultimate task for the final LLM.
  --context PATH [PATH ...]
                        One or more file or directory paths for context. Dirs parsed recursively for supported types.
  --meta-instructions TEXT_OR_PATH
                        Instructions for the META_PROMPT generator (how to build the final prompt). Text or file path.

Input/Output Specification:
  --input TEXT_OR_PATH  Description of the expected input for the final prompt. Text or file path.
  --output TEXT_OR_PATH
                        Description of the desired output from the final prompt. Text or file path.
  --input-instructions TEXT_OR_PATH
                        Instructions for the USER on how to provide input. Text or file path.
  --output-instructions TEXT_OR_PATH
                        Instructions for the LLM on how to format output. Text or file path.

Prompt Characteristics (for the final prompt):
  --persona TEXT_OR_PATH
                        Specify the persona the final LLM should adopt (e.g., 'Helpful assistant', 'Expert Python programmer'). Text or file path.
  --constraints TEXT_OR_PATH
                        General constraints the final LLM must adhere to (e.g., 'Answer in under 100 words', 'Use only information from the context'). Text or file path.
  --tone TEXT_OR_PATH   Specify the desired tone for the final LLM's output (e.g., 'Formal', 'Casual and friendly', 'Technical'). Text or file path.
  --negative-constraints TEXT_OR_PATH
                        Specify what the final LLM should NOT do (e.g., 'Do not mention pricing', 'Avoid using jargon'). Text or file path.

Examples:
  --example-input TEXT_OR_PATH
                        An example of valid input for the final prompt. Text or file path.
  --example-output TEXT_OR_PATH
                        An example of desired output from the final prompt. Text or file path.

Output and Configuration:
  --save-on-disk PATH   Save the generated META_PROMPT to this file path instead of printing to stdout.
  --copy                Copy the generated META_PROMPT to the system clipboard.
  --config PATH         Specify a configuration file path (default search: ./.promptbuilder.yaml, ~/.config/promptbuilder/.promptbuilder.yaml).
  --template PATH       Specify a custom META_PROMPT Jinja2 template file.

Modes and Verbosity:
  -i, --interactive     Activate Interactive Mode to gather inputs via prompts.
  -v, --verbose         Increase output verbosity (-v for INFO, -vv for DEBUG). Rich logging provides detailed info.
```
*(Note: The exact appearance of the help message in your terminal depends on your environment and terminal width.)*

## Configuration (`.promptbuilder.yaml`)

You can customize default behavior by creating a configuration file named `.promptbuilder.yaml` in either:

1.  The current working directory (`./.promptbuilder.yaml`)
2.  The user's config directory (`~/.config/promptbuilder/.promptbuilder.yaml`)

The file in the current directory takes precedence. Use the `--config PATH` argument to specify an explicit location.

**Example `.promptbuilder.yaml`:**

```yaml
# Default path to the Jinja2 template for the meta-prompt
# If relative, searched relative to current working directory first.
# default_meta_prompt_template_path: custom_templates/my_meta_prompt.j2

# Format string for placeholders like {{INPUT}}, {{OUTPUT}} in the *final* prompt
# The meta-prompt will instruct the LLM to use this format.
placeholder_format: "__%s__" # Default is "{{%s}}"

# Maximum size (in MB) for individual context files to be included.
# Set to 0 or comment out for effectively no limit (within memory constraints).
context_max_file_size_mb: 10.0 # Default is 0.3

# List of file extensions (case-insensitive on Windows/macOS) to include
# when parsing context directories recursively. Ensure they start with a '.'
context_supported_extensions:
  - .py
  - .md
  - .txt
  - .rst
  - .json
  - .yaml
  - .java
  - .c
  - .cpp
  - .h
  - .hpp
  # Default includes .txt, .md, .py, .json, .yaml, .xml, .csv, .html, .css, .js

# Default text encoding for reading context files.
context_encoding: utf-8 # Default is utf-8

# If true, automatically select 'yes' for copying to clipboard in interactive mode
# if --copy is not specified. The --copy flag always overrides this.
copy_to_clipboard_default: true # Default is true

# Default directory to resolve relative paths specified with --save-on-disk.
# If --save-on-disk provides an absolute path, this is ignored.
output_dir: ./generated_meta_prompts # Default is "." (current directory)
```

## Template Customization

The structure and wording of the generated META_PROMPT are controlled by a [Jinja2](https://jinja.palletsprojects.com/) template.

*   **Default Template:** Located within the installed package at `promptbuilder/templates/default_meta_prompt.j2`. You can copy and modify this.
*   **Custom Template:** Use the `--template PATH/TO/YOUR/template.j2` argument to specify your own template file.

Your custom template can access the data collected from command-line arguments or interactive mode. Key variables available in the template context include:

*   `task_description`: The core task string.
*   `meta_instructions`: String content from `--meta-instructions` (potentially read from file).
*   `input_description`, `output_description`, `input_instructions`, `output_instructions`: Strings from corresponding arguments (potentially read from file).
*   `persona`, `constraints`, `tone`, `negative_constraints`: Strings from corresponding arguments (potentially read from file), or `None` if not provided.
*   `example_input`, `example_output`: Strings from corresponding arguments (potentially read from file).
*   `context_items`: A list of tuples `(relative_path_string, content_string)` for each included context file.
*   `context_files_processed`: Integer count of files successfully included.
*   `context_files_skipped`: Integer count of files skipped due to limits/errors/filters.
*   `config`: The loaded `Config` object itself (e.g., access `config.context_max_file_size_mb`).
*   `placeholder(name)`: A function that returns the placeholder string using the configured format (e.g., `placeholder('INPUT')` might return `{{INPUT}}` or `__INPUT__`).
*   `verbose_level`: Integer indicating verbosity level (0, 1, or 2+).

Review the `default_meta_prompt.j2` file for examples of how these variables are used.

## Future Considerations (Optional Enhancements)

*   **Advanced Context Modes:** Option to automatically summarize very large context files before inclusion to save tokens, possibly using a simpler LLM call or heuristics.
*   **Direct LLM Interaction:** Add optional flags (`--execute-with <llm_api_config>`) to directly send the generated META_PROMPT to a configured LLM API (e.g., OpenAI, Anthropic, local Ollama) and display/save the resulting TASK_PERFORMING_PROMPT.
*   **Prompt Library:** Implement commands (`promptbuilder save <name>`, `promptbuilder load <name>`, `promptbuilder list`) to manage generated META_PROMPTs and perhaps associated TASK_PERFORMING_PROMPTs locally.
*   **Syntax Highlighting:** Automatically apply syntax highlighting using Rich when printing context file contents or code examples to the console during processing or in the final output.
*   **Template Variables Validation:** Add checks within the template rendering to warn if expected variables (like `task_description`) are missing, aiding custom template development.
*   **More Output Formats:** Option to output the META_PROMPT in JSON or other structured formats besides plain text.
*   **Dependency Locking:** Consider adding instructions for `uv pip compile` to generate a `requirements.lock` file for reproducible builds, and updating the install instructions to use `uv pip sync requirements.lock`.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues on the project repository. For significant changes, please open an issue first to discuss the approach.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details. (You should add a `LICENSE` file with the MIT License text if you intend to use it).
```

### FILE: `pyproject.toml`
```toml
[project]
name = "promptbuilder"
version = "0.1.1" # Increment version
# ... other project metadata ...
requires-python = ">=3.8"
dependencies = [
  "pyyaml>=6.0",
  "jinja2>=3.1",
  "pyperclip>=1.8", # Added rich
  "rich>=13.0",
  "prompt-toolkit>=3.0.51",
]

[project.scripts]
promptbuilder = "promptbuilder.cli:main"

[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]
```

### FILE: `test_ptk.py`
```py
# test_ptk.py
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.input.defaults import create_input
from prompt_toolkit.output.defaults import create_output
import sys
import os

print("--- Prompt Toolkit Minimal Test ---")
print(f"Python version: {sys.version}")
print(f"TERM environment variable: {os.environ.get('TERM', 'Not Set')}")

# Create a session with explicit I/O
session = PromptSession(
    history=InMemoryHistory(),
    auto_suggest=AutoSuggestFromHistory(),
    input=create_input(),
    output=create_output()
)

print("\nEnter multi-line text below.")
print("Try using arrow keys, Home, End, Delete etc.")
print("Press Esc -> Enter to finish.")
print("-" * 20)

try:
    text = session.prompt(
        "> ",
        multiline=True
    )
    print("\n" + "-" * 20)
    print("--- Input Received ---")
    if text is not None:
        print(repr(text)) # Show exact representation including newlines
    else:
        print("Received None (likely EOF)")
    print("--------------------")

except KeyboardInterrupt:
    print("\nInput cancelled (Ctrl+C).")
except EOFError:
    print("\nEOF detected.")
except Exception as e:
    print(f"\nAn error occurred: {e}")
    import traceback
    traceback.print_exc() # Print full traceback if prompt fails unexpectedly

print("Test finished.")
```

## FOLDER: `src`

```text

```

## FOLDER: `src/promptbuilder`

```text

```

### FILE: `src/promptbuilder/__init__.py`
```py
# Optional: Define package-level items or leave empty
# You could set up root logger here if desired, but basicConfig in cli.py is fine too.
import logging

# Configure the root logger for the package
# logging.getLogger(__name__).addHandler(logging.NullHandler())
```

### FILE: `src/promptbuilder/__main__.py`
```py
# This allows running the package using 'python -m promptbuilder'
import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())
```

### FILE: `src/promptbuilder/cli.py`
```py
# promptbuilder/cli.py
import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Rich imports
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel

from . import config as cfg
from . import context
from . import templating
from . import utils
from . import interactive

# --- Rich Setup ---
# Use a global console object for convenience in a CLI app
console = Console()
# Configure logging to use RichHandler
logging.basicConfig( # Keep basicConfig for initial level setting, but configure handlers below
    level=logging.WARNING, format="%(message)s", datefmt="[%X]", handlers=[] # No default handlers initially
)
# Get the root logger for the promptbuilder package specifically, or the root logger if preferred
# Using a specific logger allows finer control if this tool becomes part of a larger app
# logger = logging.getLogger('promptbuilder')
# Or configure the root logger directly:
logger = logging.getLogger() # Configure root logger
logger.addHandler(RichHandler(console=console, rich_tracebacks=True, markup=True))
# Set initial level - setup_logging will adjust this
logger.setLevel(logging.WARNING)

# Note: We are configuring the root logger here. If you wanted ONLY promptbuilder logs
# to use RichHandler, you'd get logging.getLogger('promptbuilder') and add the handler there.
# Configuring the root logger makes *all* logging (including libraries if they log) use Rich.

def setup_logging(verbose_level: int):
    """Configures logging level based on verbosity."""
    if verbose_level == 1:
        logger.setLevel(logging.INFO)
        logger.info("Verbose mode enabled (INFO level)")
    elif verbose_level >= 2:
        logger.setLevel(logging.DEBUG)
        logger.info("Verbose mode enabled (DEBUG level)")
    # Else: keep default (WARNING) setup above


def create_parser() -> argparse.ArgumentParser:
    """Creates the argument parser for the CLI."""
    # (Parser definition remains largely the same, help text will be standard)
    # ... (keep existing parser code) ...
    parser = argparse.ArgumentParser(
        description="Generate META_PROMPTs for instructing LLMs to create task-performing prompts.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Core arguments
    core_group = parser.add_argument_group('Core arguments')
    core_group.add_argument(
        "--task",
        type=str,
        help="**(Required unless interactive)** Concise description of the ultimate task for the final LLM."
    )
    core_group.add_argument(
        "--context",
        type=str,
        nargs='+',  # Allows one or more paths
        help="One or more file or directory paths for context. Dirs parsed recursively for supported types."
    )
    core_group.add_argument(
        "--meta-instructions",
        metavar="TEXT_OR_PATH",
        help="Instructions for the META_PROMPT generator (how to build the final prompt). Text or file path."
    )

    # Input/Output Specification
    io_group = parser.add_argument_group('Input/Output Specification')
    io_group.add_argument(
        "--input",
        metavar="TEXT_OR_PATH",
        help="Description of the expected input for the final prompt. Text or file path."
    )
    io_group.add_argument(
        "--output",
        metavar="TEXT_OR_PATH",
        help="Description of the desired output from the final prompt. Text or file path."
    )
    io_group.add_argument(
        "--input-instructions",
        metavar="TEXT_OR_PATH",
        help="Instructions for the USER on how to provide input. Text or file path."
    )
    io_group.add_argument(
        "--output-instructions",
        metavar="TEXT_OR_PATH",
        help="Instructions for the LLM on how to format output. Text or file path."
    )

    # Prompt Characteristics (NEW GROUP)
    char_group = parser.add_argument_group('Prompt Characteristics (for the final prompt)')
    char_group.add_argument(
        "--persona",
        metavar="TEXT_OR_PATH",
        help="Specify the persona the final LLM should adopt (e.g., 'Helpful assistant', 'Expert Python programmer'). Text or file path."
    )
    char_group.add_argument(
        "--constraints",
        metavar="TEXT_OR_PATH",
        help="General constraints the final LLM must adhere to (e.g., 'Answer in under 100 words', 'Use only information from the context'). Text or file path."
    )
    char_group.add_argument(
        "--tone",
        metavar="TEXT_OR_PATH", # Allow file path for more complex tone descriptions
        help="Specify the desired tone for the final LLM's output (e.g., 'Formal', 'Casual and friendly', 'Technical'). Text or file path."
    )
    char_group.add_argument(
        "--negative-constraints",
        metavar="TEXT_OR_PATH",
        help="Specify what the final LLM should NOT do (e.g., 'Do not mention pricing', 'Avoid using jargon'). Text or file path."
    )

    # Examples
    example_group = parser.add_argument_group('Examples')
    example_group.add_argument(
        "--example-input",
        metavar="TEXT_OR_PATH",
        help="An example of valid input for the final prompt. Text or file path."
    )
    example_group.add_argument(
        "--example-output",
        metavar="TEXT_OR_PATH",
        help="An example of desired output from the final prompt. Text or file path."
    )

    # Output and Configuration
    output_group = parser.add_argument_group('Output and Configuration')
    output_group.add_argument(
        "--save-on-disk",
        metavar="PATH",
        help="Save the generated META_PROMPT to this file path instead of printing to stdout."
    )
    output_group.add_argument(
        "--copy",
        action="store_true",
        help="Copy the generated META_PROMPT to the system clipboard."
    )
    output_group.add_argument(
        "--config",
        metavar="PATH",
        help=f"Specify a configuration file path (default search: ./{cfg.DEFAULT_CONFIG_FILENAME}, {cfg.CONFIG_SEARCH_PATHS[1]})."
    )
    output_group.add_argument(
        "--template",
        metavar="PATH",
        help="Specify a custom META_PROMPT Jinja2 template file."
    )

    # Modes and Verbosity
    mode_group = parser.add_argument_group('Modes and Verbosity')
    mode_group.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Activate Interactive Mode to gather inputs via prompts."
    )
    mode_group.add_argument(
        "-v", "--verbose",
        action="count",
        default=0,
        help="Increase output verbosity (-v for INFO, -vv for DEBUG)."
    )
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()

    setup_logging(args.verbose) # Configure logging level based on -v flags

    # Load configuration
    config = cfg.Config.load(args.config)
    if args.verbose > 0:
        # logger.info(f"Loaded configuration: {config}") # Logger handles this now
        pass # Logging is handled by setup_logging and logger calls

    collected_data: Optional[Dict[str, Any]] = None
    final_actions = {
        'save_path': args.save_on_disk,
        'copy_flag': args.copy or (config.copy_to_clipboard_default if hasattr(config, 'copy_to_clipboard_default') else False),
    }

    if args.interactive:
        logger.info("Starting interactive mode...")
        # Pass the console object to interactive mode
        interactive_results = interactive.run_interactive_mode(args, config, console)
        if interactive_results is None:
            console.print("[yellow]Interactive mode cancelled.[/yellow]")
            sys.exit(0) # User cancelled
        collected_data = interactive_results
        # Pop actions data collected interactively
        final_actions['save_path'] = collected_data.pop('save_path', final_actions['save_path'])
        final_actions['copy_flag'] = collected_data.pop('copy_flag', final_actions['copy_flag'])
    else:
        # CLI Mode
        if not args.task:
            parser.print_help() # Use parser's help printer
            console.print("\n[bold red]Error:[/bold red] --task is required in non-interactive mode.")
            sys.exit(1)

        logger.info("Running in CLI mode...")
        # Collect data from args (no change needed here)
        collected_data = {
            'task_description': args.task,
            'context_paths': args.context,
            'meta_instructions_src': args.meta_instructions,
            'input_desc_src': args.input,
            'input_instr_src': args.input_instructions,
            'output_desc_src': args.output,
            'output_instr_src': args.output_instructions,
            'persona_src': args.persona,
            'constraints_src': args.constraints,
            'tone_src': args.tone,
            'negative_constraints_src': args.negative_constraints,
            'example_input_src': args.example_input,
            'example_output_src': args.example_output,
        }
        # final_actions already set from args/config

    # --- Common Processing (Both Modes) ---

    # Resolve text/path arguments using utils.read_text_or_path
    # This part remains the same logic, utils handles logging now
    template_data: Dict[str, Any] = {
         'task_description': collected_data.get('task') or collected_data.get('task_description'),
         'meta_instructions': utils.read_text_or_path(collected_data.get('meta_instructions_src'), config.context_encoding, 'meta-instructions', console),
         'input_description': utils.read_text_or_path(collected_data.get('input_desc_src'), config.context_encoding, 'input description', console),
         'input_instructions': utils.read_text_or_path(collected_data.get('input_instr_src'), config.context_encoding, 'input instructions', console),
         'output_description': utils.read_text_or_path(collected_data.get('output_desc_src'), config.context_encoding, 'output description', console),
         'output_instructions': utils.read_text_or_path(collected_data.get('output_instr_src'), config.context_encoding, 'output instructions', console),
         'persona': utils.read_text_or_path(collected_data.get('persona_src'), config.context_encoding, 'persona', console),
         'constraints': utils.read_text_or_path(collected_data.get('constraints_src'), config.context_encoding, 'constraints', console),
         'tone': utils.read_text_or_path(collected_data.get('tone_src'), config.context_encoding, 'tone', console),
         'negative_constraints': utils.read_text_or_path(collected_data.get('negative_constraints_src'), config.context_encoding, 'negative constraints', console),
         'example_input': utils.read_text_or_path(collected_data.get('example_input_src'), config.context_encoding, 'example input', console),
         'example_output': utils.read_text_or_path(collected_data.get('example_output_src'), config.context_encoding, 'example output', console),
         'verbose_level': args.verbose,
         'config': config,
    }

    # Process context
    context_items = []
    context_files_processed = 0
    context_files_skipped = 0
    context_paths_to_parse = collected_data.get('context_paths', [])
    if context_paths_to_parse:
         logger.info("Processing context paths...")
         # Pass console to context parser for rich warnings/errors if needed inside
         context_items, context_files_processed, context_files_skipped = context.parse_context_paths(
             context_paths_to_parse,
             config,
             console, # Pass console
             args.verbose
         )
    template_data['context_items'] = context_items
    template_data['context_files_processed'] = context_files_processed
    template_data['context_files_skipped'] = context_files_skipped


    # Determine template path
    template_path = Path(args.template) if args.template else config.default_meta_prompt_template_path

    # Generate META_PROMPT
    logger.info("Generating META_PROMPT...")
    # Pass console to templating for rich errors if needed inside
    meta_prompt = templating.render_meta_prompt(template_path, template_data, config, console)

    if not meta_prompt:
        # Error already logged by render_meta_prompt via logger
        sys.exit(1)

    # --- Output Actions ---
    output_performed = False
    # 1. Save to Disk
    save_target_str = final_actions.get('save_path')
    if save_target_str:
        save_path = Path(save_target_str)
        # Resolve relative to output_dir from config if path is not absolute
        if not save_path.is_absolute() and config.output_dir:
             # Make output_dir absolute relative to CWD if it's not already
             abs_output_dir = config.output_dir.resolve()
             save_path = abs_output_dir / save_path
        else:
             # If save_path is absolute or output_dir is '.', resolve normally
             save_path = save_path.resolve()

        # Pass console to save function
        if utils.save_to_disk(meta_prompt, save_path, console):
             output_performed = True
        else:
             # Error logged by save_to_disk
             pass # Proceed without saving


    # 2. Copy to Clipboard
    if final_actions.get('copy_flag'):
        # Pass console to copy function
        if utils.copy_to_clipboard(meta_prompt, console):
            output_performed = True
        else:
             # Error logged by copy_to_clipboard
             pass # Proceed without copying

    # 3. Print to Stdout using Rich
    if not output_performed or (not save_target_str and not final_actions.get('copy_flag')):
         separator = False
         if output_performed: # Add a separator only if other actions *succeeded* but stdout is still needed
              separator = True
         elif save_target_str or final_actions.get('copy_flag'): # Add separator if actions were *attempted* but maybe failed
              separator = True

         if separator:
             console.print("\n---\n[bold cyan]Generated META_PROMPT:[/bold cyan]")
         else: # Only printing to stdout
             console.print("[bold cyan]Generated META_PROMPT:[/bold cyan]")

         # Optionally use Markdown or Syntax highlighting if the prompt format warrants it
         # console.print(Markdown(meta_prompt))
         console.print(meta_prompt) # Print plain text for now

    logger.info("PromptBuilder finished.")
    sys.exit(0)


if __name__ == '__main__':
    main()
```

### FILE: `src/promptbuilder/config.py`
```py
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
```

### FILE: `src/promptbuilder/context.py`
```py
# promptbuilder/context.py
import logging
import os
from pathlib import Path
from typing import List, Optional, Tuple, Set

# Rich imports (only needed if direct printing is done here, logger handles most)
# from rich.console import Console

from .config import Config

# Use the logger configured in cli.py
logger = logging.getLogger(__name__)

ContextInfo = Tuple[str, Optional[str]]

def parse_context_paths(
    paths: List[str],
    config: Config,
    console: 'Console', # Type hint for console (forward reference)
    verbose_level: int = 0
) -> Tuple[List[ContextInfo], int, int]:
    """
    Parses context paths (files/directories), applying configuration limits.
    Uses absolute paths for processing but returns relative paths for display.

    Returns:
        Tuple containing:
        - List of ContextInfo tuples: (relative_path_string, content_or_summary).
        - Total number of files processed internally (attempted reads).
        - Total number of files skipped (filtered out or read errors).
    """
    context_items: List[ContextInfo] = []
    processed_files_count = 0 # Files actually read or attempted to read
    skipped_files_count = 0   # Files skipped due to filters, errors, not found etc.
    max_bytes = int(config.context_max_file_size_mb * 1024 * 1024)
    supported_ext_set = set(config.context_supported_extensions)
    # Use case-insensitive matching for extensions on case-insensitive filesystems like Windows
    is_case_insensitive_fs = os.path.normcase('A') == os.path.normcase('a')
    if is_case_insensitive_fs:
        supported_ext_set = {ext.lower() for ext in supported_ext_set}

    processed_real_paths: Set[Path] = set() # Keep track of canonical paths to avoid duplicates
    files_to_process: List[Tuple[Path, str]] = [] # Store (absolute_path, original_user_path_str)
    cwd = Path.cwd()

    if not paths:
        return [], 0, 0

    # 1. Collect all potential files using absolute paths for reliability
    for path_str in paths:
        input_path = Path(path_str)
        try:
            # Resolve symlinks and make absolute. strict=True raises error if not found.
            absolute_path = input_path.resolve(strict=True)
            # Use realpath to get the canonical path for duplicate checking
            real_path = absolute_path.resolve() # Or Path(os.path.realpath(absolute_path)) for older python? resolve should be enough.
        except FileNotFoundError:
             logger.warning(f"Context path not found: [yellow]{path_str}[/yellow]")
             skipped_files_count += 1
             continue
        except Exception as e:
             logger.error(f"Error resolving path [red]{path_str}[/red]: {e}")
             skipped_files_count += 1
             continue

        if real_path in processed_real_paths:
             logger.debug(f"Skipping already processed path: {path_str} (resolved: {absolute_path})")
             continue
        processed_real_paths.add(real_path) # Add the canonical path

        if absolute_path.is_file():
            files_to_process.append((absolute_path, path_str)) # Keep track of original input path string too
        elif absolute_path.is_dir():
            logger.info(f"Recursively searching directory: [blue]{path_str}[/blue] (resolved: {absolute_path})")
            try:
                items_in_dir = 0
                skipped_in_dir = 0
                # Use Path.rglob for robust recursive globbing
                for item in absolute_path.rglob('*'):
                    items_in_dir += 1
                    try:
                        # Check if item exists and is a file before resolving (performance)
                        if item.is_file():
                            item_resolved = item.resolve(strict=True) # Resolve items found during iteration
                            item_real_path = item_resolved.resolve()
                            if item_real_path not in processed_real_paths:
                                files_to_process.append((item_resolved, str(item))) # Use item path as 'original' here
                                processed_real_paths.add(item_real_path)
                            # else: ignore duplicate file found via recursive search
                        # else: ignore subdirectories explicitly found by rglob
                    except FileNotFoundError:
                        # File might have been deleted between rglob and resolve
                         logger.debug(f"Item no longer exists, skipping: {item}")
                         skipped_in_dir += 1
                         skipped_files_count += 1
                    except Exception as e:
                         logger.warning(f"Skipping item within directory [yellow]{absolute_path}[/yellow] due to resolve error: {item} ({e})")
                         skipped_in_dir += 1
                         skipped_files_count += 1
                if verbose_level > 0:
                    logger.info(f"Directory scan [blue]{path_str}[/blue]: Found {items_in_dir} items, skipped {skipped_in_dir} during scan.")

            except OSError as e:
                 logger.error(f"Error scanning directory [red]{absolute_path}[/red]: {e}")
                 # Hard to estimate how many files were missed, maybe add 1 skipped?
                 skipped_files_count +=1


    # 2. Process collected absolute file paths
    for file_path, original_path_str in files_to_process: # file_path is an absolute Path object
        processed_files_count += 1 # Increment for every file we attempt to process

        # --- Calculate relative path for display ---
        try:
            relative_display_path = os.path.relpath(file_path, cwd)
        except ValueError:
            # Fallback to absolute path string if relative path fails (e.g., different drives)
            logger.debug(f"Could not determine relative path for {file_path}. Using absolute path for display.")
            relative_display_path = str(file_path)

        logger.debug(f"Processing context file: {file_path} (displaying as: {relative_display_path})")

        # Check extension
        file_suffix = file_path.suffix
        check_suffix = file_suffix.lower() if is_case_insensitive_fs else file_suffix
        if check_suffix not in supported_ext_set:
            if verbose_level > 0:
                logger.info(f"Skipping file (unsupported extension '[dim]{file_suffix}[/dim]'): [yellow]{relative_display_path}[/yellow]")
            skipped_files_count += 1
            processed_files_count -= 1 # Don't count skipped files in the *processed* count
            continue

        # Check size
        try:
            file_size = file_path.stat().st_size
            if max_bytes > 0 and file_size > max_bytes: # Allow max_bytes=0 for no limit? Add config option?
                logger.warning(f"Skipping file (size {file_size / (1024*1024):.2f} MB > limit {config.context_max_file_size_mb} MB): [yellow]{relative_display_path}[/yellow]")
                skipped_files_count += 1
                processed_files_count -= 1 # Don't count skipped files in the *processed* count
                continue
            if file_size == 0:
                 logger.info(f"Including empty file: [dim]{relative_display_path}[/dim]")
                 context_items.append((relative_display_path, ""))
                 # processed_files_count remains incremented, it was processed.
                 continue

        except OSError as e:
            logger.error(f"Error accessing file metadata [red]{relative_display_path}[/red]: {e}")
            skipped_files_count += 1
            processed_files_count -= 1 # Don't count error files in the *processed* count
            continue

        # Read content
        try:
            content = file_path.read_text(encoding=config.context_encoding)
            # Store relative path in results
            context_items.append((relative_display_path, content))
            if verbose_level > 1:
                 logger.debug(f"Successfully read content from: [green]{relative_display_path}[/green]")
            # processed_files_count remains incremented
        except UnicodeDecodeError:
            logger.warning(f"Skipping file (encoding error with '[cyan]{config.context_encoding}[/cyan]'): [yellow]{relative_display_path}[/yellow]")
            skipped_files_count += 1
            processed_files_count -= 1
        except IOError as e:
            logger.error(f"Error reading file [red]{relative_display_path}[/red]: {e}")
            skipped_files_count += 1
            processed_files_count -= 1
        except Exception as e:
            logger.error(f"Unexpected error reading file [red]{relative_display_path}[/red]: {e}", exc_info=True)
            skipped_files_count += 1
            processed_files_count -= 1


    actual_included = len(context_items)
    # Adjust final counts: total_attempts is the size of files_to_process
    total_attempts = len(files_to_process)
    # Skipped count should reflect filters + errors encountered during processing phase
    # The initial skipped_files_count covers path resolution errors etc.
    final_skipped_count = skipped_files_count + (total_attempts - actual_included)

    if verbose_level > 0 or final_skipped_count > 0 : # Report summary if verbose or if files were skipped
         logger.info(f"Context processing summary: Files attempted={total_attempts}, Included=[green]{actual_included}[/green], Skipped=[yellow]{final_skipped_count}[/yellow]")

    # Return list of (relative_path_str, content) tuples
    # Return the count of files successfully included, and the count of files skipped
    return context_items, actual_included, final_skipped_count
```

### FILE: `src/promptbuilder/example.promptbuilder.yaml`
```yaml
# Default path to the Jinja2 template for the meta-prompt
# default_meta_prompt_template_path: /path/to/your/custom/template.j2

# Format string for placeholders like {{INPUT}}, {{OUTPUT}} in the *final* prompt
# The meta-prompt will instruct the LLM to use this format.
placeholder_format: "__%s__" # Default is "{{%s}}"

# Maximum size (in MB) for individual context files to be included. Set to 0 for no limit.
context_max_file_size_mb: 10.0 # Default is 0.3

# List of file extensions to include when parsing context directories recursively.
# Ensure they start with a '.'
context_supported_extensions:
  - .py
  - .md
  - .txt
  - .rst
  - .json
  - .yaml
  # Default includes .txt, .md, .py, .json, .yaml, .xml, .csv, .html, .css, .js

# Default text encoding for reading context files.
context_encoding: utf-8 # Default is utf-8

# If true, automatically copy generated prompts to clipboard unless --copy=False (hypothetical) is used.
# Affects the default choice in interactive mode if --copy is not specified.
copy_to_clipboard_default: true # Default is true

# Default directory to resolve relative paths when using --save-on-disk without an absolute path.
output_dir: ./generated_prompts # Default is "." (current directory)
```

### FILE: `src/promptbuilder/interactive.py`
```py
# src/promptbuilder/interactive.py

import logging
import shlex
import os  # Needed for os.path.sep
import sys  # For sys.exit
from pathlib import Path
from typing import Dict, Any, Optional, List

# Rich imports (Only for OUTPUT formatting now)
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text
from rich.syntax import Syntax
from rich.markup import escape  # To safely display user input

from .config import Config

# Import ALL input functions from utils now AND path_completer
from .utils import (
    get_single_line_input,
    get_multiline_input,
    get_yesno_confirmation,
    validate_path_input,
    path_completer,
)

# Use the logger configured in cli.py
logger = logging.getLogger(__name__)

# Multi-line prompt guide (remains the same)
MULTILINE_PROMPT_GUIDE = Text.from_markup(
    "\n[dim]Enter text below. Press [bold]Esc[/bold] then [bold]Enter[/bold] to finish.[/dim]"
    "\n[dim](Allows multi-line editing with arrow keys, Home/End, etc.)[/dim]"
)


def run_interactive_mode(
    cli_args: Any, config: Config, console: Console
) -> Optional[Dict[str, Any]]:
    """Runs the interactive prompting session using ONLY prompt_toolkit for input."""
    collected_data: Dict[str, Any] = {}
    # Initialize actions based on CLI args and config defaults
    final_actions = {
        "save_path": cli_args.save_on_disk,
        "copy_flag": True,  # Default to True for interactive mode
    }

    console.print(Rule("[bold cyan]PromptBuilder Interactive Mode[/bold cyan]"))
    console.print()
    console.print(
        Panel(  # Rich Panel for output
            Text.from_markup(
                "This interactive mode will guide you through providing the details needed to generate a [bold]META_PROMPT[/bold].\n"
                "The META_PROMPT contains instructions for a Large Language Model (LLM) to create a final, task-specific prompt for you.\n\n"
                "[yellow]Tip:[/yellow] You can provide file paths for many fields. If the path exists, its content will be read.\n"
                "[yellow]Tip:[/yellow] Press [bold]Ctrl+C[/bold] at any prompt to cancel and exit."
            ),
            title="Welcome!",
            border_style="blue",
            expand=False,
        )
    )
    console.print(
        "[dim](Leave optional fields blank and press Enter to skip)[/dim]"
    )

    # --- Main Interactive Loop ---
    try:  # Wrap the main input gathering in try...except KeyboardInterrupt
        # 1. Task (Required)
        console.print()  # Add space before
        console.print(Rule("Core Task"))
        console.print()
        if cli_args.task:
            console.print(
                f"Using Task from command line: [green]'{escape(cli_args.task)}'[/green]"
            )
            collected_data["task"] = cli_args.task
        else:
            while "task" not in collected_data or not collected_data["task"]:
                task = get_single_line_input(
                    console, "Enter the ultimate task description (Required): "
                )
                if task:
                    collected_data["task"] = task
                else:
                    console.print(
                        "[prompt.invalid]Task description cannot be empty."
                    )
        # console.print() # Space after task input (optional, rule provides separation)

        # 2. Context (Optional, Multiple) - Use path_completer
        console.print()  # Add space before
        console.print(Rule("Context Files/Folders"))
        console.print()
        if cli_args.context:
            console.print(
                f"Using Context paths from command line: [green]{', '.join(escape(p) for p in cli_args.context)}[/green]"
            )
            collected_data["context_paths"] = cli_args.context
        else:
            context_paths = []
            console.print(
                "[dim]Enter paths to files or folders for context. Dirs searched recursively.[/dim]"
            )
            console.print(
                f"[dim]Supported extensions: {', '.join(config.context_supported_extensions)}[/dim]"
            )
            console.print(
                "[dim]Enter a blank line when finished. Press TAB to autocomplete paths.[/dim]"
            )
            while True:
                path_str = get_single_line_input(
                    console, "Add context path: ", completer=path_completer
                )
                if not path_str:
                    break  # Finished
                validated_path = validate_path_input(
                    path_str, check_exists=True, console=None
                )
                if validated_path:
                    if validated_path.exists():
                        context_paths.append(str(validated_path))
                        console.print(  # Feedback is okay close to input
                            f"[info]Added: {escape(str(validated_path))}[/info]"
                        )
                    else:
                        console.print(
                            f"[warning]Path does not exist or is not accessible: [yellow]{escape(str(validated_path))}[/yellow][/warning]"
                        )
                else:
                    console.print(
                        f"[error]Invalid path format: [yellow]{escape(path_str)}[/yellow][/error]"
                    )
            # Print summary of context paths after loop
            console.print()  # Add space after loop
            if context_paths:
                collected_data["context_paths"] = context_paths
                console.print(f"Collected {len(context_paths)} context path(s).")
            else:
                console.print("No context paths provided.")
                collected_data["context_paths"] = None

        # Define fields to iterate through
        fields_to_ask = [
            (
                "meta_instructions_src",
                "Meta Instructions",
                "Guidance for the prompt generator (how to build the final prompt).",
                "> ",
                True,
                None,
            ),
            (
                "input_desc_src",
                "Input Description",
                "What the final prompt expects as input.",
                "> ",
                True,
                None,
            ),
            (
                "input_instr_src",
                "Input Instructions",
                "How the end-user should provide input to the final prompt.",
                "> ",
                True,
                "input_desc_src",
            ),
            (
                "output_desc_src",
                "Output Description",
                "What the final prompt should produce as output.",
                "> ",
                True,
                None,
            ),
            (
                "output_instr_src",
                "Output Instructions",
                "How the LLM should format the output of the final prompt.",
                "> ",
                True,
                "output_desc_src",
            ),
            (
                "persona_src",
                "Persona",
                "Specify the persona the final LLM should adopt (e.g., 'Expert Python programmer').",
                "Persona: ",
                False,
                None,
            ),
            (
                "constraints_src",
                "Constraints",
                "General constraints the final LLM must adhere to (e.g., 'Answer in under 100 words').",
                "> ",
                True,
                None,
            ),
            (
                "tone_src",
                "Tone",
                "Specify the desired tone for the final LLM's output (e.g., 'Formal', 'Casual').",
                "Tone: ",
                False,
                None,
            ),
            (
                "negative_constraints_src",
                "Negative Constraints",
                "Specify what the final LLM should NOT do (e.g., 'Do not mention pricing').",
                "> ",
                True,
                None,
            ),
            (
                "example_input_src",
                "Example Input",
                "An example of valid input for the final prompt.",
                "> ",
                True,
                None,
            ),
            (
                "example_output_src",
                "Example Output",
                "An example of desired output from the final prompt.",
                "> ",
                True,
                None,
            ),
        ]

        # Iterate through optional fields
        for (
            key,
            rule_title,
            description_dim,
            input_prompt,
            is_multiline,
            depends_on_key,
        ) in fields_to_ask:
            dependency_key_base = (
                depends_on_key.replace("_src", "") if depends_on_key else None
            )
            if depends_on_key and not (
                collected_data.get(depends_on_key)
                or getattr(cli_args, dependency_key_base, None)
            ):
                logger.debug(
                    f"Skipping '{rule_title}' because dependency '{depends_on_key}' is not met."
                )
                collected_data[key] = None
                continue

            console.print()  # Add space before rule
            console.print(Rule(rule_title))
            cli_arg_name = key.replace("_src", "")
            cli_value = getattr(cli_args, cli_arg_name, None)

            if cli_value:
                console.print(
                    f"Using value from command line: [green]'{escape(str(cli_value))}'[/green]"
                )
                collected_data[key] = cli_value
                # No input needed, maybe add space after this message?
                # console.print() # Optional space after CLI value message
            else:
                console.print(
                    f"[dim]{description_dim} (Optional, leave blank to skip)[/dim]"
                )

                if is_multiline:
                    console.print(
                        MULTILINE_PROMPT_GUIDE
                    )  # Shows simplified instruction now
                    user_input = get_multiline_input(console, input_prompt)
                else:
                    # No completer needed for these general single-line fields
                    user_input = get_single_line_input(console, input_prompt)

                if user_input:
                    collected_data[key] = user_input.strip()
                else:
                    collected_data[key] = None
                # console.print() # Optional space after input field

        # --- Confirmation ---
        console.print()  # Add space before summary
        console.print(Rule("Summary"))
        console.print()

        # Helper function (no changes needed)
        def format_summary_value(
            key: str, data: dict, max_len=100
        ) -> Text:
            # (implementation unchanged)
            value = data.get(key)
            if key == "context_paths":
                if value and isinstance(value, list):
                    paths_str = ", ".join(f"'{escape(p)}'" for p in value)
                    if len(paths_str) > max_len:
                        paths_str = paths_str[: max_len - 3] + "..."
                    return Text(
                        f"{len(value)} path(s): {paths_str}", style="green"
                    )
                else:
                    return Text("None", style="dim")
            elif isinstance(value, str) and value:
                escaped_value = escape(value)
                display_value = escaped_value.replace("\n", "\\n")
                if len(display_value) > max_len:
                    display_value = display_value[: max_len - 3] + "..."
                return Text(f"'{display_value}'", style="green")
            elif value:
                return Text(f"{escape(str(value))}", style="green")
            else:
                return Text("None", style="dim")

        # Build the summary content (no changes needed)
        summary_content = Text()
        key_display_map = {
            "task": "Task",
            "context_paths": "Context Paths",
            "meta_instructions_src": "Meta Instructions",
            "input_desc_src": "Input Description",
            "input_instr_src": "Input Instructions",
            "output_desc_src": "Output Description",
            "output_instr_src": "Output Instructions",
            "persona_src": "Persona",
            "constraints_src": "Constraints",
            "tone_src": "Tone",
            "negative_constraints_src": "Negative Constraints",
            "example_input_src": "Example Input",
            "example_output_src": "Example Output",
        }
        num_items = len(key_display_map)
        for i, (key, display_name) in enumerate(key_display_map.items()):
            value_text = format_summary_value(key, collected_data)
            summary_content.append(f"{display_name}: ", style="bold")
            summary_content.append(value_text)
            if i < num_items - 1:
                summary_content.append("\n")

        console.print(
            Panel(
                summary_content,
                title="Collected Information",
                border_style="blue",
                expand=False,
            )
        )

        # --- Proceed Prompt (using standard input) ---
        console.print(
            # Use Markup directly here for the prompt text
            "\n[white]Press [bold]ENTER[/bold] to generate the prompt, or [bold]Ctrl+C[/bold] to cancel.[/white]"
        )
        input()  # Wait for Enter or Ctrl+C
        console.print()  # Add space after proceed confirmation

        # --- Final Actions ---
        console.print(Rule("Final Actions"))
        console.print()
        # Save to disk
        if not cli_args.save_on_disk:
            # Print the prompt text manually using console.print
            console.print(
                "Save prompt to disk? (Enter path or leave blank for stdout): ",
                end="",  # Prevent extra newline before input()
            )
            # Use standard input()
            save_path_str = input()

            if save_path_str:
                save_path_str = save_path_str.strip()
                validated_save_path = validate_path_input(
                    save_path_str, check_exists=False, console=None
                )
                if validated_save_path:
                    try:
                        abs_path = Path(save_path_str).resolve()
                        final_actions["save_path"] = str(abs_path)
                        console.print(
                            f"[info]Will save to: {escape(str(abs_path))}[/info]"
                        )
                    except Exception as e:
                        final_actions["save_path"] = str(
                            validated_save_path
                        )  # Fallback
                        console.print(
                            f"[info]Will save to (relative): {escape(str(validated_save_path))}[/info]"
                        )
                        logger.warning(
                            f"Could not resolve save path {validated_save_path}: {e}"
                        )
                else:
                    console.print(
                        f"[error]Invalid save path format: [yellow]{escape(save_path_str)}[/yellow]. Will print to stdout.[/error]"
                    )
                    final_actions["save_path"] = None
            else:  # User pressed Enter with no input
                final_actions["save_path"] = None
                console.print("[info]Will print to stdout.[/info]")
            console.print()  # Add space after save path interaction

        else:  # Path provided via CLI arg
            console.print(
                f"Will save to disk (from --save-on-disk): [green]{escape(str(cli_args.save_on_disk))}[/green]"
            )
            # Add space after CLI message
            console.print()

        # Copy to Clipboard - No longer asked, default is True
        if final_actions.get("copy_flag"):
            console.print("[info]Will copy prompt to clipboard.[/info]")
            console.print()  # Add space after copy message

        # --- Generate Equivalent Command --- (No changes needed)
        command_parts = ["promptbuilder"]

        def add_arg(flag: str, value: Optional[Any]):
            if value:
                command_parts.append(flag)
                command_parts.append(shlex.quote(str(value)))

        arg_map = {
            "task": "--task",
            "meta_instructions_src": "--meta-instructions",
            "input_desc_src": "--input",
            "input_instr_src": "--input-instructions",
            "output_desc_src": "--output",
            "output_instr_src": "--output-instructions",
            "persona_src": "--persona",
            "constraints_src": "--constraints",
            "tone_src": "--tone",
            "negative_constraints_src": "--negative-constraints",
            "example_input_src": "--example-input",
            "example_output_src": "--example-output",
        }
        for key, flag in arg_map.items():
            add_arg(flag, collected_data.get(key))
        context_paths_final = collected_data.get("context_paths")
        if context_paths_final and isinstance(context_paths_final, list):
            command_parts.append("--context")
            for path in context_paths_final:
                command_parts.append(shlex.quote(path))
        if final_actions.get("save_path"):
            add_arg("--save-on-disk", final_actions["save_path"])
        if final_actions.get("copy_flag"):
            command_parts.append("--copy")
        if cli_args.template:
            add_arg("--template", cli_args.template)
        if cli_args.config:
            add_arg("--config", cli_args.config)
        if cli_args.verbose > 0:
            command_parts.append(f"-{'v' * cli_args.verbose}")
        equivalent_command = " ".join(command_parts)
        console.print(Rule("[bold blue]Equivalent Command[/bold blue]"))
        console.print()
        console.print(
            "You can use this command to reproduce the same meta-prompt without interactive mode:"
        )
        console.print(
            Syntax(
                equivalent_command,
                "bash",
                theme="default",
                line_numbers=False,
                word_wrap=True,
            )
        )
        console.print("")

        # Attach final actions determined above
        collected_data["save_path"] = final_actions.get("save_path")
        collected_data["copy_flag"] = final_actions.get("copy_flag")

        return collected_data

    except KeyboardInterrupt:
        # Catch Ctrl+C from any input function OR the standard input() calls
        console.print("\n[yellow]Interactive mode cancelled by user.[/yellow]")
        sys.exit(0)  # Exit gracefully
```

### FILE: `src/promptbuilder/templating.py`
```py
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Rich imports (only needed for direct printing, logger handles most)
# from rich.console import Console

from jinja2 import Environment, FileSystemLoader, TemplateNotFound, select_autoescape

from .config import Config

# Use logger configured in cli.py
logger = logging.getLogger(__name__)

def render_meta_prompt(
    template_path: Path,
    data: Dict[str, Any],
    config: Config,
    console: 'Console' # Type hint for console
) -> Optional[str]:
    """Renders the meta prompt using Jinja2."""
    try:
        # Ensure template_path is absolute or relative to CWD if not found directly
        if not template_path.is_absolute():
            # Try relative to CWD first
            lookup_path_cwd = Path.cwd() / template_path
            # Try relative to config file location? (More complex)
            # Try relative to default template dir? (Maybe confusing)
            if lookup_path_cwd.is_file():
                 template_path = lookup_path_cwd
            # If still not found, FileSystemLoader might find it if it's relative to *its* search path (template_dir)

        if not template_path.is_file():
             # Use logger for error, RichHandler will format it
             logger.error(f"Template file not found: [red]{template_path}[/red]")
             # Maybe try the default template as a fallback?
             default_template = config.default_meta_prompt_template_path
             if default_template.is_file() and template_path != default_template:
                 logger.warning(f"Falling back to default template: [blue]{default_template}[/blue]")
                 template_path = default_template
             else:
                 logger.error("Default template also not found or is the same as the missing one. Cannot render.")
                 return None # Exit if no template is usable


        logger.info(f"Using template file: [blue]{template_path.resolve()}[/blue]")
        template_dir = template_path.parent
        template_filename = template_path.name

        env = Environment(
            loader=FileSystemLoader(template_dir, followlinks=True), # Allow symlinks if needed
            autoescape=select_autoescape(['html', 'xml']), # Autoescape common web formats if template generates them
            trim_blocks=True,
            lstrip_blocks=True,
            enable_async=False # Ensure Jinja2 runs synchronously
        )

        # Add placeholder function directly to the template context
        data['placeholder'] = lambda name: config.placeholder_format % name.upper()
        # Add config object directly to context
        data['config'] = config

        template = env.get_template(template_filename)
        rendered_prompt = template.render(data)
        logger.debug("Template rendering successful.")
        return rendered_prompt.strip() # Strip leading/trailing whitespace from final render

    except TemplateNotFound:
        logger.error(f"Template [red]{template_filename}[/red] not found in directory [blue]{template_dir}[/blue]")
        return None
    except Exception as e:
        # Log the error with traceback using RichHandler
        logger.error(f"Error rendering template [red]{template_path}[/red]: {e}", exc_info=True)
        return None
```

### FILE: `src/promptbuilder/tmpp.py`
```py
# src/promptbuilder/interactive.py

import logging
import shlex
import os  # Needed for os.path.sep
import sys  # For sys.exit
from pathlib import Path
from typing import Dict, Any, Optional, List

# Rich imports (Only for OUTPUT formatting now)
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text
from rich.syntax import Syntax
from rich.markup import escape  # To safely display user input

from .config import Config

# Import ALL input functions from utils now AND path_completer
from .utils import (
    get_single_line_input,
    get_multiline_input,
    get_yesno_confirmation,
    validate_path_input,
    path_completer,  # Still needed for context paths
)

# Use the logger configured in cli.py
logger = logging.getLogger(__name__)

# --- MODIFIED Multi-line prompt guide ---
MULTILINE_PROMPT_GUIDE = Text.from_markup(
    "\n[dim]Enter text below. Press [bold]Esc[/bold] then [bold]Enter[/bold] to finish.[/dim]"
    "\n[dim](Allows multi-line editing with arrow keys, Home/End, etc.)[/dim]"
)


def run_interactive_mode(
    cli_args: Any, config: Config, console: Console
) -> Optional[Dict[str, Any]]:
    """Runs the interactive prompting session using ONLY prompt_toolkit for input."""
    collected_data: Dict[str, Any] = {}
    # Initialize actions based on CLI args and config defaults
    final_actions = {
        "save_path": cli_args.save_on_disk,
        "copy_flag": True,  # Default to True for interactive mode
    }

    console.print(Rule("[bold cyan]PromptBuilder Interactive Mode[/bold cyan]"))
    console.print(
        Panel(  # Rich Panel for output
            Text.from_markup(
                "This interactive mode will guide you through providing the details needed to generate a [bold]META_PROMPT[/bold].\n"
                "The META_PROMPT contains instructions for a Large Language Model (LLM) to create a final, task-specific prompt for you.\n\n"
                "[yellow]Tip:[/yellow] You can provide file paths for many fields. If the path exists, its content will be read.\n"
                "[yellow]Tip:[/yellow] Press [bold]Ctrl+C[/bold] at any prompt to cancel and exit."
            ),
            title="Welcome!",
            border_style="blue",
            expand=False,
        )
    )
    console.print(
        "[dim](Leave optional fields blank and press Enter to skip)[/dim]"
    )

    # --- Main Interactive Loop ---
    try:  # Wrap the main input gathering in try...except KeyboardInterrupt
        # 1. Task (Required)
        console.print(Rule("Core Task"))
        if cli_args.task:
            console.print(
                f"Using Task from command line: [green]'{escape(cli_args.task)}'[/green]"
            )
            collected_data["task"] = cli_args.task
        else:
            while "task" not in collected_data or not collected_data["task"]:
                task = get_single_line_input(
                    console, "Enter the ultimate task description (Required): "
                )
                if task:
                    collected_data["task"] = task
                else:
                    console.print(
                        "[prompt.invalid]Task description cannot be empty."
                    )

        # 2. Context (Optional, Multiple) - Use path_completer
        console.print(Rule("Context Files/Folders"))
        if cli_args.context:
            console.print(
                f"Using Context paths from command line: [green]{', '.join(escape(p) for p in cli_args.context)}[/green]"
            )
            collected_data["context_paths"] = cli_args.context
        else:
            context_paths = []
            console.print(
                "[dim]Enter paths to files or folders for context. Dirs searched recursively.[/dim]"
            )
            console.print(
                f"[dim]Supported extensions: {', '.join(config.context_supported_extensions)}[/dim]"
            )
            console.print(
                "[dim]Enter a blank line when finished. Press TAB to autocomplete paths.[/dim]"
            )
            while True:
                # *** USE path_completer HERE ***
                path_str = get_single_line_input(
                    console, "Add context path: ", completer=path_completer
                )
                if not path_str:
                    break  # Finished
                validated_path = validate_path_input(
                    path_str, check_exists=True, console=None
                )
                if validated_path:
                    if validated_path.exists():
                        context_paths.append(str(validated_path))
                        console.print(
                            f"[info]Added: {escape(str(validated_path))}[/info]"
                        )
                    else:
                        console.print(
                            f"[warning]Path does not exist or is not accessible: [yellow]{escape(str(validated_path))}[/yellow][/warning]"
                        )
                else:
                    console.print(
                        f"[error]Invalid path format: [yellow]{escape(path_str)}[/yellow][/error]"
                    )

            if context_paths:
                collected_data["context_paths"] = context_paths
                console.print(f"Collected {len(context_paths)} context path(s).")
            else:
                console.print("No context paths provided.")
                collected_data["context_paths"] = None

        # Define fields to iterate through
        fields_to_ask = [
            (
                "meta_instructions_src",
                "Meta Instructions",
                "Guidance for the prompt generator (how to build the final prompt).",
                "> ",
                True,
                None,
            ),
            (
                "input_desc_src",
                "Input Description",
                "What the final prompt expects as input.",
                "> ",
                True,
                None,
            ),
            (
                "input_instr_src",
                "Input Instructions",
                "How the end-user should provide input to the final prompt.",
                "> ",
                True,
                "input_desc_src",
            ),
            (
                "output_desc_src",
                "Output Description",
                "What the final prompt should produce as output.",
                "> ",
                True,
                None,
            ),
            (
                "output_instr_src",
                "Output Instructions",
                "How the LLM should format the output of the final prompt.",
                "> ",
                True,
                "output_desc_src",
            ),
            (
                "persona_src",
                "Persona",
                "Specify the persona the final LLM should adopt (e.g., 'Expert Python programmer').",
                "Persona: ", # Use descriptive prompt for single line
                False,
                None,
            ),
            (
                "constraints_src",
                "Constraints",
                "General constraints the final LLM must adhere to (e.g., 'Answer in under 100 words').",
                "> ",
                True,
                None,
            ),
            (
                "tone_src",
                "Tone",
                "Specify the desired tone for the final LLM's output (e.g., 'Formal', 'Casual').",
                "Tone: ", # Use descriptive prompt for single line
                False,
                None,
            ),
            (
                "negative_constraints_src",
                "Negative Constraints",
                "Specify what the final LLM should NOT do (e.g., 'Do not mention pricing').",
                "> ",
                True,
                None,
            ),
            (
                "example_input_src",
                "Example Input",
                "An example of valid input for the final prompt.",
                "> ",
                True,
                None,
            ),
            (
                "example_output_src",
                "Example Output",
                "An example of desired output from the final prompt.",
                "> ",
                True,
                None,
            ),
        ]

        # Iterate through optional fields
        for (
            key,
            rule_title,
            description_dim,
            input_prompt,
            is_multiline,
            depends_on_key,
        ) in fields_to_ask:
            dependency_key_base = (
                depends_on_key.replace("_src", "") if depends_on_key else None
            )
            if depends_on_key and not (
                collected_data.get(depends_on_key)
                or getattr(cli_args, dependency_key_base, None)
            ):
                logger.debug(
                    f"Skipping '{rule_title}' because dependency '{depends_on_key}' is not met."
                )
                collected_data[key] = None
                continue

            console.print(Rule(rule_title))
            cli_arg_name = key.replace("_src", "")
            cli_value = getattr(cli_args, cli_arg_name, None)

            if cli_value:
                console.print(
                    f"Using value from command line: [green]'{escape(str(cli_value))}'[/green]"
                )
                collected_data[key] = cli_value
            else:
                console.print(
                    f"[dim]{description_dim} (Optional, leave blank to skip)[/dim]"
                )

                if is_multiline:
                    console.print(MULTILINE_PROMPT_GUIDE) # Shows simplified instruction now
                    user_input = get_multiline_input(console, input_prompt)
                else:
                    # No completer needed for these general single-line fields
                    user_input = get_single_line_input(console, input_prompt)

                if user_input:
                    collected_data[key] = user_input.strip()
                else:
                    collected_data[key] = None

        # --- Confirmation ---
        console.print(Rule("Summary"))

        # Helper function (no changes needed)
        def format_summary_value(
            key: str, data: dict, max_len=100
        ) -> Text:
            value = data.get(key)
            if key == "context_paths":
                if value and isinstance(value, list):
                    paths_str = ", ".join(f"'{escape(p)}'" for p in value)
                    if len(paths_str) > max_len:
                        paths_str = paths_str[: max_len - 3] + "..."
                    return Text(
                        f"{len(value)} path(s): {paths_str}", style="green"
                    )
                else:
                    return Text("None", style="dim")
            elif isinstance(value, str) and value:
                escaped_value = escape(value)
                display_value = escaped_value.replace("\n", "\\n")
                if len(display_value) > max_len:
                    display_value = display_value[: max_len - 3] + "..."
                return Text(f"'{display_value}'", style="green")
            elif value:
                return Text(f"{escape(str(value))}", style="green")
            else:
                return Text("None", style="dim")

        # Build the summary content (no changes needed)
        summary_content = Text()
        key_display_map = {
            "task": "Task",
            "context_paths": "Context Paths",
            "meta_instructions_src": "Meta Instructions",
            "input_desc_src": "Input Description",
            "input_instr_src": "Input Instructions",
            "output_desc_src": "Output Description",
            "output_instr_src": "Output Instructions",
            "persona_src": "Persona",
            "constraints_src": "Constraints",
            "tone_src": "Tone",
            "negative_constraints_src": "Negative Constraints",
            "example_input_src": "Example Input",
            "example_output_src": "Example Output",
        }
        num_items = len(key_display_map)
        for i, (key, display_name) in enumerate(key_display_map.items()):
            value_text = format_summary_value(key, collected_data)
            summary_content.append(f"{display_name}: ", style="bold")
            summary_content.append(value_text)
            if i < num_items - 1:
                summary_content.append("\n")

        console.print(
            Panel(
                summary_content,
                title="Collected Information",
                border_style="blue",
                expand=False,
            )
        )

        # --- Proceed Prompt (using standard input) ---
        console.print(
            # Use Markup directly here for the prompt text
            "\n[white]Press [bold]ENTER[/bold] to generate the prompt, or [bold]Ctrl+C[/bold] to cancel.[/white]"
        )
        # *** USE STANDARD input() FOR FINAL CONFIRMATION ***
        input()
        # Ctrl+C during input() will raise KeyboardInterrupt, caught below

        # --- Final Actions ---
        console.print(Rule("Final Actions"))
        # Save to disk
        if not cli_args.save_on_disk:
            # *** USE STANDARD input() FOR SAVE PATH ***
            console.print(
                "Save prompt to disk? (Enter path or leave blank for stdout): ",
                end="", # Prevent extra newline before input()
            )
            # Use standard input() - loses path completion but guarantees Enter works
            save_path_str = input()

            if save_path_str:  # Check if user entered anything
                # Strip whitespace just in case
                save_path_str = save_path_str.strip()
                # Validate the path obtained from input()
                validated_save_path = validate_path_input(
                    save_path_str, check_exists=False, console=None
                )
                if validated_save_path:
                    try:
                        abs_path = Path(save_path_str).resolve()
                        final_actions["save_path"] = str(abs_path)
                        console.print(
                            f"[info]Will save to: {escape(str(abs_path))}[/info]"
                        )
                    except Exception as e:
                        final_actions["save_path"] = str(
                            validated_save_path
                        )  # Fallback
                        console.print(
                            f"[info]Will save to (relative): {escape(str(validated_save_path))}[/info]"
                        )
                        logger.warning(
                            f"Could not resolve save path {validated_save_path}: {e}"
                        )
                else:
                    console.print(
                        f"[error]Invalid save path format: [yellow]{escape(save_path_str)}[/yellow]. Will print to stdout.[/error]"
                    )
                    final_actions["save_path"] = None
            else:  # User pressed Enter with no input
                final_actions["save_path"] = None
                console.print("[info]Will print to stdout.[/info]")

        else:  # Path provided via CLI arg
            console.print(
                f"Will save to disk (from --save-on-disk): [green]{escape(str(cli_args.save_on_disk))}[/green]"
            )
            final_actions["save_path"] = cli_args.save_on_disk

        # Copy to Clipboard - No longer asked, default is True
        if final_actions.get("copy_flag"):
            console.print("[info]Will copy prompt to clipboard.[/info]")

        # --- Generate Equivalent Command --- (No changes needed)
        command_parts = ["promptbuilder"]
        def add_arg(flag: str, value: Optional[Any]):
            if value: command_parts.append(flag); command_parts.append(shlex.quote(str(value)))
        arg_map = { "task": "--task", "meta_instructions_src": "--meta-instructions", "input_desc_src": "--input", "input_instr_src": "--input-instructions", "output_desc_src": "--output", "output_instr_src": "--output-instructions", "persona_src": "--persona", "constraints_src": "--constraints", "tone_src": "--tone", "negative_constraints_src": "--negative-constraints", "example_input_src": "--example-input", "example_output_src": "--example-output", }
        for key, flag in arg_map.items(): add_arg(flag, collected_data.get(key))
        context_paths_final = collected_data.get("context_paths")
        if context_paths_final and isinstance(context_paths_final, list):
            command_parts.append("--context")
            for path in context_paths_final: command_parts.append(shlex.quote(path))
        if final_actions.get("save_path"): add_arg("--save-on-disk", final_actions["save_path"])
        if final_actions.get("copy_flag"): command_parts.append("--copy")
        if cli_args.template: add_arg("--template", cli_args.template)
        if cli_args.config: add_arg("--config", cli_args.config)
        if cli_args.verbose > 0: command_parts.append(f"-{'v' * cli_args.verbose}")
        equivalent_command = " ".join(command_parts)
        console.print(Rule("[bold blue]Equivalent Command[/bold blue]"))
        console.print("You can use this command to reproduce the same meta-prompt without interactive mode:")
        console.print( Syntax( equivalent_command, "bash", theme="default", line_numbers=False, word_wrap=True, ) )
        console.print("")

        # Attach final actions determined above
        collected_data["save_path"] = final_actions.get("save_path")
        collected_data["copy_flag"] = final_actions.get("copy_flag")

        return collected_data

    except KeyboardInterrupt:
        # Catch Ctrl+C from any input function OR the standard input() calls
        console.print("\n[yellow]Interactive mode cancelled by user.[/yellow]")
        sys.exit(0) # Exit gracefully
```

### FILE: `src/promptbuilder/utils.py`
```py
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
```

## FOLDER: `src/promptbuilder/templates`

```text

```

### FILE: `src/promptbuilder/templates/default_meta_prompt.j2`
```
{# ============================================================ #}
{#               META-PROMPT FOR LLM PROMPT GENERATION          #}
{#               (Using Jinja Template Structure)               #}
{# ============================================================ #}

{# This top section provides meta-instructions for the system RENDERING this template. #}
{# It does NOT become part of the final generated prompt string. #}
**Objective:** Generate a high-quality TASK_PERFORMING_PROMPT based on the specifications below. This prompt will be used by a human user or another system to instruct an LLM to perform a specific task.

**Your Role (As Renderer):** You are rendering this Jinja template to produce a ready-to-use Task-Performing Prompt for an LLM.

**Core Task for the Final LLM (Defined by User):**
The ultimate task the final LLM needs to perform is:
{{ task_description }}

{# Optional Meta-Instructions for the Renderer (How to process this template): #}
{% if meta_instructions %}
**Meta-Instructions for Template Rendering:**
{{ meta_instructions }}
{% endif %}

{# ========================================================================== #}
{# START OF THE ACTUAL TASK-PERFORMING PROMPT TO BE GENERATED               #}
{# ========================================================================== #}
{# This section defines the text that WILL BE GENERATED as the final prompt. #}

{% if persona %}
## Assigned Role
You are to adopt the following persona for this task: {{ persona }}
{% else %}
## Assigned Role
You are an expert AI assistant.
{% endif %}

## Core Task & Context
Your primary task is: {{ task_description }}

{% if context_items %}
You MUST perform this task by drawing upon the principles, terminology, style, and information contained within the following provided context. Analyze and utilize this context carefully.

**Provided Context:**
{# Loop through each context item (path, content) #}
{% for path, content in context_items %}
--- START CONTEXT FILE: {{ path }} ---
{% if content is not none %}
{{ content }}
{% else %}
[File Content Could Not Be Read or File Was Empty]
{% endif %}
--- END CONTEXT FILE: {{ path }} ---
{% endfor %}
{# Add note about skipped files if any #}
{% if context_files_skipped > 0 %}
**(Note: {{ context_files_skipped }} context file(s) were skipped due to unsupported extensions, size limits exceeding {{ config.context_max_file_size_mb }} MB, or read errors. Their content is NOT included above.)**
{% endif %}

{% else %}
Perform this task based on your general knowledge, adhering to the specified output requirements and constraints.
{% endif %}

## Input Specification
{% if input_description %}
The end-user will provide input matching the following description:
{{ input_description }}

The user's input will be provided below, marked by the `{{ placeholder('INPUT') }}` placeholder.
{% if input_instructions %}

Instructions for the User's Input:
{{ input_instructions }}
{% endif %}

**User Input:**
```
{{ placeholder('INPUT') }}
```
{% else %}
The end-user will provide their query or data directly. Process the input provided below:
```
{{ placeholder('INPUT') }}
```
{% endif %}

## Output Specification
{% if output_description or output_instructions %}
You must generate an output that adheres *exactly* to the following specifications:

{% if output_description %}
**Output Description:**
{{ output_description }}
{% endif %}

{% if output_instructions %}
**Formatting and Structure Requirements:**
{{ output_instructions }}
{% endif %}
{% else %}
Generate a clear and concise response addressing the user's input and the core task.
{% endif %}

## Constraints & Guidelines
Adhere strictly to the following constraints and guidelines:
{% if constraints %}
*   **General Constraints:** {{ constraints }}
{% endif %}
{% if tone %}
*   **Tone:** Maintain a {{ tone }} tone.
{% endif %}
{% if negative_constraints %}
*   **What NOT to Do (Negative Constraints):** {{ negative_constraints }}
{% endif %}
*   Focus solely on the provided input and context (if any) to generate the response. Do not add information not present in the source materials unless explicitly asked to.
*   Be precise and follow all formatting instructions meticulously.

## Examples (Optional)
{% if example_input or example_output %}
Refer to these examples for guidance on the expected input/output format and quality:

{% if example_input %}
**Good Example Input:**
```
{{ example_input }}
```
{% endif %}

{% if example_output %}
**Good Example Output:**
```
{{ example_output }}
```
{% endif %}
{% endif %}

{# ========================================================================== #}
{# END OF THE ACTUAL TASK-PERFORMING PROMPT TO BE GENERATED                 #}
{# ========================================================================== #}

{# Final meta-instruction to the rendering system #}
Now, generate the complete TASK_PERFORMING_PROMPT based on the structure and content defined above.
```
