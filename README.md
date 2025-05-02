# get-lazy-with-llms-clinic
This repository attempts at helping to understand how to use LLMs for Moderate and Difficult Tasks.

## Epistemology of Tasks
| **Task Type**                       | **Description**                                              | **Prompt Strategy**                                                                                               | **Example Task**                                      |
|------------------------------------|--------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------|
| `Easy Task` (Known Knowns)           | The task is straightforward and familiar                     | `"Do <TASK>"`                                                                                                      | "Sort this list alphabetically."                      |
| `Moderate Task` (Known Unknowns - X) | You know *what* you don’t know (e.g., best practices for X) | 1. `"What are best practices to do X?"` → *LLM returns `BEST_PRACTICES_TO_SOLVE_X`*<br>2. `"Use best <BEST_PRACTICES_TO_SOLVE_X>, do <TASK>"`           | "Write secure Python code to handle file uploads."     |
| `Difficult Task` (Unknown Unknowns)  | You don’t know what you don’t know| *Requires iterative prompting, clarification, decomposition, or exploration*                                       | "Design a prompt generation framework for multi-agent systems." |

## How to Solve Tasks with LLMs
![solving_tasks_with_llms.png](./assets/solving_tasks_with_llms.png)


## Axiom: To solve a complex task, we need (at least) a complex prompt.

While it might be enough to type a  few words into ChatGPT to solve a simple task, it is very benefitial to create complex structured prompts to solve more complicated tasks.

See [Effective LLM Prompting Strategies: From Simple to Complex](./theory/Effective%20LLM%20Prompting%20Strategies:%20From%20Simple%20to%20Complex.md)
for examples of simple vs complex prompts.


## Never write complex prompts by hand.
[Use LLMs to help you write a good prompt](./theory/Prompt%20Generation%20Engine.md)


## Methodology
1. Manually work through several example `TASKs`
2. Create a tool in python to help constructing the `META_PROMPT` (which will be fed to an LLM to get the `TASK_PERFORMER_PROMPT`).
3. The `TASK_PERFORMER_PROMPT` will be used to ask an LLM to solve our **difficult** `TASK`.


This repository can be cloned into your existing project and built upon.
`my-docs` - documentation of frameworks or APIs you download from the internet
`my-prompts` - prompt templates
`my-scripts` - scripts that help you gather context for LLM prompts

# my-scripts
## dir-ingest
Merge file content of a directory into a single file for the LLM.

```bash
# Example: 

# - digest current directory into a JSON file `digest.json` (preserves file/folder structure)
# - exclude *.json,*.log and *.yaml files 
# - exclude files larger than 300KB

python my-scripts/dir-digest/dir-digest.py . --output digest.json --exclude "*.json,*.log,*.yaml" --max-size 300
```

[How to use.](./my-scripts/dir-digest/README.md)

## urls-ingest
Merge content from a list of URLs into a single file


# General Developer Advice
1. If you are using Windows, **use WSL2 for development**. This is a virtual Linux environment on your Windows PC.
2. Whenever you can, **write your texts in markdown format (.md)** rather than in .docx, .pdf, etc...
3. **Use git**

# Recommended Tools
## Digest repo/directory into a single file for LLM
1. https://github.com/travisvn/gptree - https://gptree.dev/
2. https://github.com/cyclotruc/gitingest - https://gitingest.com/
3. https://github.com/yamadashy/repomix - https://repomix.com/