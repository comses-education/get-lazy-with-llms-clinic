**Improved Requirements for `promptbuilder`**

**1. Core Functionality**

*   **Purpose:** Generate a META_PROMPT designed to instruct an LLM to create a high-quality TASK_PERFORMING_PROMPT based on user inputs.
*   **Modes of Operation:**
    *   **CLI Mode:** Operate based on command-line arguments provided at invocation.
    *   **Interactive Mode:** Guide the user through a series of prompts to gather the necessary information if invoked with the `--interactive` flag.
*   **Input Sources:** Accept task description, context (files/folders), meta-instructions, input/output descriptions, and input/output instructions via command-line arguments *or* interactive prompts, potentially reading content from specified files.
*   **Output:** Produce the generated META_PROMPT.

**2. Command-Line Interface (CLI)**

*   **Invocation:** `promptbuilder [OPTIONS]`
*   **Arguments:**
    *   `--task TEXT`: **(Required)** A concise description of the *ultimate* task the user wants the *final* LLM to perform. Used to instruct the META_PROMPT generator.
    *   `--context PATH [PATH ...]`: Specifies one or more local file paths or directory paths. Directories should be parsed recursively for supported file types (see Configuration).
    *   `--meta-instructions TEXT_OR_PATH`: *(Renamed from `--instructions` for clarity)* Instructions specifically for the LLM generating the META_PROMPT, guiding *how* it should construct the TASK_PERFORMING_PROMPT (e.g., "Generate a prompt suitable for a novice user", "Ensure the prompt asks the LLM to adopt the persona of a helpful assistant"). Can be a string or a path to a file.
    *   `--input TEXT_OR_PATH`: Description of the *expected input* for the final TASK_PERFORMING_PROMPT. If provided, the META_PROMPT must instruct the generation of a `{{INPUT}}` placeholder (or configured equivalent) in the TASK_PERFORMING_PROMPT. Can be a string or a path to a file.
    *   `--output TEXT_OR_PATH`: Description of the *desired output* from the final TASK_PERFORMING_PROMPT. If provided, the META_PROMPT must instruct the generation of an `{{OUTPUT}}` placeholder (or configured equivalent) or descriptive section in the TASK_PERFORMING_PROMPT. Can be a string or a path to a file.
    *   `--input-instructions TEXT_OR_PATH`: Specific instructions on *how the user should provide input* to the final TASK_PERFORMING_PROMPT. If provided, the META_PROMPT must instruct the generation of an `{{INPUT_INSTRUCTIONS}}` placeholder (or configured equivalent) or descriptive section in the TASK_PERFORMING_PROMPT. Can be a string or a path to a file.
    *   `--output-instructions TEXT_OR_PATH`: Specific instructions on *how the LLM should format or structure its output* when using the final TASK_PERFORMING_PROMPT. If provided, the META_PROMPT must instruct the generation of an `{{OUTPUT_INSTRUCTIONS}}` placeholder (or configured equivalent) or descriptive section in the TASK_PERFORMING_PROMPT. Can be a string or a path to a file.
    *   `--example-input TEXT_OR_PATH`: *(New)* An example of valid input for the final TASK_PERFORMING_PROMPT. To be included in the META_PROMPT to guide the TASK_PERFORMING_PROMPT generation.
    *   `--example-output TEXT_OR_PATH`: *(New)* An example of the desired output for the final TASK_PERFORMING_PROMPT. To be included in the META_PROMPT.
    *   `--save-on-disk PATH`: If provided, save the generated META_PROMPT to this file path instead of printing to stdout.
    *   `--copy`: *(New, replaces implicit copy)* A flag to explicitly request copying the generated META_PROMPT to the system clipboard upon successful execution.
    *   `--config PATH`: *(New)* Specify a path to a configuration file (default: `./.promptbuilder` or `~/.config/promptbuilder/.promptbuilder`).
    *   `--template PATH`: *(New)* Specify a custom META_PROMPT template file to use instead of the default.
    *   `-i, --interactive`: *(New)* Activate Interactive Mode.
    *   `-v, --verbose`: *(New)* Increase output verbosity (e.g., show loaded config, files parsed). Multiple `-v` flags increase verbosity level.
    *   `-h, --help`: Display help message and exit.

**3. Interactive Mode (`--interactive`)**

*   **Activation:** Triggered by the `-i` or `--interactive` flag.
*   **Goal:** Guide the user step-by-step to gather all necessary information for building the META_PROMPT.
*   **Behavior:**
    *   **Respects CLI Arguments:** If other arguments (e.g., `--task`) are provided alongside `--interactive`, use those values as defaults and *do not* prompt the user for that specific piece of information. Prompt only for missing information.
    *   **Initial Prompt:** Start by asking for the `--task` description (if not provided via CLI). This is mandatory.
    *   **Sequential Prompting:** Proceed to ask for optional inputs corresponding to the CLI arguments (`--context`, `--meta-instructions`, `--input`, `--output`, etc.).
        *   Clearly state what information is being requested (e.g., "Enter the path to a file or folder for context (leave blank to skip):").
        *   Indicate optional fields clearly (e.g., "[Optional] Describe the expected input format...").
        *   Allow users to skip optional fields easily (e.g., by pressing Enter on an empty line).
    *   **Input Handling:**
        *   **Text Input:** For descriptions/instructions provided as strings, allow multi-line input. Define a clear end-of-input mechanism (e.g., typing `END` on a new line or pressing Ctrl+D).
        *   **Path Input:** Prompt for file or directory paths. Validate path existence *after* entry if feasible/desired. Allow adding multiple context paths sequentially until the user indicates they are done (e.g., entering 'done' or leaving blank). Clarify recursive parsing for directories.
    *   **Configuration:** Load defaults from the configuration file (`.promptbuilder`) before starting the interactive session.
    *   **Confirmation:** Before generating the final META_PROMPT, display a summary of all collected information (task description, context files listed, input/output descriptions, etc.) and ask the user for confirmation (e.g., "Proceed with generation? [Y/n]"). If 'n', exit gracefully.
    *   **Final Options:** After gathering core prompt info, ask about final actions:
        *   "Save prompt to disk? (Enter path or leave blank for stdout):"
        *   "Copy prompt to clipboard? [y/N]:"
    *   **Generation:** Upon confirmation, generate the META_PROMPT using the collected information.
    *   **Output:** Display to stdout or save to file, and copy to clipboard, based on the user's choices in the final options step.


**4. Configuration (`.promptbuilder` file)**

*   **Location:** Search order: `./.promptbuilder`, `~/.config/promptbuilder/.promptbuilder`. Allow overriding with `--config`.
*   **Format:** INI or YAML (Choose one, YAML is more flexible).
*   **Defaults:** Provide reasonable defaults for:
    *   `default_meta_prompt_template_path`: Path to the default META_PROMPT template file shipped with the tool.
    *   `placeholder_format`: String format for placeholders (e.g., `{{%s}}`, `__%s__`). Default: `{{%s}}`.
    *   `context_max_file_size_mb`: Maximum size for individual files included from context (to prevent memory issues). Default: 5MB.
    *   `context_supported_extensions`: List of file extensions to parse recursively (e.g., `.txt, .md, .py, .json, .yaml, .xml`). Default: `.txt, .md`.
    *   `context_encoding`: Default text encoding for reading files. Default: `utf-8`.
    *   `copy_to_clipboard_default`: Boolean (true/false) whether to copy by default (alternative to requiring `--copy`). Default: `false`.
    *   `output_dir`: Default directory to save prompts if `--save-on-disk` is used without a full path. Default: `.`.
    *   `interactive_multiline_end_marker` (New, e.g., `END`. Default: `END`)

**5. Context Handling**

*   **Recursive Parsing:** If a directory is provided via `--context`, recursively find files matching `context_supported_extensions`.
*   **Content Inclusion:**
    *   Provide a clear summary of the context included in the META_PROMPT (e.g., list of filenames, total size).
    *   Consider adding a `--context-mode` flag (e.g., `list`=filenames only, `snippets`=filenames+first N lines, `full`=full content within size limits) - *Start with `list` and maybe `full` with size limits.*
*   **File Size Limit:** Apply `context_max_file_size_mb` limit. Skip or truncate files exceeding the limit, issuing a warning if verbose.
*   **Encoding:** Use `context_encoding` from config, falling back gracefully if decoding fails (e.g., skip file with warning).

**6. META_PROMPT Generation**

*   **Templating Engine:** Use a standard templating engine (e.g., Jinja2) to build the META_PROMPT from a template file.
*   **Default Template:** Provide a well-structured default META_PROMPT template based on the best practices outlined in the context document (clear directive, sections with delimiters, role setting, instructions for placeholders, context summary integration).
*   **Placeholder Injection:**
    *   Dynamically inject user-provided content (`--task`, context summary, `--meta-instructions`, etc.) into the template.
    *   If `--input`, `--output`, `--input-instructions`, or `--output-instructions` are provided, the META_PROMPT *must* explicitly instruct the LLM to include corresponding placeholders (using the configured `placeholder_format`) or descriptive sections in the generated TASK_PERFORMING_PROMPT. The META_PROMPT itself should clearly show *what* these placeholders represent (using the user-provided descriptions).
    *   Example section in META_PROMPT if `--input` is used:
        ```
        #### INPUT SPECIFICATIONS ####
        The final prompt must instruct the LLM to expect input described as:
        [Content from --input argument or file]
        The final prompt MUST include a placeholder formatted as '{{INPUT}}' for the user to insert their actual input.
        ```
*   **Example Inclusion:** If `--example-input` or `--example-output` are provided, include them clearly within the META_PROMPT to guide the LLM.

**7. Output & Integration**

*   **Standard Output:** By default, print the generated META_PROMPT to `stdout`.
*   **Save to Disk:** If `--save-on-disk PATH` is provided, write the META_PROMPT to the specified file. Handle potential file system errors gracefully.
*   **Clipboard:** If `--copy` is specified (or if `copy_to_clipboard_default` is true in config and not overridden), copy the generated META_PROMPT to the system clipboard using a cross-platform library (e.g., `pyperclip`). Provide feedback (e.g., "Prompt copied to clipboard.").

**8. Reliability & Error Handling**

*   **Input Validation:** Validate command-line arguments (e.g., check if file paths exist).
*   **File Handling:** Implement robust error handling for file I/O (reading context, instructions, saving output), providing informative error messages.
*   **Dependency Management:** Use `pyproject.toml` (with Poetry or similar) or `requirements.txt` to manage dependencies.
*   **Testing:** Include unit tests for core logic (argument parsing, file reading, template rendering) and integration tests for common usage scenarios.

**9. Maintainability, Modularity & Testability**
*   **Architectural Goal:** Design the application with a **highly modular structure** to ensure components are independently testable, maintainable, and potentially reusable.
*   **Code Structure:**
    *   Organize code into distinct modules with clear responsibilities (e.g., `cli.py` for command-line parsing and flow control, `config.py` for loading/managing settings, `context.py` for parsing context files/folders, `templating.py` for META_PROMPT generation, `interactive.py` for the interactive session logic, `utils.py` for common helpers like file I/O or clipboard).
*   **Decoupling:**
    *   **Isolate Core Logic:** The core functionality (parsing context, reading files, rendering templates using collected data) **must** be implemented in functions or classes that are independent of the specific CLI framework (`argparse`, `click`, etc.) and the interactive prompting library.
    *   **Dependency Injection:** Where appropriate, pass dependencies (like configuration objects, file readers, or template renderers) into functions or classes rather than relying on global state. This makes unit testing significantly easier as dependencies can be mocked.
*   **Testability:**
    *   **Unit Tests:** Implement comprehensive unit tests for each module, focusing on testing the isolated core logic. Mock external dependencies like file system access or clipboard operations.
    *   **Integration Tests:** Create integration tests that verify the end-to-end flows for both CLI argument-based usage and the interactive mode. These tests should cover common scenarios, including file handling and configuration loading.
*   **Readability & Standards:** Use clear variable names, extensive type hints (enforced where possible), comprehensive docstrings, and adhere strictly to PEP 8 guidelines.
*   **Logging:** Implement configurable logging (controlled via `-v` flags) to provide insights into the application's execution flow, especially for debugging file parsing, config loading, and template rendering steps.
*   **Documentation:** Maintain a detailed `README.md` and potentially developer documentation outlining the architecture, modules, and how to run tests.

**10. Future Considerations (Optional Enhancements)**

*   **Interactive Mode:** A guided mode asking the user questions to build the prompt.
*   **Advanced Context Modes:** Summarization of context files before inclusion.
*   **Direct LLM Interaction:** Option to directly send the generated META_PROMPT to a configured LLM API and display/save the resulting TASK_PERFORMING_PROMPT.
*   **Prompt Library:** Functionality to save/load/manage generated META_PROMPTs and TASK_PERFORMING_PROMPTs.

These improved requirements leverage the best practices context, clarify ambiguities, add useful features (config file, templates, examples, verbosity, explicit copy), and emphasize reliability and maintainability.
