# get-lazy-with-llms-clinic
A toolkit and guide for using LLMs effectively on moderately complex tasks through better prompting.

## What this repository includes
1. Some theoretical elaborations on how to get better results from LLMs by creating better prompts
2. **Process documentation** of the task solving with LLMs process for several **example tasks**:
    - **QA**
        - [explain-abm-concept](): *manually find relevant context that should guide the LLM to better explain an ABM concept.*
        - [parameter-sweep-suggestion](): 
        
    - **code generation**
        - [abm-mesa-skeleton-generator](): *create a template/skeleton ABM using the Mesa framework and an example ABM*
        - [codemeta-generator]():
        - [dir-ingest](): *create a Python CLI to recursively merge the contents of all files in a directory into a single file for LLMs.*
        - [url-ingest](): *create a Python CLI to download and merge content from a list of URLs into a single file for LLMs*
        - [prompt-builder](./practice/08_build_promptbuilder_tool/README.md): *Create a Python CLI tool that helps users generate a META_PROMPT, which guides an LLM to produce a TASK_PERFORMING_PROMPT for completing a specific user-defined task.*
    
    - **documentation generation**
        - [abm-odd-documentation-generator]():
    
    - **evaluation by specified criteria**
        - [abm-odd-evaluator](): *generate an evaluation report for an ABM (given it's documentation and code) according to the ODD Protocol and ABM best practices from the "Understanding Complex Systems — Bruce Edmonds & Ruth Meyer (eds.), Simulating Social Complexity: A Handbook."*
3. **Task results (prompts and tools)** of the *task solving processes* above:
    - [Evaluation prompt for an ABM]()
    - [dir-ingest tool](./practice/06_build_diringest_tool/README.md)
    - [url-ingest tool]()
    - [prompt-builder tool](./practice/08_build_promptbuilder_tool/code/08_one_shot_solution_[aistudio.google]_[gemini-2.5-pro-preview-03-25]/README.md)
    - ...

## Recommendations on how to use this repository
- **5 minutes: read** 
    - use https://gitingest.com/ to convert this whole repo to a single text file (`REPO_CONTENT`). Ask an LLM (for example Gemini 2.5 Pro wiht aistudio.google) to summarize it for you: 
    ```yml
        "I am a <ROLE> (e.g., product manager, software architect, researcher). 
        
        Given the following repository content, create a clear, concise briefing document I can read in under 5 minutes. Focus on summarizing the purpose, key components, examples, theoretical resoning and any critical considerations. The tone should be informative and executive-friendly. Here's the content: 
        
        <REPO_CONTENT>"
    ```
- **15 minutes: read**
    1. Use the prompt above and read the LLM summary **(5 min)**. 
    2. Choose an example that is relevant to your work and follow it's *Task Solving Process* **(10 min)**
- **30 minutes: read + practice** 
    1. Clone this repo to your computer
    2. Continue with this README.md
    3. Choose an example that is relevant to your work and follow it's [task solving process](#what-this-repository-includes)
    4. Run the example tools
    5. Modify the provided prompts that were used to generate the tools
    6. Generate new tools

# General Developer Advice
1. If you are using Windows, **use WSL2 for development**. This is a virtual Linux environment on your Windows PC.
2. Whenever you can, **write your texts in markdown format (.md)** rather than in .docx, .pdf, etc...
3. **Use git**

# Recommended Tools
**Digest repo/directory into a single file for LLMs**
1. https://github.com/travisvn/gptree | use online: https://gptree.dev/
2. https://github.com/cyclotruc/gitingest | use online: https://gitingest.com/
3. https://github.com/yamadashy/repomix | use online: https://repomix.com/