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

## Contributing

(Optional: Add guidelines for contributing if you plan for others to contribute.)
Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

(Optional: Specify the license, e.g., MIT License. Make sure you have a corresponding LICENSE file.)
This project is licensed under the MIT License - see the LICENSE file for details.