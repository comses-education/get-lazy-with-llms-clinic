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
