# Use LLMs to help you write a good prompt
But you need to help the LLM first: supply some `RELEVANT_CONTEXT` for your `TASK`.

## `RELEVANT_CONTEXT`
Examples of relevant context:
- domain-specific information
- guidelines
- examples
- documentation, or style guides
- etc.

## `TASK`
Every TASK has `INPUT` and `OUTPUT`. Both `INPUT` and `OUTPUT` might have certain formats or need to adhere to certain specifications, etc: `USER_INPUT_SPECIFICATION`, `USER_OUPUT_SPECIFICATION`. You might want to specify additional guidelines: `USER_CONSTRAINTS_AND_GUIDELINES`



## How to use the improved Meta-Prompt:

1.  The *user* fills in the placeholders:
    *   `{{TASK}}`: Their specific goal.
    *   `{{RELEVANT_CONTENT_FOR_TASK}}`: The contextual documents, guidelines, examples.
    *   `{{USER_INPUT_SPECIFICATION}}`: Description of the input for the *final* task.
    *   `{{USER_OUTPUT_SPECIFICATION}}`: Description of the desired output for the *final* task.
    *   `{{USER_CONSTRAINTS_AND_GUIDELINES}}`: Rules for the *final* task's output.
2.  This completed Meta-Prompt is given to LLM-1.
3.  LLM-1 follows the instructions within the Meta-Prompt (analyzing content, synthesizing instructions) and generates the Task-Performing Prompt.
4.  LLM-1 returns the generated Task-Performing Prompt within the specified JSON structure.
5.  The user takes the `generated_prompt` string and uses it (potentially filling in an `{{END_USER_INPUT_DATA}}` placeholder within it) with LLM-2 to accomplish the original `{{TASK}}`.

## Examples

- Example 1: Explaining an ABM Concept
- Example 2: Generating ABM Skeleton Code using Mesa Framework
- Example 3: Parameter Sweep Suggestion
- Example 4: Writing documentation for an ABM according to the ODD Protocol
- Example 5: Creating a codemeta.json file from model documentation
- Example 6: Create a Python CLI tool for building meta-prompts

| Example                         | `{{TASK}}`                                                                                                                               | `{{RELEVANT_CONTENT_FOR_TASK}}`                                                                                                                                                                                                                                                        | `{{USER_INPUT_SPECIFICATION}}`                                                                                                                                                                                              | `{{USER_OUTPUT_SPECIFICATION}}`                                                                                                                                                                                                                                                                                       | `{{USER_CONSTRAINTS_AND_GUIDELINES}}`                                                                                                                                                                                                                                                                                               |
| :------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Explain ABM Concept**      | Explain the concept of "emergence" in Agent-Based Modeling, using Schelling's Segregation Model as the primary example.                 | - Foundational ABM texts (e.g., Wilensky & Rand) defining emergence. <br> - Documentation/papers on Schelling's model (rules, outcomes). <br> - Principles of clear explanation for beginners.                                                                                      | Description: None needed beyond the prompt itself. The request is self-contained. <br> Placeholder name in generated prompt (if needed for clarity, though likely unused): `N/A`                                                      | Structure: Prose explanation. <br> Length: 2-3 paragraphs. <br> Style: Clear, concise, accessible to a beginner in ABM. <br> Content: Define emergence in ABM, describe Schelling agent rules & macro-pattern, explicitly link the two, emphasize emergent nature. <br> Format: Plain text or Markdown.                               | - Avoid overly technical jargon; explain if used. <br> - Focus on micro-level rules leading to macro-level patterns. <br> - Ensure factual accuracy based on standard ABM literature and Schelling model descriptions.                                                                                                     |
| **2. Generate ABM Code**        | Generate skeleton Python code for a `mesa.Agent` subclass representing an individual in an SIR model.                                    | - Mesa library documentation (`mesa.Agent` API, model structure). <br> - Python style guide (PEP 8). <br> - Type hinting conventions (Python `typing` module). <br> - Common SIR model agent attributes (ID, state) and logic flow (infection check, recovery check).                   | Description: None needed beyond the prompt itself. The requirements are fully specified. <br> Placeholder name in generated prompt: `N/A`                                                                                        | Structure: Single Python code block. <br> Language: Python 3. <br> Content: Define class `PersonAgent(mesa.Agent)`, include `__init__(unique_id, model, initial_state)`, store attributes, define `step()` method with commented placeholders for SIR logic. <br> Format: Markdown code block (```python ... ```). | - Code must be valid Python 3. <br> - Adhere strictly to PEP 8. <br> - Include type hints for method signatures and key attributes. <br> - Include comments indicating where `S->I` and `I->R` logic should go. <br> - Output *only* the code block, no surrounding text.                                                              |
| **3. Parameter Sweep Suggestion** | Suggest 3-5 key parameters for sensitivity analysis/parameter sweep for a described traffic ABM, with justifications.                  | - Principles of sensitivity analysis and parameter sweeps in simulation. <br> - Literature/examples of common parameters in traffic ABMs (e.g., density, speed, following distance, network properties). <br> - Typical goals of traffic simulation (e.g., analyzing congestion, travel time). | Description: Text describing the user's specific traffic ABM, including agents (cars), their rules (speed, following), environment (network), and key output metrics (e.g., avg travel time). <br> Placeholder name: `{{MODEL_DESCRIPTION}}` | Structure: Bulleted list. <br> Quantity: 3-5 items. <br> Content: Each item: Parameter name + 1-2 sentence justification linking parameter variation to expected impact on model outcomes (e.g., congestion, flow). <br> Style: Clear, concise, focused on simulation experiment design. <br> Format: Markdown list.                | - Justifications must explain *why* the parameter is important to vary for sensitivity. <br> - Parameters should be relevant to agent behavior, density, or environment. <br> - Suggestions must be based *only* on the provided `{{MODEL_DESCRIPTION}}`.                                                                          |
| **4. Write ODD Documentation**  | Generate documentation for an ABM according to the ODD (Overview, Design concepts, Details) protocol structure.                          | - The ODD protocol specification papers (Grimm et al., 2006, 2010, 2020). <br> - Examples of published ODD documentation. <br> - Principles of technical writing (clarity, completeness, structure).                                                                                 | Description: Detailed text describing the user's ABM, covering its purpose, entities, state variables, spatial/temporal scales, process overview, scheduling, design concepts (e.g., adaptation, sensing), initialization, inputs, submodels. <br> Placeholder name: `{{ABM_DETAILS}}` | Structure: Text document strictly following the ODD sections (Purpose, Entities/State Variables/Scales, Process Overview/Scheduling, Design Concepts, Initialization, Input Data, Submodels). <br> Style: Formal, objective, technical. <br> Format: Markdown, with clear headings for each ODD section.                                | - Adhere strictly to the structure and content requirements of the standard ODD protocol. <br> - Cover *all* required elements within each ODD section. <br> - Extract information *only* from the provided `{{ABM_DETAILS}}`. <br> - Be comprehensive and precise in the descriptions for each section.                               |
| **5. Create codemeta.json**     | Generate a `codemeta.json` file describing a software project (specifically an ABM) based on provided documentation or metadata details. | - The CodeMeta context/vocabulary/schema definition (JSON-LD). <br> - Examples of `codemeta.json` files for software projects. <br> - Best practices for software metadata (e.g., FAIR principles).                                                                                    | Description: Text containing information about the ABM software/model, such as: name, author(s), affiliations, description, keywords, license, code repository URL, version, dependencies, relevant publication DOI, contact point. <br> Placeholder name: `{{MODEL_DOCUMENTATION}}` | Structure: Single, valid JSON object. <br> Format: JSON conforming to the CodeMeta schema (using `@context": "https://doi.org/10.5063/schema/codemeta-2.0"`). <br> Content: Extract and populate relevant CodeMeta fields (e.g., `name`, `description`, `author`, `license`, `codeRepository`, `keywords`, `softwareRequirements`). | - Output *only* the JSON object, nothing else. <br> - Ensure the output is valid JSON. <br> - Adhere strictly to the CodeMeta vocabulary/schema. <br> - Extract information accurately from the provided `{{MODEL_DOCUMENTATION}}`. <br> - Use `null` or omit fields if the information is not available in the input text. |
| **6. Create Python CLI Tool** | Generate a prompt that instructs an LLM to create a Python command-line tool for building prompts (meta or otherwise). | - Description of the desired tool (its inputs: role, task, instructions, context, input_spec; its features: behavioral instructions, config file `.promptbuilder`, CLI structure `python promptbuilder --task ...`). <br> - Python `argparse` documentation. <br> - Python `configparser` (or `json`/`yaml`) documentation. <br> - Python style guide (PEP 8). <br> - Examples of Python CLI tools. <br> - Basic principles of prompt engineering. | Description: None needed beyond the prompt itself. The tool requirements are fully specified within the generated prompt (which itself is derived from the `{{RELEVANT_CONTENT_FOR_TASK}}`). <br> Placeholder name: `N/A` | Structure: Python code for the command-line tool. <br> Language: Python 3. <br> Content: A complete, runnable Python script implementing the specified CLI tool, including argument parsing (`argparse`), reading defaults from `.promptbuilder`, assembling a prompt string, handling behavioral directives. <br> Format: Markdown code block (```python ... ```). | - Code must be valid Python 3. <br> - Must use `argparse` for command-line interface as specified. <br> - Must implement logic to read defaults from a `.promptbuilder` config file (e.g., INI or JSON format). <br> - Handle basic error conditions (e.g., missing required arguments). <br> - Include comments explaining the code's structure and logic. <br> - Adhere to PEP 8 style guidelines. <br> - Output *only* the Python code block. |


### Use the example inputs to generate performing prompts
For Example 1:
```
python promptbuilder.py --task "Explain the concept of "emergence" in Agent-Based Modeling, using Schelling's Segregation Model as the primary example." 
                        --context "path/to/relevant-context.md"
```


# Notes

## What LLMs to use for prompt generation?
- gemini models with currently up to 1M token size context window
- notebooklm.google
- reasoning models

## Context preparation

### What format?
- use Markdown format: https://www.markdownguide.org/ LLMs understand it best. Markdown supports math formulas, tables, etc.
- use mermain diagrams: https://mermaid.js.org/

### How large can the context be?
- Theoretically pretty large. Gemini 1.5 Pro allows for 1M context window (this is larger than "War and Peace" by Tolstoy ~0.7M tokens).
- Try to keep it as small and specific to the task as possible.

### How to add information to context?
#### How to get the context information from websites, pdfs, journals, etc...?
- copy paste what you can copy paste. Pay attention to how the information is being pasted: the indentation might be off, or there might be artifacts.
- use tools like https://gitingest.com/ to merge the contents of whole github repos into a single markdown file
- use scripts like `scripts/dir_ingest.py` and `scripts/urls_ingest.py` to merge the content of all files in a directory or download the content of a list of urls into a single markdown file.
- use tools to convert pdfs and urls to markdown:
    - https://jina.ai/reader/
    - https://github.com/VikParuchuri/marker



# References
1. https://www.prompthub.us/blog/a-complete-guide-to-meta-prompting