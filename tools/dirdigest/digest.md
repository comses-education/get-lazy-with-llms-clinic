## FOLDER: `.`

```text

```

### FILE: `LICENSE`
```
MIT License

Copyright (c) [YEAR] [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### FILE: `promptbuilderdigest.md`
```md
## FOLDER: `.`

```text

```

### FILE: `README.md`
```md
# Promptbuilder CLI Tool

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
*   **Context Aware:** Include content from local files and directories (recursively) as context.
*   **Structured Input/Output:** Define expected inputs, outputs, and formatting instructions.
*   **Prompt Characteristics:** Specify persona, tone, constraints, and negative constraints for the final prompt.
*   **Examples:** Provide input/output examples to guide the final prompt generation.
*   **Customizable Templates:** Use the default meta-prompt template or provide your own Jinja2 template.
*   **Configurable:** Set defaults via a `.promptbuilder.yaml` configuration file.
*   **Output Options:** Print to console, save to file, copy to clipboard.

## Example Call
```bash
promptbuilder \
             --task "create high quality scientific evaluation reports of agent-based models based on their documentation and code" \
             --context ./test_docs/abm_odd_evaluator/ \
             --input "model code and documentation" \
             --input-instructions "by using a tool like diringest or gitingest to create a digest of the whole model's code into a single markdown file" \
             --output "High quality evaluation report based on criteria and structure from the CONTEXT" \
             --output-instructions "return the evaluation report in markdown format" \
             --persona "an expert in agent-based modeling and social simulation, drawing on the principles and best practices outlined in Understanding Complex Systems — Bruce Edmonds & Ruth Meyer (eds.), Simulating Social Complexity: A Handbook." \
             --tone "Factual" \
             --save-on-disk ./generated_prompts/abm_odd_evaluator_prompt_2.md
```

## Installation

**Prerequisites:**

*   Python (3.8+ recommended)
*   [Poetry](https://python-poetry.org/docs/#installation) (for package management)

**Steps:**

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

2.  **Install dependencies and the tool:**
    Poetry will create a virtual environment and install the necessary packages defined in `pyproject.toml`.
    ```bash
    poetry install
    ```

3.  **Activate the virtual environment:**
    To use the `promptbuilder` command directly, activate the Poetry shell:
    ```bash
    # Typically 'poetry shell', but use 'poetry env activate' if needed for your setup
    poetry shell
    # or
    # poetry env activate
    ```
    (Alternatively, you can run commands via `poetry run promptbuilder [OPTIONS]`)

4.  **Verify installation:**
    ```bash
    promptbuilder --help
    ```

## Usage Examples

**(Ensure you are in the activated Poetry shell or use `poetry run promptbuilder ...`)**

**1. Basic Task (Minimum Required for CLI):**
Generate a meta-prompt for creating a task prompt that summarizes text.

```bash
promptbuilder --task "Summarize the provided text into three key bullet points."
```
*(Output: The generated META_PROMPT will be printed to the console.)*

**2. Adding Context from Files/Folders:**
Include the content of specific files or all supported files within a directory as context.

```bash
# Context from a specific file
promptbuilder --task "Explain the main function in this Python code." \
              --context ./src/main.py

# Context from all supported files (.txt, .md, .py, etc.) in a directory and subdirectories
promptbuilder --task "Summarize the key topics covered in these project documents." \
              --context ./project_docs/
```
*(Output: META_PROMPT printed, instructing the LLM to consider the content of the specified files/folders.)*

**3. Specifying Input and Output:**
Define what the final `TASK_PERFORMING_PROMPT` should expect as input and produce as output.

```bash
promptbuilder --task "Translate the user's input text from English to French." \
              --input "A single paragraph of English text." \
              --output "The French translation of the input paragraph." \
              --output-instructions "Provide only the French translation, no extra commentary."
```
*(Output: META_PROMPT printed, instructing the LLM to create a TASK_PERFORMING_PROMPT that includes placeholders/sections and format instructions.)*

**4. Defining Prompt Characteristics:**
Specify the persona, constraints, tone, and negative constraints for the final prompt generated by the LLM.

```bash
promptbuilder --task "Rewrite the provided paragraph to be suitable for a 5th-grade reading level." \
              --context ./complex_paragraph.txt \
              --persona "An experienced elementary school teacher explaining a concept." \
              --tone "Simple, encouraging, and clear." \
              --constraints "Use short sentences. Define any technical terms simply." \
              --negative-constraints "Do not use analogies involving pop culture. Avoid overly complex vocabulary."
```
*(Output: META_PROMPT printed, instructing the LLM to generate a final prompt incorporating these specific characteristics.)*

**5. Using Files for Long Instructions or Examples:**
Provide detailed instructions or examples from files instead of directly on the command line.

```bash
# Create instruction files first (e.g., meta_guide.txt, tone_guide.txt, example_in.txt, example_out.txt)
# meta_guide.txt: "Generate a prompt suitable for a novice user. Ensure the tone is helpful and encouraging."
# tone_guide.txt: "Professional but friendly, avoiding overly technical jargon unless defined."
# example_in.txt: "def hello():\n  print('world')"
# example_out.txt: "function hello() {\n  console.log('world');\n}"

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
*(Output: META_PROMPT saved to the specified file AND copied to the clipboard.)*

**7. Interactive Mode:**
Let `promptbuilder` guide you through gathering the necessary information.

```bash
promptbuilder --interactive
```
*(Output: Follow the prompts to enter task description, context paths, instructions, persona, constraints, etc.)*

You can also combine interactive mode with pre-filled arguments:
```bash
promptbuilder -i --task "Debug Python code snippet" --context ./my_buggy_code.py
```
*(Output: Interactive mode starts, skipping prompts for `--task` and `--context` as they were provided.)*

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
  -v, --verbose         Increase output verbosity (-v for INFO, -vv for DEBUG).
```

## Configuration (`.promptbuilder.yaml`)

You can customize default behavior by creating a configuration file named `.promptbuilder.yaml` in either:

1.  The current working directory (`./.promptbuilder.yaml`)
2.  The user's config directory (`~/.config/promptbuilder/.promptbuilder.yaml`)

The file in the current directory takes precedence. Use the `--config PATH` argument to specify an explicit location.

**Example `.promptbuilder.yaml`:**

```yaml
# Default path to the Jinja2 template for the meta-prompt
# default_meta_prompt_template_path: /path/to/your/custom/template.j2

# Format string for placeholders like {{INPUT}}, {{OUTPUT}} in the *final* prompt
# The meta-prompt will instruct the LLM to use this format.
placeholder_format: "__%s__" # Default is "{{%s}}"

# Maximum size (in MB) for individual context files to be included.
context_max_file_size_mb: 10.0 # Default is 5.0

# List of file extensions to include when parsing context directories recursively.
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

# If true, automatically copy generated prompts to clipboard unless --no-copy (not implemented) is used.
copy_to_clipboard_default: true # Default is false

# Default directory to save prompts if --save-on-disk is used with just a filename.
output_dir: ./generated_prompts # Default is "." (current directory)

# Marker used in interactive mode to signal the end of multi-line text input.
interactive_multiline_end_marker: EOD # Default is "END"
```

## Template Customization

The structure and wording of the generated META_PROMPT are controlled by a [Jinja2](https://jinja.palletsprojects.com/) template.

*   **Default Template:** Located within the installed package at `promptbuilder/templates/default_meta_prompt.j2`.
*   **Custom Template:** Use the `--template PATH/TO/YOUR/template.j2` argument to specify your own template file.

Your custom template can access the data collected from command-line arguments or interactive mode. Key variables available in the template context include:

*   `task_description`: The core task string.
*   `meta_instructions`: String content from `--meta-instructions`.
*   `input_description`, `output_description`, `input_instructions`, `output_instructions`: Strings from corresponding arguments.
*   `persona`, `constraints`, `tone`, `negative_constraints`: Strings from corresponding arguments (or `None` if not provided).
*   `example_input`, `example_output`: Strings from corresponding arguments.
*   `context_items`: A list of tuples `(path_string, content_string)` for each included context file.
*   `context_files_skipped`: Integer count of files skipped due to limits/errors.
*   `config`: The loaded Config object (e.g., `config.context_max_file_size_mb`).
*   `placeholder(name)`: A function that returns the placeholder string using the configured format (e.g., `placeholder('INPUT')` might return `{{INPUT}}` or `__INPUT__`).
*   `verbose_level`: Integer from `-v` flags.

## Future Considerations (Optional Enhancements)

*   **Cosmetics:** Use rich for better UX
*   **Interactive Mode:** Use `Ctrl+Enter` instead of `END` to jump to the next prompt.
*   **Advanced Context Modes:** Summarization of context files before inclusion.
*   **Direct LLM Interaction:** Option to directly send the generated META_PROMPT to a configured LLM API and display/save the resulting TASK_PERFORMING_PROMPT.
*   **Prompt Library:** Functionality to save/load/manage generated META_PROMPTs and TASK_PERFORMING_PROMPTs.

## Contributing

(Optional: Add guidelines for contributing if you plan for others to contribute.)
Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

(Optional: Specify the license, e.g., MIT License. Make sure you have a corresponding LICENSE file.)
This project is licensed under the MIT License - see the LICENSE file for details.
```

### FILE: `pyproject.toml`
```toml
[project]
name = "promptbuilder"
version = "0.1.0"
description = "A tool to generate meta-prompts for instructing LLMs to create task-performing prompts."
authors = [
  { name = "Your Name", email = "you@example.com" }
]
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
  "pyyaml>=6.0",
  "jinja2>=3.1",
  "pyperclip>=1.8"
]

[project.scripts]
promptbuilder = "src.cli:main"

[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"
```

## FOLDER: `src`

```text

```

### FILE: `src/__init__.py`
```py
# Optional: Define package-level items or leave empty
# You could set up root logger here if desired, but basicConfig in cli.py is fine too.
import logging

# Configure the root logger for the package
# logging.getLogger(__name__).addHandler(logging.NullHandler())
```

### FILE: `src/__main__.py`
```py
# This allows running the package using 'python -m promptbuilder'
import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())
```

### FILE: `src/cli.py`
```py
# promptbuilder/cli.py
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

    setup_logging(args.verbose)

    # Load configuration
    config = cfg.Config.load(args.config)
    if args.verbose > 0:
        logger.info(f"Loaded configuration: {config}")


    collected_data: Optional[Dict[str, Any]] = None
    final_actions = {
        'save_path': args.save_on_disk,
        'copy_flag': args.copy or (config.copy_to_clipboard_default and not args.copy),
    }

    if args.interactive:
        logger.info("Starting interactive mode...")
        interactive_results = interactive.run_interactive_mode(args, config)
        if interactive_results is None:
            sys.exit(0) # User cancelled
        collected_data = interactive_results
        final_actions['save_path'] = collected_data.pop('save_path', None)
        final_actions['copy_flag'] = collected_data.pop('copy_flag', False)
    else:
        # CLI Mode
        if not args.task:
            parser.error("--task is required in non-interactive mode.")
            # sys.exit(1) # Unreachable due to parser.error

        logger.info("Running in CLI mode...")
        collected_data = {
            'task_description': args.task,
            'context_paths': args.context,
            'meta_instructions_src': args.meta_instructions,
            'input_desc_src': args.input,
            'input_instr_src': args.input_instructions,
            'output_desc_src': args.output,
            'output_instr_src': args.output_instructions,
            # Add sources for new args
            'persona_src': args.persona,
            'constraints_src': args.constraints,
            'tone_src': args.tone,
            'negative_constraints_src': args.negative_constraints,
            'example_input_src': args.example_input,
            'example_output_src': args.example_output,
        }
        # final_actions already set from args/config

    # --- Common Processing (Both Modes) ---

    # Resolve text/path arguments
    template_data: Dict[str, Any] = {
         'task_description': collected_data.get('task') or collected_data.get('task_description'),
         'meta_instructions': utils.read_text_or_path(collected_data.get('meta_instructions_src'), config.context_encoding, 'meta-instructions'),
         'input_description': utils.read_text_or_path(collected_data.get('input_desc_src'), config.context_encoding, 'input description'),
         'input_instructions': utils.read_text_or_path(collected_data.get('input_instr_src'), config.context_encoding, 'input instructions'),
         'output_description': utils.read_text_or_path(collected_data.get('output_desc_src'), config.context_encoding, 'output description'),
         'output_instructions': utils.read_text_or_path(collected_data.get('output_instr_src'), config.context_encoding, 'output instructions'),
         # Read new args
         'persona': utils.read_text_or_path(collected_data.get('persona_src'), config.context_encoding, 'persona'),
         'constraints': utils.read_text_or_path(collected_data.get('constraints_src'), config.context_encoding, 'constraints'),
         'tone': utils.read_text_or_path(collected_data.get('tone_src'), config.context_encoding, 'tone'),
         'negative_constraints': utils.read_text_or_path(collected_data.get('negative_constraints_src'), config.context_encoding, 'negative constraints'),
         'example_input': utils.read_text_or_path(collected_data.get('example_input_src'), config.context_encoding, 'example input'),
         'example_output': utils.read_text_or_path(collected_data.get('example_output_src'), config.context_encoding, 'example output'),
         'verbose_level': args.verbose,
         'config': config, # Pass config object to template
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

    # 3. Print to Stdout
    if not output_performed or (not save_target_str and not final_actions.get('copy_flag')):
         if output_performed: # Add a separator only if other actions *succeeded* but stdout is still needed
              print("\n--- Generated META_PROMPT ---")
         elif save_target_str or final_actions.get('copy_flag'): # Add separator if actions were *attempted* but maybe failed
              print("\n--- Generated META_PROMPT (stdout fallback) ---")

         print(meta_prompt)

    logger.info("PromptBuilder finished.")
    sys.exit(0)


if __name__ == '__main__':
    main()
```

### FILE: `src/config.py`
```py
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
    context_max_file_size_mb: float = 0.3
    context_supported_extensions: List[str] = field(default_factory=lambda: [".txt", ".md", ".py", ".json", ".yaml", ".xml", ".csv", ".html", ".css", ".js"])
    context_encoding: str = "utf-8"
    copy_to_clipboard_default: bool = True
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

### FILE: `src/context.py`
```py
# promptbuilder/context.py
import logging
import os  # <--- Import the os module
from pathlib import Path
from typing import List, Optional, Tuple, Set

from .config import Config

logger = logging.getLogger(__name__)

# ContextInfo still holds (path_string, content)
ContextInfo = Tuple[str, Optional[str]]

def parse_context_paths(
    paths: List[str],
    config: Config,
    verbose_level: int = 0
) -> Tuple[List[ContextInfo], int, int]:
    """
    Parses context paths (files/directories), applying configuration limits.
    Uses absolute paths for processing but returns relative paths for display.

    Returns:
        Tuple containing:
        - List of ContextInfo tuples: (relative_path_string, content_or_summary).
        - Total number of files processed internally.
        - Total number of files skipped.
    """
    context_items: List[ContextInfo] = []
    processed_files = 0
    skipped_files = 0
    max_bytes = int(config.context_max_file_size_mb * 1024 * 1024)
    supported_ext_set = set(config.context_supported_extensions)
    processed_paths: Set[Path] = set() # Keep track of canonical paths to avoid duplicates
    files_to_process: List[Path] = []
    cwd = Path.cwd() # <--- Get Current Working Directory once

    if not paths:
        return [], 0, 0

    # 1. Collect all potential files using absolute paths for reliability
    for path_str in paths:
        # Resolve input path relative to CWD if it's not absolute already
        input_path = Path(path_str)
        try:
            # Resolve symlinks and make absolute
            absolute_path = input_path.resolve(strict=True)
        except FileNotFoundError:
             logger.warning(f"Context path not found: {path_str}")
             skipped_files += 1
             continue
        except Exception as e:
             logger.error(f"Error resolving path {path_str}: {e}")
             skipped_files += 1
             continue


        if not absolute_path.exists(): # Should be redundant after resolve(strict=True) but safe check
            logger.warning(f"Context path resolved but does not exist: {absolute_path} (from {path_str})")
            skipped_files += 1
            continue

        if absolute_path in processed_paths:
             logger.debug(f"Skipping already processed path: {path_str} (resolved: {absolute_path})")
             continue

        if absolute_path.is_file():
            files_to_process.append(absolute_path)
            processed_paths.add(absolute_path)
        elif absolute_path.is_dir():
            logger.info(f"Recursively searching directory: {path_str} (resolved: {absolute_path})")
            try:
                for item in absolute_path.rglob('*'):
                    try:
                        item_resolved = item.resolve(strict=True) # Resolve items found during iteration
                        if item_resolved in processed_paths:
                            continue
                        if item.is_file(): # Check original item type before resolving
                            files_to_process.append(item_resolved)
                            processed_paths.add(item_resolved)
                        # else: ignore subdirectories explicitly found by rglob
                    except Exception as e:
                         logger.warning(f"Skipping item within directory {absolute_path} due to resolve error: {item} ({e})")
                         skipped_files += 1 # Count unresolvable items as skipped

            except OSError as e:
                 logger.error(f"Error scanning directory {absolute_path}: {e}")
                 skipped_files+=1 # Consider dir scan error as skipped potential files


    # 2. Process collected absolute file paths
    for file_path in files_to_process: # file_path is an absolute Path object
        processed_files += 1

        # --- Calculate relative path for display ---
        try:
            # Create path relative to the current working directory
            relative_display_path = os.path.relpath(file_path, cwd)
        except ValueError as e:
            # This might happen if paths are on different drives (Windows)
            logger.warning(f"Could not determine relative path for {file_path} relative to {cwd}: {e}. Using absolute path for display.")
            relative_display_path = str(file_path) # Fallback to absolute path string

        logger.debug(f"Processing context file: {file_path} (displaying as: {relative_display_path})")

        # Check extension (use absolute path's suffix)
        if file_path.suffix.lower() not in supported_ext_set:
            if verbose_level > 0:
                # Log with the path the user will see (relative)
                logger.info(f"Skipping file (unsupported extension {file_path.suffix}): {relative_display_path}")
            skipped_files += 1
            continue

        # Check size (use absolute path's stat)
        try:
            file_size = file_path.stat().st_size
            if file_size > max_bytes:
                logger.warning(f"Skipping file (size {file_size / (1024*1024):.2f} MB > limit {config.context_max_file_size_mb} MB): {relative_display_path}")
                skipped_files += 1
                continue
            if file_size == 0:
                 logger.info(f"Including empty file: {relative_display_path}")
                 # --- Store relative path in results ---
                 context_items.append((relative_display_path, ""))
                 continue

        except OSError as e:
            logger.error(f"Error accessing file metadata {relative_display_path}: {e}")
            skipped_files += 1
            continue

        # Read content (use absolute path's read_text)
        try:
            content = file_path.read_text(encoding=config.context_encoding)
            # --- Store relative path in results ---
            context_items.append((relative_display_path, content))
            if verbose_level > 1:
                 logger.debug(f"Successfully read content from: {relative_display_path}")
        except UnicodeDecodeError:
            logger.warning(f"Skipping file (encoding error with '{config.context_encoding}'): {relative_display_path}")
            skipped_files += 1
        except IOError as e:
            logger.error(f"Error reading file {relative_display_path}: {e}")
            skipped_files += 1

    # Calculate total attempted *after* initial collection and resolution attempts
    total_processed_after_collection = len(files_to_process)
    actual_included = len(context_items)

    if verbose_level > 0:
         # Report based on files actually attempted for reading after collection/filtering
         logger.info(f"Context processing summary: Attempted reads={total_processed_after_collection}, Included={actual_included}, Skipped (filter/read error)={skipped_files}")

    # Return list of (relative_path_str, content) tuples
    return context_items, total_processed_after_collection, skipped_files # Return count of files attempted reads
```

### FILE: `src/interactive.py`
```py
# promptbuilder/interactive.py
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

from .config import Config
from .utils import get_multiline_input, validate_path_input, read_text_or_path # Added read_text_or_path

logger = logging.getLogger(__name__)

def run_interactive_mode(cli_args: Any, config: Config) -> Optional[Dict[str, Any]]:
    """Runs the interactive prompting session."""
    collected_data: Dict[str, Any] = {}
    final_actions = {'save_path': None, 'copy_flag': False}

    print("--- PromptBuilder Interactive Mode ---")
    print("Please provide the following details to build the meta-prompt.")
    print("(Leave optional fields blank and press Enter to skip)")
    print(f"(For multi-line input, type '{config.interactive_multiline_end_marker}' on a new line to finish)")

    # 1. Task (Required)
    if cli_args.task:
        print(f"\nUsing Task from command line: {cli_args.task}")
        collected_data['task'] = cli_args.task
    else:
        while not collected_data.get('task'):
            task = input("\nEnter the ultimate task description (Required): ").strip()
            if task:
                collected_data['task'] = task
            else:
                print("Task description cannot be empty.")

    # 2. Context (Optional, Multiple)
    if cli_args.context:
        print(f"\nUsing Context paths from command line: {', '.join(cli_args.context)}")
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
            validated_path = validate_path_input(path_str, check_exists=True)
            if validated_path:
                 context_paths.append(str(validated_path)) # Store as string
        if context_paths:
             collected_data['context_paths'] = context_paths

    # 3. Meta Instructions (Optional)
    if cli_args.meta_instructions:
        print("\nUsing Meta Instructions from command line/file.")
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

    # --- Prompt Characteristics ---
    print("\n--- Final Prompt Characteristics ---")

    # 8. Persona (Optional)
    if cli_args.persona:
        print("\nUsing Persona from command line/file.")
        collected_data['persona_src'] = cli_args.persona
    else:
        persona_input = input("\n[Optional] Specify the Persona for the final LLM (e.g., 'Helpful Assistant'): ").strip()
        if persona_input:
             collected_data['persona_src'] = persona_input # Store text or path string

    # 9. Constraints (Optional)
    if cli_args.constraints:
        print("\nUsing Constraints from command line/file.")
        collected_data['constraints_src'] = cli_args.constraints
    else:
        constraints_input = get_multiline_input(
             "\n[Optional] Enter general Constraints for the final LLM:",
             config.interactive_multiline_end_marker
         ).strip()
        if constraints_input:
             collected_data['constraints_src'] = constraints_input

    # 10. Tone (Optional)
    if cli_args.tone:
        print("\nUsing Tone from command line/file.")
        collected_data['tone_src'] = cli_args.tone
    else:
        tone_input = input("\n[Optional] Specify the desired Tone (e.g., 'Formal', 'Casual'): ").strip()
        if tone_input:
             collected_data['tone_src'] = tone_input

    # 11. Negative Constraints (Optional)
    if cli_args.negative_constraints:
        print("\nUsing Negative Constraints from command line/file.")
        collected_data['negative_constraints_src'] = cli_args.negative_constraints
    else:
        neg_constraints_input = get_multiline_input(
             "\n[Optional] Enter things the final LLM should NOT do (Negative Constraints):",
             config.interactive_multiline_end_marker
         ).strip()
        if neg_constraints_input:
             collected_data['negative_constraints_src'] = neg_constraints_input


    # --- Examples ---
    print("\n--- Examples ---")
    # 12. Example Input (Optional)
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

    # 13. Example Output (Optional)
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
    # Display summary for new fields
    print(f"Persona Source: {'Provided' if collected_data.get('persona_src') else 'None'}")
    print(f"Constraints Source: {'Provided' if collected_data.get('constraints_src') else 'None'}")
    print(f"Tone Source: {'Provided' if collected_data.get('tone_src') else 'None'}")
    print(f"Negative Constraints Source: {'Provided' if collected_data.get('negative_constraints_src') else 'None'}")
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
        final_actions['save_path'] = save_path_str

    # Copy to clipboard
    copy_default_char = 'Y' if config.copy_to_clipboard_default else 'N'
    copy_prompt = f"Copy prompt to clipboard? [{copy_default_char}/{copy_default_char.lower()}]: " # Fixed prompt display
    copy_input_str = input(copy_prompt).strip().lower()

    # Logic for determining copy action in interactive mode
    should_copy = False
    if cli_args.copy: # CLI flag overrides interactive prompt
        should_copy = True
        print("Copying to clipboard (specified via --copy flag).")
    elif copy_input_str in ('y', 'yes'):
        should_copy = True
    elif copy_input_str == '' and config.copy_to_clipboard_default: # Enter defaults to config value
        should_copy = True
    # Otherwise (n, no, or other input when default is false), should_copy remains False

    final_actions['copy_flag'] = should_copy


    # Attach final actions to the collected data
    collected_data.update(final_actions)

    return collected_data
```

### FILE: `src/templating.py`
```py
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

### FILE: `src/utils.py`
```py
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
```

## FOLDER: `src/templates`

```text

```

### FILE: `src/templates/default_meta_prompt.j2`
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
```

### FILE: `pyproject.toml`
```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "dirdigest"
version = "0.1.0" # Or pull dynamically if preferred
authors = [
    { name = "Your Name", email = "your.email@example.com" },
]
description = "Generate Markdown or JSON digests of directory structures and file contents for LLM context."
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
    "click>=8.0",
    "rich>=13.0",
    "pathspec>=0.11",
    "pyperclip>=1.8",
    "tomli>=2.0.1; python_version < '3.11'",
]

[project.scripts]
# Point to the new combined function
dirdigest = "dirdigest.cli:cli_entry"

[tool.setuptools.packages.find]
where = ["src"]
```

## FOLDER: `src`

```text

```

## FOLDER: `src/dirdigest`

```text

```

### FILE: `src/dirdigest/__init__.py`
```py
"""dirdigest: Generate Markdown or JSON digests of directory contents."""

# Define the package version
# This is the single source of truth for the version.
__version__ = "0.1.0"
```

### FILE: `src/dirdigest/__main__.py`
```py
# src/dirdigest/__main__.py (Modified)
"""Allows running the CLI via `python -m dirdigest`."""

import sys
from .cli import cli_entry # Import the new combined function

if __name__ == "__main__":
    # Execute the main Click command/entry point
    # Pass prog_name if needed by Click for help messages, though often inferred
    sys.exit(cli_entry(prog_name="dirdigest"))
```

### FILE: `src/dirdigest/cli.py`
```py
# src/dirdigest/cli.py (Corrected Argument Parsing)

import logging
import sys
from pathlib import Path
from typing import Optional, Tuple, List # Added List

import click

# To use rich-click for help formatting, uncomment the next line
# import rich_click as click
# And replace @click.command(...) with @click.command(cls=click.RichGroup) # Use RichGroup if using rich-click
# Ensure rich-click is added to pyproject.toml dependencies

from . import __version__
from .config import DEFAULT_CONFIG, get_effective_config
from .core import generate_digest
from .utils import console, copy_to_clipboard, setup_logging, write_to_file

log = logging.getLogger(__name__)

# --- Helper function to split comma-separated args ---
def _split_comma_separated_args(args_tuple: Tuple[str, ...]) -> List[str]:
    """Splits strings within a tuple by commas and flattens the list."""
    final_list = []
    for item in args_tuple:
        # Split by comma, strip whitespace from each part, filter out empty strings
        split_items = [part.strip() for part in item.split(',') if part.strip()]
        final_list.extend(split_items)
    return final_list
# --- End Helper ---


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(__version__, '-V', '--version', package_name='dirdigest')
@click.argument(
    "directory",
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, readable=True, path_type=Path
    ),
    default=".",
)
@click.option(
    "-o", "--output",
    type=click.Path(file_okay=True, dir_okay=False, writable=True, path_type=Path),
    default=None,
    help="File path to write the digest to. Output is *also* copied to clipboard by default.",
)
@click.option(
    "--include",
    type=str,
    multiple=True,
    metavar="PATTERN",
    help="Glob pattern(s) to include. Separate multiple patterns with commas OR use the flag multiple times.", # Updated help
)
@click.option(
    "--exclude",
    type=str,
    multiple=True,
    metavar="PATTERN",
    help="Glob pattern(s) to exclude. Separate multiple patterns with commas OR use the flag multiple times.", # Updated help
)
@click.option(
    "--max-size",
    type=click.IntRange(min=0),
    default=None,
    metavar="KB",
    help=f"Max file size in KB to include content for. Default from config/default: {DEFAULT_CONFIG['max_size']} KB.",
)
@click.option(
    "--no-default-ignore",
    is_flag=True,
    default=False,
    help="Disable default exclusion patterns.",
)
@click.option(
    "-f", "--format",
    type=click.Choice(['markdown', 'json'], case_sensitive=False),
    default=None,
    help=f"Output format for the digest. Default from config/default: {DEFAULT_CONFIG['format']}.",
)
@click.option(
    "--clipboard/--no-clipboard",
    "clipboard_flag",
    is_flag=True,
    default=True, # Default to True (copy to clipboard)
    help="Copy output to clipboard (default) / Disable clipboard copy.",
)
@click.option(
    "-v", "--verbose",
    is_flag=True,
    default=None, # Let config merging handle the final boolean value
    help="Enable verbose (DEBUG level) logging output.",
)
def cli_entry(
    directory: Path,
    output: Optional[Path],
    include: Tuple[str, ...], # Original tuple from click
    exclude: Tuple[str, ...], # Original tuple from click
    max_size: Optional[int],
    no_default_ignore: bool,
    format: Optional[str],
    clipboard_flag: bool, # Will be True or False based on flag/default
    verbose: Optional[bool], # Will be True if -v used, None otherwise
):
    """
    dirdigest: Generate Markdown or JSON digests of directory contents.

    Recursively scans a directory, filters files based on patterns and size,
    reads text content, and outputs a consolidated digest suitable for LLMs.

    Default behavior copies the digest to the clipboard. Use --no-clipboard to disable.
    If -o is specified, writes to file *and* copies to clipboard (unless disabled).

    Example:

        dirdigest . --exclude '*.log,*.tmp' --include '*.py' # Use commas
        dirdigest . --exclude '*.log' --exclude '*.tmp'      # Use multiple flags
    """
    # *** Validation ***
    resolved_dir: Path
    try:
        resolved_dir = directory.resolve(strict=True)
        if not resolved_dir.is_dir():
            # Use click.echo for consistency, respects testing redirects better
            click.echo(f"Error: Path '{directory}' is not a directory.", file=sys.stderr)
            sys.exit(2)
    except FileNotFoundError:
        click.echo(f"Error: Path '{directory}' does not exist.", file=sys.stderr)
        sys.exit(2)
    except PermissionError as e:
        click.echo(f"Error: Permission error accessing directory '{directory}': {e}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        click.echo(f"Error: OS error accessing directory '{directory}': {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: Unexpected error validating directory '{directory}': {e}", file=sys.stderr)
        sys.exit(1)
    # *** END Explicit Validation ***


    # --- Process Include/Exclude Args ---
    # Split comma-separated patterns received from Click
    processed_include = _split_comma_separated_args(include)
    processed_exclude = _split_comma_separated_args(exclude)
    # --- End Processing ---


    # --- Configuration and Logging Setup ---
    # Use the processed lists for configuration
    cli_args = {
        "output": output,
        "include": processed_include or None, # Use None if list is empty after split
        "exclude": processed_exclude or None, # Use None if list is empty after split
        "max_size": max_size,
        "no_default_ignore": no_default_ignore, # Will be True or False
        "format": format,
        "clipboard": clipboard_flag, # Will be True or False
        "verbose": verbose, # Will be True or None
    }

    # Filter out None values *except* for 'output', as None means stdout/clipboard context
    # Flags like 'no_default_ignore' and 'clipboard' are already boolean T/F
    # 'verbose' will be included only if it's True (i.e., -v was used)
    cli_args_filtered = {
        k: v for k, v in cli_args.items()
        if v is not None or k == "output"
    }

    # Get effective config (CLI overrides file overrides defaults)
    effective_config = get_effective_config(cli_args_filtered, Path.cwd())

    # Setup logging based on the FINAL merged configuration
    setup_logging(effective_config.get("verbose", False))
    log.debug(f"dirdigest version: {__version__}")
    log.debug(f"Effective configuration: {effective_config}")
    log.debug(f"Input directory: {resolved_dir}")
    # Log the patterns *after* splitting and merging if desired
    log.debug(f"Effective include patterns: {effective_config.get('include', [])}")
    log.debug(f"Effective exclude patterns: {effective_config.get('exclude', [])} (User provided)")
    if effective_config.get('default_ignore', True):
        log.debug(f"Default exclude patterns are active.")


    # --- Determine Final Clipboard Behavior ---
    # Use the final config value which respects CLI > File > Default
    use_clipboard = effective_config.get("clipboard", True) # Default true if missing
    log.debug(f"Clipboard copy requested/final: {use_clipboard}")

    # --- Generate Digest ---
    # Pass the effective config which now contains correctly split lists
    digest_content = generate_digest(resolved_dir, effective_config)

    if digest_content is None:
        log.error("Digest generation failed (see previous errors).")
        sys.exit(1)

    # --- Handle Output ---
    file_written = False
    clipboard_copied = False
    stdout_printed = False

    # 1. File Output (if requested by CLI - check original 'output' variable)
    if output:
        log.debug(f"Attempting to write to file: {output}")
        if write_to_file(output, digest_content):
            file_written = True
        else:
            # Make file write failure critical if explicitly requested via CLI
            log.error(f"Critical Failure: Failed to write digest to file: {output}")
            sys.exit(1) # Exit if file writing fails when requested

    # 2. Clipboard Output (if not disabled in final config)
    if use_clipboard:
        log.debug("Attempting to copy to clipboard.")
        if copy_to_clipboard(digest_content):
            clipboard_copied = True
        else:
            log.warning("Failed to copy digest to clipboard.")
            # Fallback to stdout ONLY IF no file was written
            if not file_written: # Check if -o was used and successful
                 log.info("Falling back to stdout due to clipboard failure.")
                 # Use console.print which is configured by utils
                 console.print(digest_content)
                 stdout_printed = True

    # 3. Stdout Output (only if no file AND clipboard was disabled)
    # Check if CLI requested a file and if clipboard ended up disabled
    if not output and not use_clipboard:
         log.debug("Printing output to stdout (file not specified and clipboard explicitly disabled).")
         console.print(digest_content)
         stdout_printed = True

    # --- Final Status Logging ---
    if file_written and clipboard_copied:
         log.info(f"Digest written to {output} and copied to clipboard.")
    elif file_written: # Implies clipboard was disabled or failed silently (shouldn't happen with exit logic?)
         log.info(f"Digest written to {output}.") # Assume clipboard was disabled
    elif clipboard_copied: # Implies no -o was used
         # Log message already printed by copy_to_clipboard
         pass
    elif stdout_printed: # Implies fallback or (--no-clipboard and no -o)
         log.info("Digest printed to stdout.")
    else:
        # This case should only be reached if -o was specified but failed (already exited)
        # or if generation failed (already exited).
        # If code reaches here with no action, it's unexpected.
        log.warning("No definitive output action (file write/clipboard copy/stdout print) was completed.")


    log.info("dirdigest finished successfully")
    sys.exit(0)


if __name__ == "__main__":
    cli_entry()
```

### FILE: `src/dirdigest/config.py`
```py
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
```

### FILE: `src/dirdigest/core.py`
```py
# src/dirdigest/core.py (Removed redundant formatting log message)

import logging
from pathlib import Path
from typing import List, Optional, Tuple

from .filtering import PathFilter
from .formatting import format_json, format_markdown
from .models import DirectoryInfo, FileInfo, FileStatus, FileSystemItem

log = logging.getLogger(__name__)


# Statistics counters
class ProcessingStats:
    def __init__(self):
        # --- Counters ---
        self.files_included = 0
        self.files_excluded_default = 0
        self.files_excluded_user = 0
        self.files_excluded_size = 0
        self.files_excluded_include = 0
        self.files_excluded_output = 0
        self.files_skipped_permission = 0
        self.files_skipped_encoding = 0
        self.dirs_included = 0
        self.dirs_excluded = 0
        self.symlinks_skipped = 0
        # --- Path Lists (Restructured) ---
        self.included_folder_paths: List[str] = []
        self.included_file_paths: List[str] = []
        self.excluded_folder_paths: List[Tuple[str, str]] = [] # (path, reason)
        self.excluded_file_paths: List[Tuple[str, str]] = []   # (path, reason)

    def add_included_path(self, relative_path: str, is_dir: bool):
        """Records an included item's relative path."""
        if is_dir:
            self.included_folder_paths.append(relative_path)
        else:
            self.included_file_paths.append(relative_path)

    def add_excluded_path(self, relative_path: str, reason: str, is_dir: Optional[bool] = None):
        """Records an excluded item's relative path and reason."""
        # Increment specific counters based on reason
        # Note: Some counters are updated more accurately in _build_digest_structure
        if "output file" in reason:
            self.files_excluded_output += 1
        elif "size" in reason and not is_dir: # Only count size for files
            self.files_excluded_size += 1

        # Add to the correct list
        if is_dir:
            self.excluded_folder_paths.append((relative_path, reason))
        else: # Treat as file if is_dir is False or None
            self.excluded_file_paths.append((relative_path, reason))

    def excluded_by_pattern(self, reason: str):
       # This method is largely redundant now as counters are updated elsewhere
       pass

    @property
    def total_files_processed(self) -> int:
        # Note: This counts attempts, including skipped content
        return (
            self.files_included
            + self.files_excluded_default
            + self.files_excluded_user
            + self.files_excluded_size
            + self.files_excluded_include
            + self.files_excluded_output
            + self.files_skipped_permission
            + self.files_skipped_encoding
        )

    @property
    def total_files_excluded_by_filter(self) -> int:
        # Sum of specific file exclusion counters updated in _build_digest_structure
        return (
            self.files_excluded_default
            + self.files_excluded_user
            + self.files_excluded_size
            + self.files_excluded_include
            + self.files_excluded_output
        )

    @property
    def total_dirs_processed(self) -> int:
        return self.dirs_included + self.dirs_excluded

    def log_path_details(self):
        """Logs the collected paths categorized by type and status (included/excluded)."""

        def log_section(title: str, paths: list, color: str, show_reason: bool = False):
            # Use f-string for title formatting consistency
            section_title = f"--- {title} ---"
            log.info(f"[bold]{section_title}[/bold]")
            if paths:
                for item in sorted(paths):
                    if show_reason:
                        path_str, reason = item
                        reason_short = reason.split(" (")[0]
                        log.info(f"  [{color}]- {path_str}[/{color}] ([dim]{reason_short}[/dim])")
                    else:
                        path_str = item
                        log.info(f"  [{color}]+ {path_str}[/{color}]")
            else:
                log.info("  (None)")
            # Make footer match title length
            log.info(f"[bold]{'-' * len(section_title)}[/bold]")
            log.info("") # Add spacing after section

        # Print in the desired order
        log_section("Excluded Folders", self.excluded_folder_paths, "red", show_reason=True)
        log_section("Excluded Files", self.excluded_file_paths, "red", show_reason=True)
        log_section("Included Folders", self.included_folder_paths, "green")
        log_section("Included Files", self.included_file_paths, "green")


    def log_summary(self):
        """Logs the summary statistics."""
        log.info("[bold]--- Processing Summary ---[/bold]")
        log.info(f"Included Files (Content Read): {self.files_included}")
        log.info(f"Included Directories:          {self.dirs_included}")
        # Calculate total excluded dirs count for summary
        total_dirs_excluded = len(self.excluded_folder_paths) + self.symlinks_skipped # Include symlinks if they are counted as excluded dirs elsewhere? Check logic.
        log.info(f"Excluded Directories:          {self.dirs_excluded}") # Use counter updated in _build_digest_structure
        log.info(f"Excluded Files (By Filter):    {self.total_files_excluded_by_filter}")
        log.info(f"  - By Output File Target:     {self.files_excluded_output}")
        log.info(f"  - By Default Pattern:        {self.files_excluded_default}")
        log.info(f"  - By User Pattern:           {self.files_excluded_user}")
        log.info(f"  - By Max Size:               {self.files_excluded_size}")
        log.info(f"  - By Include Pattern:        {self.files_excluded_include}")
        log.info("Skipped File Content (Included Files):")
        log.info(f"  - Permission Errors:         {self.files_skipped_permission}")
        log.info(f"  - Encoding Errors:           {self.files_skipped_encoding}")
        log.info(f"Skipped Symlinks:              {self.symlinks_skipped}")
        log.info("[bold]--------------------------[/bold]")
        log.info("")


def _read_file_content(
    file_path: Path, encoding: str, stats: ProcessingStats
) -> Tuple[Optional[str], FileStatus, float]:
    """Attempts to read file content, handling errors and size."""
    status = FileStatus.INCLUDED
    content = None
    size_bytes = 0
    size_kb = 0.0
    try:
        size_bytes = file_path.stat().st_size
        size_kb = size_bytes / 1024.0
        content = file_path.read_text(encoding=encoding, errors="strict")
        log.debug(f"Read {file_path.name} ({size_kb:.1f} KB)")

    except UnicodeDecodeError:
        log.warning(f"Could not decode {file_path} as {encoding}. Treating as binary/non-text.")
        status = FileStatus.SKIPPED_ENCODING
        stats.files_skipped_encoding += 1
    except PermissionError:
        log.warning(f"Permission error reading {file_path}. Skipping content.")
        status = FileStatus.SKIPPED_PERMISSION
        stats.files_skipped_permission += 1
    except OSError as e:
        log.warning(f"OS error reading {file_path}: {e}. Skipping content.")
        status = FileStatus.SKIPPED_PERMISSION
        stats.files_skipped_permission += 1
    except Exception as e:
        log.error(f"Unexpected error reading {file_path}: {e}", exc_info=True)
        status = FileStatus.SKIPPED_PERMISSION
        stats.files_skipped_permission += 1

    size_kb = (size_bytes / 1024.0) if size_bytes else 0.0
    return content, status, size_kb


def _build_digest_structure(
    current_path: Path,
    root_dir: Path,
    path_filter: PathFilter,
    stats: ProcessingStats,
    config: dict,
) -> Optional[FileSystemItem]:
    """
    Recursively traverses the directory, filters items, and builds the data structure.
    Also collects included/excluded paths in the stats object for logging.
    """
    relative_path_repr = ""
    resolved_current_path = current_path
    is_dir_known = None

    try: resolved_current_path = current_path.resolve()
    except (OSError, FileNotFoundError) as e:
        try: relative_path_repr = str(current_path.relative_to(root_dir).as_posix()) if current_path != root_dir else "."
        except ValueError: relative_path_repr = str(current_path)
        reason = f"Could not resolve path: {e}"
        log.warning(f"{reason}. Skipping {current_path}.")
        stats.add_excluded_path(relative_path_repr, reason, is_dir=None)
        return None

    resolved_root_dir = root_dir

    try:
        if resolved_current_path == resolved_root_dir: relative_path_repr = "."
        else: relative_path_repr = str(resolved_current_path.relative_to(resolved_root_dir).as_posix())
    except ValueError:
        reason = f"Path outside root directory {resolved_root_dir}"
        log.warning(f"{resolved_current_path}: {reason}. Skipping.")
        is_dir_known = None
        try: is_dir_known = resolved_current_path.is_dir()
        except OSError: pass
        stats.add_excluded_path(str(resolved_current_path), reason, is_dir=is_dir_known)
        return None

    pathspec_match_path = ("" if relative_path_repr == "." else relative_path_repr)

    follow_symlinks = config.get("follow_symlinks", False)
    if current_path.is_symlink():
        is_dir_known = None
        if not follow_symlinks:
            reason = "Skipping symlink (follow_symlinks=False)"
            log.debug(f"{relative_path_repr}: {reason} (points to {resolved_current_path})")
            stats.symlinks_skipped += 1
            try: is_dir_known = resolved_current_path.is_dir()
            except OSError: pass
            stats.add_excluded_path(relative_path_repr, reason, is_dir=is_dir_known)
            return None
        else:
            if resolved_current_path == resolved_root_dir:
                reason = "Symlink loop detected: -> root"
                log.warning(f"{relative_path_repr}: {reason}. Skipping.")
                stats.symlinks_skipped += 1
                stats.add_excluded_path(relative_path_repr, reason, is_dir=True)
                return None

    try:
        if not resolved_current_path.exists():
            reason = "Path does not exist after resolution/symlink check"
            log.warning(f"{relative_path_repr}: {reason}. Skipping.")
            stats.add_excluded_path(relative_path_repr, reason, is_dir=None)
            return None

        is_dir = resolved_current_path.is_dir()
        is_dir_known = True

        include_item, reason = path_filter.check(resolved_current_path, pathspec_match_path)

        if not include_item:
            stats.add_excluded_path(relative_path_repr, reason, is_dir=is_dir)
            if is_dir:
                stats.dirs_excluded += 1
                # Update detailed counters if needed based on reason for dir exclusion
                if "default pattern" in reason: stats.files_excluded_default += 0 # Example: No specific counter for default excluded dirs yet
                elif "user pattern" in reason: stats.files_excluded_user += 0
                elif "include pattern" in reason: stats.files_excluded_include += 0
            else: # Is file
                # Counters updated in add_excluded_path for size/output
                # Update pattern counters here
                if "default pattern" in reason: stats.files_excluded_default += 1
                elif "user pattern" in reason: stats.files_excluded_user += 1
                elif "include pattern" in reason: stats.files_excluded_include += 1
                else: stats.files_excluded_user += 1 # Fallback
            return None

        stats.add_included_path(relative_path_repr, is_dir=is_dir)

        if is_dir:
            stats.dirs_included += 1
            log.debug(f"Processing directory: {relative_path_repr}")
            dir_info = DirectoryInfo(relative_path=relative_path_repr, absolute_path=resolved_current_path, children=[])
            try: items_in_dir = sorted(list(resolved_current_path.iterdir()))
            except PermissionError:
                reason = "Permission error listing contents"
                log.warning(f"{relative_path_repr}: {reason}. Skipping directory children.")
                return dir_info
            except OSError as e:
                reason = f"OS error listing contents: {e}"
                log.warning(f"{relative_path_repr}: {reason}. Skipping directory children.")
                return dir_info

            for item_path in items_in_dir:
                child_item = _build_digest_structure(item_path, resolved_root_dir, path_filter, stats, config)
                if child_item: dir_info.children.append(child_item)
            return dir_info

        else: # Item is a file
            content, status, size_kb = _read_file_content(resolved_current_path, config.get("encoding", "utf-8"), stats)
            if status == FileStatus.INCLUDED: stats.files_included += 1
            file_info = FileInfo(relative_path=relative_path_repr, absolute_path=resolved_current_path, content=content, status=status, size_kb=size_kb)
            return file_info

    except PermissionError:
        reason = "Permission error accessing item"
        log.warning(f"{relative_path_repr}: {reason} (Resolved: {resolved_current_path}). Skipping.")
        stats.add_excluded_path(relative_path_repr, reason, is_dir=is_dir_known)
        if is_dir_known is True: stats.dirs_excluded += 1
        else: stats.files_skipped_permission += 1
        return None
    except (OSError, FileNotFoundError) as e:
        reason = f"OS error processing item: {e}"
        log.warning(f"{relative_path_repr}: {reason} (Resolved: {resolved_current_path}). Skipping.")
        stats.add_excluded_path(relative_path_repr, reason, is_dir=is_dir_known)
        if is_dir_known is True: stats.dirs_excluded += 1
        else: stats.files_skipped_permission += 1
        return None
    except Exception as e:
        reason = f"Unexpected error processing item: {e}"
        log.error(f"{relative_path_repr}: {reason} (Resolved: {resolved_current_path})", exc_info=True)
        stats.add_excluded_path(relative_path_repr, reason, is_dir=is_dir_known)
        if is_dir_known is True: stats.dirs_excluded += 1
        else: stats.files_skipped_permission += 1
        return None


def generate_digest(directory: Path, config: dict) -> Optional[str]:
    """Generates the digest for the specified directory based on the configuration."""
    log.info(f"Starting dirdigest scan for directory: {directory}")
    log.info(f"Output format: {config['format']}")
    log.info(f"Max file size: {config['max_size']} KB")
    log.info("")

    try: resolved_root = directory.resolve()
    except (OSError, FileNotFoundError) as e:
        log.error(f"Input directory {directory} cannot be resolved or accessed: {e}", exc_info=True)
        return None

    output_file = config.get("output")
    path_filter = PathFilter(
        root_dir=resolved_root,
        include_patterns=config.get("include"),
        exclude_patterns=config.get("exclude"),
        use_default_excludes=config.get("default_ignore", True),
        max_file_size_kb=config.get("max_size"),
        output_file_path=output_file,
    )

    stats = ProcessingStats()
    root_item = _build_digest_structure(resolved_root, resolved_root, path_filter, stats, config)

    stats.log_path_details()
    stats.log_summary()

    if root_item is None:
        root_was_processed_and_excluded = any(p == "." for p, r in stats.excluded_folder_paths + stats.excluded_file_paths)
        if root_was_processed_and_excluded: log.error("Root directory '.' was excluded. No output generated.")
        else: log.error("Failed to build the directory structure (root item is None). No output generated.")
        return None

    if isinstance(root_item, DirectoryInfo) and not root_item.children:
         if not stats.included_file_paths and not stats.included_folder_paths and (stats.excluded_file_paths or stats.excluded_folder_paths):
             log.warning("The scanned directory appears empty or fully excluded based on filters. Generating empty digest.")
         elif not stats.included_file_paths and not stats.included_folder_paths and not stats.excluded_file_paths and not stats.excluded_folder_paths:
             log.warning("The scanned directory appears empty or contained only unprocessable items. Generating empty digest.")

    if not isinstance(root_item, DirectoryInfo):
         log.error(f"Built structure is not a DirectoryInfo object ({type(root_item)}). Cannot format.")
         return None

    # --- Format output ---
    output_format = config.get("format", "markdown").lower()
    try:
        # --- Removed redundant log message here ---
        # log.info(f"Formatting output as {output_format.upper()}...")
        if output_format == "json": 
            digest_content = format_json(root_item)
        elif output_format == "markdown": 
            digest_content = format_markdown(root_item)
        else:
            log.error(f"Invalid output format specified: {output_format}. Defaulting to Markdown.")
            digest_content = format_markdown(root_item)
        # Keep the specific log messages inside format_json/format_markdown
        #log.info("Formatting complete.")
        # log.info("")
        return digest_content
    except Exception as e:
         log.error(f"Error during output formatting ({output_format}): {e}", exc_info=True)
         return None
```

### FILE: `src/dirdigest/filtering.py`
```py
# src/dirdigest/filtering.py (Added output file exclusion)

import logging
from pathlib import Path
from typing import List, Optional, Tuple

import pathspec

from .config import DEFAULT_EXCLUDE_PATTERNS

log = logging.getLogger(__name__)


class PathFilter:
    """Applies include/exclude filters to paths."""

    def __init__(
        self,
        root_dir: Path,
        include_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
        use_default_excludes: bool = True,
        max_file_size_kb: Optional[int] = None,
        output_file_path: Optional[Path] = None, # <<< Added output file path parameter
    ):
        """
        Initializes the PathFilter.

        Args:
            root_dir: The root directory relative to which patterns are matched.
            include_patterns: List of glob patterns to include. If None or empty,
                              all non-excluded items are implicitly included.
            exclude_patterns: List of user-provided glob patterns to exclude.
            use_default_excludes: Whether to use the built-in default exclude patterns.
            max_file_size_kb: Maximum file size in KB to include. Files larger
                              than this will be excluded by the size check.
            output_file_path: The Path object representing the output file, if specified.
        """
        self.root_dir = root_dir.resolve()
        self.include_patterns = include_patterns or []
        self.user_exclude_patterns = exclude_patterns or []
        self.use_default_excludes = use_default_excludes
        self.max_file_size_bytes = (
            max_file_size_kb * 1024 if max_file_size_kb is not None else None
        )

        # Store the resolved absolute path of the output file for comparison
        # Resolve relative paths against the current working directory where the CLI runs
        try:
            self.output_file_abs_path = output_file_path.resolve() if output_file_path else None
        except OSError as e:
            log.warning(f"Could not resolve output file path {output_file_path}: {e}. Output file exclusion might not work correctly.")
            self.output_file_abs_path = None

        # Compile pathspec matchers
        self.default_spec = pathspec.PathSpec.from_lines(
            'gitwildmatch', DEFAULT_EXCLUDE_PATTERNS
        ) if self.use_default_excludes else None
        self.user_exclude_spec = pathspec.PathSpec.from_lines(
            'gitwildmatch', self.user_exclude_patterns
        ) if self.user_exclude_patterns else None
        self.include_spec = pathspec.PathSpec.from_lines(
            'gitwildmatch', self.include_patterns
        ) if self.include_patterns else None

        log.debug(f"Filter initialized. Root context: {self.root_dir}")
        log.debug(f"  Default excludes active: {self.use_default_excludes}")
        if self.output_file_abs_path:
             log.debug(f"  Output file exclusion target: {self.output_file_abs_path}")
        if self.user_exclude_patterns:
             log.debug(f"  User excludes: {self.user_exclude_patterns}")
        if self.include_patterns:
             log.debug(f"  Includes: {self.include_patterns}")
        if self.max_file_size_bytes is not None:
            log.debug(f"  Max file size: {max_file_size_kb} KB ({self.max_file_size_bytes} B)")


    def check(self, path: Path, relative_path_str: str) -> Tuple[bool, str]:
        """
        Checks if a path should be included based on the filter rules.
        Order of checks: Output File -> Default Excludes -> User Excludes -> Include Patterns -> Size.
        """
        try:
            # Resolve path here for reliable stat checks
            abs_path = path.resolve()
            if not abs_path.exists():
                 reason = f"Excluded: Path does not exist after resolving '{path}' -> '{abs_path}'"
                 log.warning(reason)
                 return False, reason

            is_dir = abs_path.is_dir()
            display_path = relative_path_str or "."

            # --- 1. Output File Check ---
            if self.output_file_abs_path and abs_path == self.output_file_abs_path:
                reason = f"Excluded: Matches output file path '{display_path}'"
                log.debug(f"{display_path}: {reason}")
                return False, reason

            # Prepare path string for pattern matching
            match_str = relative_path_str
            if is_dir and match_str != ".":
                match_str += '/'

            # --- 2. Default Exclusions ---
            if self.default_spec and self.default_spec.match_file(match_str):
                reason = f"Excluded by default pattern matching '{display_path}'"
                log.debug(f"{display_path}: {reason}")
                return False, reason

            # --- 3. User Exclusions ---
            if self.user_exclude_spec and self.user_exclude_spec.match_file(match_str):
                reason = f"Excluded by user pattern matching '{display_path}'"
                log.debug(f"{display_path}: {reason}")
                return False, reason

            # --- 4. Inclusion Checks (Only if --include patterns are specified) ---
            # <<< Refined include logic >>>
            if self.include_spec:
                # Files MUST match include spec
                if not is_dir and not self.include_spec.match_file(match_str):
                    reason = f"Excluded: File does not match any '--include' pattern ('{display_path}')"
                    log.debug(f"{display_path}: {reason}")
                    return False, reason
                # Directories are allowed if they don't match excludes (handled above)
                # They don't strictly need to match an include pattern themselves to allow traversal
                # Note: If a dir *does* match an include, it's still included.
                # If the directory itself was excluded by steps 2 or 3, we wouldn't reach here.

            # --- 5. File Size Check (Only for files) ---
            if not is_dir and self.max_file_size_bytes is not None:
                try:
                    file_size = abs_path.stat().st_size
                    if file_size > self.max_file_size_bytes:
                        reason = (f"Excluded by size ({file_size / 1024:.1f} KB "
                                  f"> max {self.max_file_size_bytes / 1024:.1f} KB)")
                        log.debug(f"{display_path}: {reason}")
                        return False, reason
                except OSError as e:
                    reason = f"Warning: Could not get size for {abs_path.name}, skipping size check ({e})"
                    log.warning(reason)

            # --- If not excluded by any rule ---
            log.debug(f"{display_path}: Included")
            return True, "Included"

        # ... (Exception handling remains the same) ...
        except FileNotFoundError:
             reason = f"Error during filtering: File not found {path}"
             log.warning(reason)
             return False, reason
        except OSError as e:
            reason = f"OS error during filtering {path}: {e}"
            log.warning(reason)
            return False, reason
        except Exception as e:
            reason = f"Unexpected error during filtering {path}: {e}"
            log.error(reason, exc_info=True)
            return False, reason
```

### FILE: `src/dirdigest/formatting.py`
```py
# src/dirdigest/formatting.py (Removed redundant 'status: included' from JSON)

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, cast

from rich.text import Text
from rich.tree import Tree

from .models import DirectoryInfo, FileInfo, FileStatus, FileSystemItem

log = logging.getLogger(__name__)

# --- Placeholder Messages ---\
# Used for Markdown output when content is skipped
PLACEHOLDERS = {
    FileStatus.SKIPPED_SIZE: "[dirdigest: file skipped, size > max_size KB]",
    FileStatus.SKIPPED_ENCODING: "[dirdigest: binary or non-UTF8 file]",
    FileStatus.SKIPPED_BINARY: "[dirdigest: binary or non-UTF8 file]", # Same as encoding for simplicity
    FileStatus.SKIPPED_PERMISSION: "[dirdigest: permission error reading file]",
}

def _get_placeholder(item: FileInfo) -> str:
    """Gets the appropriate placeholder message for a skipped file (Markdown)."""
    placeholder = PLACEHOLDERS.get(item.status, "[dirdigest: file content skipped]")
    # Add relative path context to the placeholder
    return f"{placeholder} at {item.relative_path}"


# --- JSON Formatting ---\

def _build_json_structure(item: FileSystemItem) -> Dict[str, Any]:
    """Recursively builds the dictionary structure for JSON output."""
    if isinstance(item, FileInfo):
        # Use content if included, otherwise use a placeholder string similar to Markdown
        # Choose a placeholder that clearly indicates skipped content in JSON context
        json_placeholder = f"[dirdigest: content skipped - {item.status.value}]"
        content_value = item.content if item.status == FileStatus.INCLUDED else json_placeholder

        file_dict: Dict[str, Any] = {
            "type": item.type.value,
            "relative_path": item.relative_path,
            "content": content_value,
            # Optionally add size_kb: round(item.size_kb, 2)
            # "size_kb": round(item.size_kb, 2)
        }
        # --- Conditionally add status only if NOT included ---
        if item.status != FileStatus.INCLUDED:
            file_dict["status"] = item.status.value # e.g., "skipped_size", "skipped_encoding"

        return file_dict

    elif isinstance(item, DirectoryInfo):
        # Sort children before processing for consistent output
        item.sort_children()
        children_json = [_build_json_structure(child) for child in item.children]
        return {
            "type": item.type.value,
            "relative_path": item.relative_path,
            "children": children_json,
        }
    else:
         # Should not happen with type hints, but handle defensively
        log.error(f"Unexpected item type encountered during JSON generation: {type(item)}")
        return {"error": "Unknown item type"}


def format_json(root: DirectoryInfo) -> str:
    """Formats the directory structure as a JSON string."""
    #log.info("Formatting output as JSON...")
    json_structure = _build_json_structure(root)
    try:
        # Ensure final newline for POSIX compatibility
        return json.dumps(json_structure, indent=2) + "\n"
    except TypeError as e:
        log.error(f"Error serializing data to JSON: {e}", exc_info=True)
        # Provide a valid JSON error object
        return json.dumps({"error": "Failed to serialize data to JSON", "details": str(e)}, indent=2) + "\n"


# --- Markdown Formatting ---\

def _generate_tree_overview(directory: DirectoryInfo) -> str:
    """Generates a plain text tree structure overview for Markdown."""
    if not directory.children:
        # Represent empty included directory
        return f"{directory.relative_path}/\n(empty)\n"

    tree = Tree(f"{directory.relative_path}/", guide_style="dim")
    directory.sort_children() # Sort for consistent tree view

    def add_nodes(node: Tree, items: List[FileSystemItem]):
        for i, item in enumerate(items):
            is_last = (i == len(items) - 1)
            # Ensure guide style is consistent even for last item unless it's truly the end
            guide_style = "dim" # Default guide style

            if isinstance(item, DirectoryInfo):
                style = "bold bright_blue"
                # Use Path name for display, add trailing slash
                child_node = node.add(f"{Path(item.relative_path).name}/", style=style, guide_style=guide_style)
                # Optional: Recursively add nodes for deeper tree view (currently shallow)
                # add_nodes(child_node, item.children)
            elif isinstance(item, FileInfo):
                name = Path(item.relative_path).name
                status_marker = ""
                style = ""
                if item.status != FileStatus.INCLUDED:
                    # Use a shorter marker for tree view
                    status_marker = f" [skipped]"
                    style = "dim" # Dim skipped files in tree
                node.add(f"{name}{status_marker}", style=style, guide_style=guide_style)

    add_nodes(tree, directory.children)

    # Render the tree to plain text using Rich's console capture
    from rich.console import Console
    # Create a temporary console for capturing tree output
    capture_console = Console(record=True, width=120, force_terminal=False, color_system=None)
    # capture_console.print(tree)
    # Export without styles to keep it plain text for Markdown
    return capture_console.export_text(styles=False)


def _format_markdown_recursive(item: FileSystemItem, output_lines: List[str]):
    """Recursively builds the Markdown output lines."""

    if isinstance(item, DirectoryInfo):
        folder_path = item.relative_path
        # Use slightly more prominent headers
        output_lines.append(f"## FOLDER: `{folder_path}`")
        output_lines.append("") # Add newline

        # Generate and add the tree overview for this directory level
        tree_overview = _generate_tree_overview(item)
        output_lines.append("```text") # Use text code block for tree
        output_lines.append(tree_overview.strip()) # Add tree, remove leading/trailing whitespace
        output_lines.append("```")
        output_lines.append("") # Add newline

        # Process files directly within this folder first
        files_in_folder = [child for child in item.children if isinstance(child, FileInfo)]
        for file_item in files_in_folder:
             _format_markdown_recursive(file_item, output_lines) # Adds FILE section

        # Then recursively process sub-folders
        sub_folders = [child for child in item.children if isinstance(child, DirectoryInfo)]
        for sub_folder_item in sub_folders:
             _format_markdown_recursive(sub_folder_item, output_lines) # Adds FOLDER section

        # Optional: Add explicit end marker, might be too verbose
        # output_lines.append(f"--- END FOLDER: {folder_path} ---")
        # output_lines.append("") # Add newline

    elif isinstance(item, FileInfo):
        file_path = item.relative_path
        # Use slightly more prominent headers
        output_lines.append(f"### FILE: `{file_path}`")

        # Get content or placeholder message
        content = item.content if item.status == FileStatus.INCLUDED else _get_placeholder(item)

        # Determine language for syntax highlighting
        lang = Path(file_path).suffix.lstrip('.') if Path(file_path).suffix else ""
        # Basic check for known non-code types that shouldn't get language hints
        # Allow common text/markup/data formats
        allowed_langs = {"txt", "md", "markdown", "rst", "csv", "tsv", "xml", "html", "css", "json", "yaml", "toml", "py", "js", "java", "c", "cpp", "cs", "go", "rb", "php", "swift", "kt", "rs", "sh", "bash", "sql", "dockerfile", "hcl", "tf"}
        if lang.lower() not in allowed_langs:
             lang = "" # Default to no language hint if suffix unknown/not text-like
        if item.status != FileStatus.INCLUDED:
             lang = "" # No language for placeholders

        # Add content within a fenced code block
        output_lines.append(f"```{lang}")
        if content is not None:
            # Ensure content ends with a newline before the closing fence if it's not empty
            output_lines.append(content.rstrip('\n'))
        output_lines.append("```")
        output_lines.append("") # Add newline after file block


def format_markdown(root: DirectoryInfo) -> str:
    """Formats the directory structure as a Markdown string."""
    #log.info("Formatting output as MARKDOWN...")
    output_lines: List[str] = []
    # Start formatting from the root directory
    _format_markdown_recursive(root, output_lines)
    # Join lines, ensuring a single trailing newline
    return "\n".join(output_lines).strip() + "\n"
```

### FILE: `src/dirdigest/models.py`
```py
# src/dirdigest/models.py (Corrected)

import dataclasses
from enum import Enum
from pathlib import Path
from typing import List, Optional, Union


class ItemType(Enum):
    """Type of filesystem item."""
    FOLDER = "folder"
    FILE = "file"


class FileStatus(Enum):
    """Status of a file regarding inclusion in the digest."""
    INCLUDED = "included"
    SKIPPED_SIZE = "skipped_size"
    SKIPPED_ENCODING = "skipped_encoding"
    SKIPPED_PERMISSION = "skipped_permission"
    SKIPPED_BINARY = "skipped_binary" # Explicit status for non-text files


@dataclasses.dataclass
class FileInfo:
    """Represents information about a file."""
    # --- Non-default arguments first ---
    relative_path: str
    absolute_path: Path
    # --- Default arguments follow ---
    type: ItemType = ItemType.FILE
    content: Optional[str] = None
    status: FileStatus = FileStatus.INCLUDED
    size_kb: float = 0.0


@dataclasses.dataclass
class DirectoryInfo:
    """Represents information about a directory."""
    # --- Non-default arguments first ---
    relative_path: str
    absolute_path: Path
    # --- Default arguments follow ---
    type: ItemType = ItemType.FOLDER
    children: List[Union["DirectoryInfo", FileInfo]] = dataclasses.field(default_factory=list)

    def sort_children(self):
        """Sorts children alphabetically by relative path."""
        self.children.sort(key=lambda item: item.relative_path)

# Define a type alias for convenience
FileSystemItem = Union[DirectoryInfo, FileInfo]
```

### FILE: `src/dirdigest/utils.py`
```py
# src/dirdigest/utils.py
import logging
import sys
from pathlib import Path
from typing import Optional

import pyperclip
from rich.console import Console
from rich.logging import RichHandler

log = logging.getLogger(__name__)

console = Console()
log_console = Console(stderr=True)


def setup_logging(verbose: bool):
    """Configures logging using RichHandler, suppressing INFO when testing unless verbose."""
    # --- Test Detection ---
    # Simple check if pytest is running
    is_testing = "pytest" in sys.modules

    # Determine log level
    if verbose:
        log_level = logging.DEBUG
    elif is_testing:
        # Suppress INFO logs during tests unless -v is used
        log_level = logging.WARNING
    else:
        # Default for normal execution
        log_level = logging.INFO
    # --- End Test Detection ---

    # Remove existing handlers to prevent duplicates if called multiple times
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        level=log_level, # Use determined level
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                console=log_console,
                show_level=False,
                show_path=False,
                show_time=False,
                rich_tracebacks=True,
                markup=True,
                # Set level on handler as well to be sure
                level=log_level
            )
        ],
        # Force=True might be needed if basicConfig was called previously implicitly
        # force=True
    )

    if verbose:
        log.debug("Verbose logging enabled.") # This will only show if level is DEBUG


def copy_to_clipboard(text: str) -> bool:
    """Copies text to the system clipboard. Assumes success if no exception."""
    try:
        pyperclip.copy(text)
        # Use log.info - this will be suppressed in tests unless -v
        log.info("Digest copied to clipboard.")
        return True
    except pyperclip.PyperclipException as e:
        log.warning(f"Clipboard access failed: {e}")
        log.warning("Could not copy to clipboard. Ensure 'xclip' or 'xsel' (Linux), "
                    "'pbcopy' (macOS), or appropriate Windows mechanisms are available.")
        return False
    except Exception as e:
        log.error(f"Unexpected error during clipboard operation: {e}", exc_info=True)
        return False


def write_to_file(path: Path, content: str) -> bool:
    """Writes content to the specified file."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        # Use log.info - this will be suppressed in tests unless -v
        log.info(f"Digest written to file: {path}")
        return True
    except OSError as e:
        log.error(f"Error writing to output file {path}: {e}", exc_info=True)
        return False
    except Exception as e:
        log.error(f"Unexpected error writing to file {path}: {e}", exc_info=True)
        return False
```
