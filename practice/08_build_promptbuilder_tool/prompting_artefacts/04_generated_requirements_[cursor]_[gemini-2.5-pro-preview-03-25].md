## TASK: Develop a Python Command-Line Tool: promptbuilder

### 1. Overview

Create a robust, maintainable, and user-friendly Python CLI tool named `promptbuilder`. This tool will assist users in constructing META_PROMPTs based on provided inputs (task description, context files/folders, instructions, etc.). These META_PROMPTs are designed to be fed into a Large Language Model (LLM) to generate TASK_PERFORMING_PROMPTs, which the user will then use with an LLM for their specific task.

**Core Goal:** Generate high-quality META_PROMPTs based on user inputs and best practices, ensuring the generated code is testable, maintainable, and reliable.

### 2. Functional Requirements

#### 2.1. Core Prompt Generation
    - Parse user inputs provided via CLI arguments.
    - Read and process context from specified local files or recursively from directories. Handle various common file types (e.g., .txt, .md, .py, .json) gracefully, potentially skipping binary or unreadable files with warnings.
    - Construct a META_PROMPT string based on the provided inputs and the best practices outlined in the "Context: Best Practices" section below.
    - If `--input`, `--output`, `--input_instructions`, or `--output_instructions` are provided (either as strings or file paths), the generated META_PROMPT MUST explicitly instruct the target LLM to use corresponding placeholders (e.g., `{{INPUT}}`, `{{OUTPUT}}`) in the final TASK_PERFORMING_PROMPT.
    - Structure the META_PROMPT clearly using delimiters (e.g., Markdown headers) to separate sections like Task Description, Context, Input/Output Specs, Instructions.

#### 2.2. Output Handling
    - Output the generated META_PROMPT to standard output (stdout) by default.
    - If the `--save_on_disk` argument specifies a valid file path, write the META_PROMPT to that file instead of stdout. Create parent directories if they don't exist.
    - After successful execution (either printing to stdout or saving to disk), attempt to copy the generated META_PROMPT to the system clipboard. Report success or failure of the clipboard operation.

### 3. Command-Line Interface (CLI) - `promptbuilder`

#### 3.1. Arguments
    - `--task` (Required): A string describing the core task for the final TASK_PERFORMING_PROMPT.
    - `--context` (Optional, Multiple Allowed): Path(s) to local files or directories. If a directory is provided, parse files recursively. Supports glob patterns (e.g., `src/**/*.py`).
    - `--instructions` (Optional): A string containing specific instructions *or* a path to a file containing these instructions for the META_PROMPT generation.
    - `--input` (Optional): A string describing the expected input for the TASK_PERFORMING_PROMPT *or* a path to a file containing this description.
    - `--output` (Optional): A string describing the desired output for the TASK_PERFORMING_PROMPT *or* a path to a file containing this description.
    - `--input_instructions` (Optional): A string detailing input formatting rules *or* a path to a file containing these details.
    - `--output_instructions` (Optional): A string detailing output formatting rules *or* a path to a file containing these details.
    - `--save_on_disk` (Optional): A file path where the generated META_PROMPT should be saved.
    - `--config` (Optional): Path to a custom configuration file. Defaults to `.promptbuilder` in the current directory or user home.
    - `--format` (Optional): Specify output format for the META_PROMPT (e.g., `text`, `markdown`, `json`). Default: `text`.
    - `--verbose`, `-v` (Optional): Enable detailed logging output for debugging.
    - `--version` (Optional): Display the tool's version and exit.
    - `--help`, `-h` (Optional): Display a helpful usage message and exit.

#### 3.2. Usability
    - Provide clear and concise help messages.
    - Use a library like `argparse` or `click` for robust argument parsing.
    - Display progress indicators (e.g., a simple spinner or message) for potentially long operations like recursive directory parsing.
    - Ensure error messages are user-friendly, informative, and suggest potential fixes.

### 4. Non-Functional Requirements

#### 4.1. Configuration
    - Implement hierarchical configuration loading: Command-line args > Project `.promptbuilder` > User `~/.promptbuilder` > Default settings.
    - Support a common configuration file format (e.g., YAML or TOML).
    - Allow users to configure default values for optional arguments and potentially define reusable prompt snippets or templates.

#### 4.2. Architecture & Maintainability
    - **Modularity:** Structure the codebase into logical, decoupled modules (e.g., `cli`, `config`, `parsing`, `generation`, `output`).
    - **SOLID Principles:** Adhere to SOLID design principles.
    - **Dependency Injection:** Utilize dependency injection where appropriate to facilitate testing and flexibility (e.g., inject filesystem access, clipboard access).
    - **Extensibility:** Design with potential future extensions in mind (e.g., supporting different placeholder syntaxes, output formats, or context processors).

#### 4.3. Testability & Reliability
    - **Test Framework:** Utilize a standard Python testing framework like `pytest`.
    - **Test Coverage:** Aim for high test coverage (e.g., > 80%) for core logic.
    - **Unit Tests:** Implement comprehensive unit tests for individual modules and functions, mocking external dependencies (filesystem, clipboard).
    - **Integration Tests:** Include integration tests verifying the end-to-end CLI functionality with sample inputs and expected outputs.
    - **Input Validation:** Rigorously validate all inputs (file existence, permissions, argument formats).
    - **Error Handling:** Implement robust error handling. Catch specific exceptions and provide informative error messages. Avoid bare `except:` clauses. Ensure graceful failure modes. Use specific exit codes for different error types.

#### 4.4. Code Quality
    - **Style Guide:** Adhere strictly to PEP 8 style guidelines. Use tools like `black` for formatting and `flake8` or `ruff` for linting.
    - **Type Hinting:** Use Python type hints for all function signatures and variables. Enforce type checking using `mypy`.
    - **Documentation:** Include clear docstrings (e.g., Google or NumPy style) for all modules, classes, and functions. Maintain a clear README.md with usage instructions and examples.

#### 4.5. Dependencies
    - Minimize external dependencies. Clearly document all dependencies in `requirements.txt` or `pyproject.toml`.
    - Use a dependency management tool (e.g., `pip`, `poetry`).

#### 4.6. Performance
    - Handle reading large files or large numbers of files efficiently. Consider streaming or chunking for large files if memory becomes an issue.
    - Implement basic caching if applicable (e.g., caching parsed file contents for short durations if the same context is used repeatedly, though likely low priority initially).

### 5. Context: Best Practices for Constructing META_PROMPTs
*(This section remains the same as in the original file, providing guidance for the META_PROMPT generation logic)*

## Best Practices for Constructing META_PROMPTs for promptbuilder

Meta prompting is a powerful technique where you create prompts that generate other prompts...
... (rest of the context and citations section from the original file) ...

---

This revised structure provides a much more detailed and actionable set of requirements for an LLM, emphasizing the crucial aspects of building a high-quality, maintainable, and testable software tool.