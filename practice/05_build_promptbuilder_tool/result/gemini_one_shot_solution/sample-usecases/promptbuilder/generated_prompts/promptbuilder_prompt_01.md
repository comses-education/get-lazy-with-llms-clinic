
**Objective:** Generate a high-quality TASK_PERFORMING_PROMPT based on the specifications below. This prompt will be used by a human user to instruct another LLM to perform a specific task.

**Your Role:** You are an expert prompt engineer. Your goal is to create a clear, concise, effective, and robust TASK_PERFORMING_PROMPT.

**Core Task for the Final LLM:**
The ultimate task the final LLM needs to perform is:
Create a python command line tool which helps the user to build a META_PROMPT. The user will feed the META_PROMPT to an LLM of his choice. The generated response from the META_PROMPT should be a TASK_PERFORMING_PROMPT that the user will use to feed to an LLM of his choice to perform his TASK.


Construct the TASK_PERFORMING_PROMPT adhering to the following structure and including the specified elements:

**1. Clear Directive:** Start with a clear and direct instruction summarizing the main goal for the final LLM.

**2. Persona (Optional but Recommended):** If appropriate for the task, instruct the final LLM to adopt a specific persona (e.g., "Act as a helpful coding assistant," "You are a creative writer specializing in fantasy.").

**3. Context (If Provided):**
The final prompt should inform the LLM that the following context (files and their content) is available to assist with the task. The content is provided below, delineated by file path markers. Instruct the LLM to use this context when generating its response.

**Provided Context Content:**

--- START CONTEXT FILE: /home/asuworks/work/repos/github.com/comses-education/get-lazy-with-llms-clinic/my-prompts/6_build_a_python_cli_tool/code/05_one_shot_solution_[aistudio.google]_[gemini-2.5-pro-preview-03-25]/test_docs/promptbuilder/03_context.md ---
# Best Practices for Constructing META_PROMPTs for promptbuilder

Meta prompting is a powerful technique where you create prompts that generate other prompts. In your case, you're building a command-line tool that helps users create META_PROMPTs which will then generate TASK_PERFORMING_PROMPTs. Here's a comprehensive guide on best practices for constructing effective META_PROMPTs.

## Understanding Meta Prompting Fundamentals

Meta prompting is an advanced technique that focuses on the structural and syntactical aspects of problems rather than specific content details[10]. It's essentially using an LLM to help create, adjust, or improve prompts that will later be used for specific tasks[16].

### Key Benefits of Meta Prompting

- Overcomes the "blank page problem" in prompt engineering[5]
- Produces more focused and refined prompts[16]
- Creates structured frameworks that can be applied across various domains[10]
- Allows dynamic adaptation based on feedback[5]
- Helps tailor prompts to specific tones, formats, or audiences[16]

## Structuring Your META_PROMPT

### 1. Clear Directive and Purpose

Begin with a clear statement about what the META_PROMPT is meant to accomplish:

```
You will create a prompt that helps the user perform the following task: [--task]. 
The prompt you create should be comprehensive, clear, and optimized for an LLM to execute effectively.
```

This establishes the meta-level nature of the interaction and sets clear expectations[1][4].

### 2. Follow a Hierarchical Structure

Organize your META_PROMPT in a logical progression:

1. Directive (what the LLM should do)
2. Task description (from `--task`)
3. Context information (from `--context`)
4. Input/output specifications
5. Special instructions or constraints

This structured approach helps the LLM organize its thinking process[11].

### 3. Use Delimiters for Different Sections

Separate different parts of your META_PROMPT with clear delimiters:

```
### TASK DESCRIPTION ###
[task description here]

### CONTEXT ###
[context information here]

### INPUT SPECIFICATIONS ###
[input details here]
```

This improves clarity and prevents different sections from bleeding into each other[1][11].

## Providing Clear Instructions

### 1. Be Specific and Descriptive

Instead of:
```
Create a prompt for summarizing text.
```

Use:
```
Create a detailed prompt that will instruct an LLM to summarize technical documentation while preserving key technical terms, maintaining the original structure, and highlighting actionable items.
```

Specificity leads to better results[1][11][13].

### 2. Create a Role and Scenario

Frame the task within a specific role and scenario:

```
The prompt you create should position the LLM as an expert technical writer with experience in translating complex concepts into accessible language.
```

This gives context and purpose to the generated prompt[11].

### 3. Specify Format Requirements

Clearly indicate how the TASK_PERFORMING_PROMPT should be formatted:

```
The prompt you create should include:
1. A clear introduction of what the LLM will do
2. Step-by-step instructions for processing the input
3. Guidelines for formatting the output
4. Examples of good responses (if applicable)
```

This ensures the generated prompt has all necessary components[1][11].

## Handling Input and Context

### 1. Context Processing Instructions

When using the `--context` parameter, provide clear instructions on how to use the context:

```
I am providing context from the following files: [list of files]. Your prompt should instruct the LLM to process this information by:
1. Identifying key components and relationships
2. Extracting relevant terminology
3. Understanding the overall structure
```

This helps the META_PROMPT correctly incorporate the context into the generated TASK_PERFORMING_PROMPT[13].

### 2. Placeholder Implementation

When input/output parameters are specified, explicitly instruct the META_PROMPT to create placeholders:

```
The prompt you generate must include the following placeholder: {{INPUT}}
The user will replace this placeholder with their specific input when using the prompt.
```

This ensures the generated prompt has proper placeholders for user inputs and expected outputs[11].

### 3. Sample Data Usage

Provide guidance on how to use sample data:

```
Include an example of how the prompt should handle this sample input: [sample]
Demonstrate the expected output format using this example: [example output]
```

Examples clarify expectations and improve prompt quality[1].

## Advanced Techniques

### 1. Task Decomposition

For complex tasks, instruct the META_PROMPT to break down the task:

```
The prompt you create should break down the task of [complex task] into the following sub-tasks:
1. Initial analysis of input
2. Intermediate processing steps
3. Final output generation
```

Breaking down complex tasks improves prompt effectiveness[13].

### 2. Encourage Multi-perspective Thinking

Guide the META_PROMPT to consider different approaches:

```
Your prompt should encourage the LLM to consider multiple perspectives when approaching the task, such as:
- Technical feasibility
- User experience
- Ethical implications
```

This creates more robust TASK_PERFORMING_PROMPTs[11].

### 3. Error Handling and Edge Cases

Instruct the META_PROMPT to include error handling:

```
The prompt you create should include instructions for handling these potential edge cases:
- Missing or incomplete input
- Ambiguous requirements
- Conflicting criteria
```

This anticipates problems and makes the final prompt more robust[4].

## Implementation Example for promptbuilder

Here's how these practices come together in a sample META_PROMPT for your tool:

```
Your task is to create a comprehensive, effective prompt that will enable an LLM to {{TASK_DESCRIPTION}}.

### CONTEXT INFORMATION ###
The prompt will be used in the following context: {{CONTEXT_SUMMARY}}

### INPUT SPECIFICATIONS ###
The prompt should instruct the LLM to accept input in the following format:
{{INPUT_DESCRIPTION}}

### OUTPUT SPECIFICATIONS ###
The prompt should instruct the LLM to produce output with these characteristics:
{{OUTPUT_DESCRIPTION}}

### PROMPT REQUIREMENTS ###
The prompt you create must:
1. Begin with a clear role and task definition
2. Include specific instructions for processing the input
3. Provide detailed guidance on generating the required output
4. Include placeholders marked with double curly braces for variable inputs
5. Consider edge cases and provide error handling instructions

Return only the complete, ready-to-use prompt without explanations or meta-commentary.
```

## Testing and Iteration

Always encourage users to test their META_PROMPTs and iterate based on the quality of the TASK_PERFORMING_PROMPTs generated[13][5].

A good approach is to include a feedback loop in your tool that allows users to refine their META_PROMPTs based on the results they get.

By following these best practices, your `promptbuilder` tool will help users create effective META_PROMPTs that generate high-quality, task-specific prompts for their needs.

## Conclusion

Creating effective META_PROMPTs requires clear structure, specific instructions, and thoughtful consideration of how the generated prompt will be used. By implementing these best practices in your `promptbuilder` tool, you'll enable users to create powerful, flexible prompts that take full advantage of LLMs' capabilities.

Remember that different models may respond differently to the same META_PROMPT, so it's important to test with the specific models your users will employ[15].

Citations:
[1] https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api
[2] https://www.promptingguide.ai/techniques/prompt_chaining
[3] https://www.reddit.com/r/PromptEngineering/comments/1d3obpg/16_prompt_patterns_templates/
[4] https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/system-message
[5] https://www.prompthub.us/blog/a-complete-guide-to-meta-prompting
[6] https://www.reddit.com/r/LocalLLaMA/comments/1gsss8i/meta_prompts_are_here/
[7] https://github.com/Eladlev/AutoPrompt
[8] https://www.reddit.com/r/PromptEngineering/comments/1dk1zmi/introducing_promptml_cli_write_and_execute/
[9] https://www.digitalocean.com/resources/articles/prompt-engineering-best-practices
[10] https://www.promptingguide.ai/techniques/meta-prompting
[11] https://www.prompthub.us/blog/10-best-practices-for-prompt-engineering-with-any-model
[12] https://www.reddit.com/r/PromptDesign/comments/1fvg2ww/meta_prompting_methods_and_templates/
[13] https://www.promptingguide.ai/introduction/tips
[14] https://github.com/promptware/metaprompt
[15] https://cloud.google.com/blog/products/application-development/five-best-practices-for-prompt-engineering
[16] https://www.godofprompt.ai/blog/guide-for-meta-prompting
[17] https://www.ibm.com/docs/en/rational-change/5.3.0?topic=queries-using-prompting
[18] https://www.reddit.com/r/PromptEngineering/comments/141fwmi/awesome_list_of_prompt_engineering_techniques/
[19] https://www.prompthub.us/blog/prompt-chaining-guide
[20] https://mirascope.com/blog/langchain-prompt-template/
[21] https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/advanced-prompt-engineering
[22] https://www.linkedin.com/pulse/crafting-ai-prompt-templates-reusable-engineering-tk--e0w8c
[23] https://platform.openai.com/docs/guides/prompt-engineering
[24] https://platform.openai.com/docs/guides/prompt-generation
[25] https://python.langchain.com/docs/concepts/prompt_templates/
[26] https://microsoft.github.io/Workshop-Interact-with-OpenAI-models/Part-2-labs/System-Message/
[27] https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-placeholders.html
[28] https://dev.to/get_pieces/10-prompt-engineering-best-practices-23dk
[29] https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-design-strategies
[30] https://github.com/meta-prompting/meta-prompting
[31] https://www.reddit.com/r/ChatGPT/comments/144nrnf/i_built_an_opensource_tool_to_autogenerate_prompts/
[32] https://github.com/mufeedvh/code2prompt
[33] https://www.prompthub.us/blog/10-best-practices-for-prompt-engineering-with-any-model
[34] https://cookbook.openai.com/examples/enhance_your_prompts_with_meta_prompting
[35] https://www.youtube.com/watch?v=TKwuJtohaxk
[36] https://datascientest.com/en/all-about-automated-prompt-engineering
[37] https://github.com/c-bata/go-prompt
[38] https://community.openai.com/t/a-guide-to-crafting-effective-prompts-for-diverse-applications/493914
[39] https://www.llama.com/docs/model-cards-and-prompt-formats/meta-code-llama/

--- END CONTEXT FILE: /home/asuworks/work/repos/github.com/comses-education/get-lazy-with-llms-clinic/my-prompts/6_build_a_python_cli_tool/code/05_one_shot_solution_[aistudio.google]_[gemini-2.5-pro-preview-03-25]/test_docs/promptbuilder/03_context.md ---


--- START CONTEXT FILE: /home/asuworks/work/repos/github.com/comses-education/get-lazy-with-llms-clinic/my-prompts/6_build_a_python_cli_tool/code/05_one_shot_solution_[aistudio.google]_[gemini-2.5-pro-preview-03-25]/test_docs/promptbuilder/05_improved_requirements.md ---
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

--- END CONTEXT FILE: /home/asuworks/work/repos/github.com/comses-education/get-lazy-with-llms-clinic/my-prompts/6_build_a_python_cli_tool/code/05_one_shot_solution_[aistudio.google]_[gemini-2.5-pro-preview-03-25]/test_docs/promptbuilder/05_improved_requirements.md ---


--- START CONTEXT FILE: /home/asuworks/work/repos/github.com/comses-education/get-lazy-with-llms-clinic/my-prompts/6_build_a_python_cli_tool/code/05_one_shot_solution_[aistudio.google]_[gemini-2.5-pro-preview-03-25]/test_docs/promptbuilder/01_task.md ---
Create a python command line tool which helps the user to build a META_PROMPT.
The user will feed the META_PROMPT to an LLM of his choice. The generated response from the META_PROMPT should be a TASK_PERFORMING_PROMPT that the user will use to feed to an LLM of his choice to perform his TASK.

--- END CONTEXT FILE: /home/asuworks/work/repos/github.com/comses-education/get-lazy-with-llms-clinic/my-prompts/6_build_a_python_cli_tool/code/05_one_shot_solution_[aistudio.google]_[gemini-2.5-pro-preview-03-25]/test_docs/promptbuilder/01_task.md ---


--- START CONTEXT FILE: /home/asuworks/work/repos/github.com/comses-education/get-lazy-with-llms-clinic/my-prompts/6_build_a_python_cli_tool/code/05_one_shot_solution_[aistudio.google]_[gemini-2.5-pro-preview-03-25]/test_docs/promptbuilder/06_instructions.md ---

--- END CONTEXT FILE: /home/asuworks/work/repos/github.com/comses-education/get-lazy-with-llms-clinic/my-prompts/6_build_a_python_cli_tool/code/05_one_shot_solution_[aistudio.google]_[gemini-2.5-pro-preview-03-25]/test_docs/promptbuilder/06_instructions.md ---





**4. Input Specification (If Provided):**

**5. Output Specification (If Provided):**

**6. Examples (If Provided):**

**7. Constraints & Tone:** Ensure the final prompt clearly states any constraints, desired tone, or negative constraints (what the LLM *should not* do).

**8. Final Check:** The generated TASK_PERFORMING_PROMPT should be self-contained, unambiguous, and directly usable by a human interacting with an LLM.



Now, based on all the above instructions, generate the TASK_PERFORMING_PROMPT.