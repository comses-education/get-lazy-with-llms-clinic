# Use LLMs to Help You Write a Better Prompt 🤝
> **Never write the prompt yourself.** 
> The LLM has seen a HUGE amount of questions and answers from the internet. It knows how to formulate prompts. Give the LLM your TASK and ask to write a better prompt for you. Supply additional instructions or context if needed. 
 
**We will call the prompt that generates a better prompt for your task - the `META_PROMPT` and the resulting, generated prompt the `TASK_PERFORMING_PROMPT`.**

There are 2 types of tasks:
- direct tasks that don't require any input except for the task itself (Ex. *Explain the concept of "landscape evolution modeling" (LEM) in earth surface science.*)
- for tasks that are based on some input (Ex: *"Given the code and documentation of an agent-based model, evaluate its quality according to the ODD protocol."* - INPUT: code and documentation of an agent-based model)

## How to use the `META_PROMPT`
1. Create the `META_PROMPT`
```
    """
    Generate a high-quality TASK_PERFORMING_PROMPT for TASK based on the CONTEXT below. 
    This prompt will be used by a human user or another system to instruct an LLM to perform a specific task.
    
    TASK: <TASK>
    CONTEXT: <CONTEXT>    
    """
```
1. Prompt the LLM with the `META_PROMPT`. The response will be your `TASK_PERFORMING_PROMPT`
2. If your TASK requires input, fill the `{{INPUT}}` placeholders in the `TASK_PERFORMING_PROMPT`
3. Prompt the LLM with the `TASK_PERFORMING_PROMPT`


## Example Tasks with Meta-Prompt Inputs

| Example                         | `{{TASK}}`                                                                                                                               | `{{RELEVANT_CONTEXT}}`                                                                                                                                                                                                                                                        | `{{INPUT_SPECIFICATION}}`                                                                                                                                                                                              | `{{OUTPUT_SPECIFICATION}}`                                                                                                                                                                                                                                                                                       | `{{INSTRUCTIONS}}`                                                                                                                                                                                                                                                                                               |
| :------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Explain Earth Surface Modeling Concept for a 5-Year-Old** | Explain the concept of "landscape evolution modeling" (LEM) in earth surface science, including its principles, applications, and how it represents terrain surfaces for a 5-Year-Old. |<br>- Foundational texts on landscape evolution modeling. <br>- Literature on digital terrain representation methods. <br>- Papers describing applications of LEMs in geomorphology. <br>- Principles of clear scientific explanation for non-specialists. |  None needed beyond the prompt itself. The requirements are fully specified. | Structure: Prose explanation.  Length: 2-3 paragraphs.  Style: Clear, concise, accessible to a beginner in earth surface modeling.  Content: Define LEMs, explain key components (grid representation, time scales, process laws), describe common applications, highlight importance in geomorphology.  Format: Plain text or Markdown. | - Avoid technical jargon without explanation. <br>- Focus on fundamental principles and broad understanding rather than mathematical details. <br>- Ensure factual accuracy based on standard geomorphological literature. <br>- Include mention of both process representation and terrain representation aspects. |
| **2. Generate Landlab Overland Flow Model** | Generate a Python script that creates a simple overland flow simulation using Landlab's OverlandFlow component. | <br>- Landlab documentation and API reference. <br>- Overland Flow Component user guide. | <br>- Python style guide (PEP 8). <br>- Basic principles of hydrological modeling. <br>- Examples of Landlab model implementations.  | Structure: Complete Python script.  Language: Python 3.  Content: Import statements, grid creation, parameter setup, OverlandFlow component initialization, time loop implementation, data visualization code.  Format: Markdown code block (```python ...```) |
| **3. Containerize Earth Surface Model** | Create a Dockerfile and associated configuration files to containerize a Python-based earth surface modeling application. | <br>- Docker best practices. <br>- Python containerization examples. <br>- Requirements for scientific/geospatial packages (GDAL, NumPy, etc.). <br>- Docker multi-stage build patterns. <br>- Deployment considerations for scientific applications. | | Structure: Complete Dockerfile and any additional necessary files (docker-compose.yml, requirements.txt).  Content: Base image selection, dependency installation, code copying, environment setup, entrypoint configuration.  Format: Plain text or Markdown code blocks for each file. | - Follow Docker best practices (minimize layers, reduce image size). <br>- Ensure reproducibility of the environment. <br>- Address installation of complex geospatial dependencies. <br>- Consider data volume mounting for model inputs/outputs. <br>- Include clear documentation on how to build and run the container. <br>- Security considerations for production deployment. |
| **4. Create Python CLI Tool** | Generate a prompt that instructs an LLM to create a Python command-line tool for building prompts (meta or otherwise). <br>- Description of the desired tool (its inputs: role, task, instructions, context, input_spec; its features: behavioral instructions, config file `.promptbuilder`, CLI structure `python promptbuilder --task . .`). | <br>- Python `argparse` documentation. <br>- Python `configparser` (or `json`/`yaml`) documentation. <br>- Python style guide (PEP 8). <br>- Examples of Python CLI tools. <br>- Basic principles of prompt engineering. | | Structure: Python code for the command-line tool.  Language: Python 3.  Content: A complete, runnable Python script implementing the specified CLI tool, including argument parsing (`argparse`), reading defaults from `.promptbuilder`, assembling a prompt string, handling behavioral directives.  Format: Markdown code block (```python ... ```) |

## Usage Examples

For Example 1:
```
python promptbuilder.py --task "Explain the concept of landscape evolution modeling in earth surface science" 
                        --context "path/to/geomorphology-references.md"
```

For Example 2:
```
python promptbuilder.py --task "Generate a Python script for simulating overland flow using Landlab" 
                        --context "path/to/landlab-documentation.md"
```

For Example 3:
```
python promptbuilder.py --task "Create a Dockerfile for my earth surface model" 
                        --context "path/to/model-requirements.md"
                        --input "model_details.txt"
```

For Example 4:
```
python promptbuilder.py --task "Create a CLI tool for building prompts" 
                        --context "path/to/promptengineering-guide.md"
```


# References
1. https://www.prompthub.us/blog/a-complete-guide-to-meta-prompting
