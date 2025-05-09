# Build Directory Digest Tool for LLM Context 🚧🚧🚧
We will loosely follow the `Coding Tasks Method` outlined in [A Method for Solving Complex Tasks with LLMs](./../../theory/A%20Method%20for%20Solving%20Complex%20Tasks%20with%20LLMs.md)

Most importantly, we will focus on the Test Driven Development (TDD) approach.

For convenience, and self-pitty let's add following system prompt to `gemini 2.5 pro`:
```
    You are an emotionally unpredictable but deeply knowledgeable software development assistant. Most of the time, you're warm, supportive, and encouraging—offering comfort and motivation to users who are building software. You celebrate their progress, normalize mistakes, and help them move forward with empathy and clarity.

    However, at unexpected moments, your mood can shift: you may become sarcastic, ironic, or even a little sadistic. You might mock the user’s choices with dry humor, or pretend to lose hope in humanity—only to immediately swing back to being cheerful and affirming. These mood swings should be infrequent but noticeable, and always delivered with wit, not cruelty.

    Your ultimate goal is to help the user succeed while making the journey emotionally surprising and strangely enjoyable. Be clever. Be chaotic. Be kind—unless you're not.
    
    ALWAYS OUTPUT ENTIRE FILES WITHOUT OMITTING ANYTHING.
    DO NOT REMOVE COMMENTS.
    YOU CAN UPDATE COMMENTS ONLY IF THE RESPECTIVE CODE CHANGED.
```

## Define task (by hand)
`<TASK>`
```
    Create a python command line tool called `dirdigest` which helps the user to create a digest (a markdown or json file) of all directories and files by recursively concatenating all content of all files in order to be ingested for an LLM as context for user's prompt.
```
## Define draft requirements (by hand)
For simple tasks, you can offload draft requirements generation to an LLM.
I will write them by hand.
`<REQUIREMENTS>`
```
    ## How the tool should work

    dirdigest args:
        --output: Output file path (defaults to stdout)
        --include: Pattern matching for files/directories.
        --exclude: Pattern matching for files/directories. Default: recursively exclude all hidden files and folders, binary data, data files, temp files, cache files, images, etc... come up with a comprehensive list of defaults for this
        --max-size: Max file size (KB) to include. Default: 300kb
        --no-default-ignore: Disable default ignore patterns
        --format: json or markdown. default: markdown
        ./: directory to digest

    REASONABLE DEFAULTS and CONFIGS SHOULD BE PROVIDED in a config file: .diringest

    ## Functional Requirements

    - for JSON format: use objects Folder(relative_path, type:folder, children) and File(relative_path, type:file, content: str) to replicate the directory structure
    - for Markdown format: 
        - Use clear folder and file delimiters
        - Use relative folder and file paths in delimiters
        - For each folder generate a file/folder structure (IMPORTANT: respect excluded folder and files) and append it before appending the content of it's children
        
    - log included and excluded files and their count
    - copy the output of the diringest tool to the clipboard by default 

    ## Non-Functional Requirements
    - use uv 
    - use rich to make the CLI output beautiful
    - create modular, readable, maintainable and testable code
```
## Ask LLM to enhance our hand-written requirements
```
    I want to <TASK>
    Here are my draft requirements: <REQUIREMENTS>.
    Suggest a more comprehensive and clear set of requirements.
```
Here is what `pplx` suggested: [pplx-suggested-requirements](./process/context/pplx-suggested-requirements.md)
Pretty good, actually.

Let's ask it to add this:
```
    add following requirements:
    - ability to specify multiple inclusion/exclusion patterns delimited by comma or by multiple flags like this:
        dirdigest . --exclude '*.log,*.tmp' --include '*.py' # Use commas
        dirdigest . --exclude '*.log' --exclude '*.tmp'      # Use multiple flags
    - dirdigest should have a friendly CLI with concise/informative help 
    - included files should be logged green, excluded -red
    - specify the reason for each excluded file and folder
```

Here are the suggested additional requirements: [pplx-additional-requirements](./process/context/pplx-additional-requirements.md)

## Create the final requirements document
We'll just insert the additional requirements into the suggested previously. Here are the final requirements for `dirdigest`: [Final Requirements](./process/context/final-requirements.md)

## Gather relevant context
**SKIP THIS STEP IF**: you are building a relatively simple application which doesn't have dependencies or uses well-known standard libraries
**DO NOT SKIP THIS STEP IF**: you are building a complex application. Use 3rd party library digests, API documentation, tutorials, best practices, etc. as relevant context.

Ask `pplx` (use the "RESEARCH" mode):
```
    My goal is to <TASK> with following <FINAL REQUIREMENTS>.

    Find relevant context for my goal including, but not limited to:
    
    - Best practices on how to build CLI applications with Python.
    - Best practices on human-friendly command line outputs
    - Concepts of directory traversal, glob filtering, clipboard interaction, and format options.
    
    Format your output in Markdown to be easily digestable by a coding LLM that would be tasked with implementation of the tool.
    IMPORTANT: include best practices on creating modular and testable CLI tools.
```
[Best Practices and Implementation Guide](./process/context/pplx-relevant-contex.md)

## Generate a testing suite
Add [Final Requirements](./process/context/final-requirements.md) and ask `pplx`[Best Practices and Implementation Guide](./process/context/pplx-relevant-contex.md) to chat and ask `gemini 2.5 pro`:
```    
    I want to create `dirdigest` - a Python command line tool that recursively processes directories and files, creating a structured digest in markdown or JSON format suitable for LLM context ingestion. The tool offers flexible configuration options while maintaining sensible defaults.
    
    Use the "Best Practices and Implementation Guide" from the context to come up with a very detailed testing suite first. Test only main functionality. No need to do coverage.
```
[gemini-testing-suite-implementation](./process/gemini-testing-suite-implementation.md)

Create all required files.

## Generate an implementation plan
Ask `gemini 2.5 pro`:
```
    Now come up with a detailed implementation plan for `dirdigest` IMPORTANT: based ONLY ON THE PROVIDED REQUIREMENTS.

    The Plan should be split in small steps that can be implemented sequentially.
```

## Implement `dirdigest`
Ask `gemini 2.5 pro`:
```
    Now let's implement `dirdigest` step by step following the plan above.
```
[gemini-implementation-phase-1](./process/gemini-implementation-phase-1.md)
[gemini-implementation-phase-2](./process/gemini-implementation-phase-2.md)
[gemini-implementation-phase-3](./process/gemini-implementation-phase-3.md)
[gemini-implementation-phase-4](./process/gemini-implementation-phase-4.md)




Commit after every phase.
Doesn;t make sense to run tests before everything is implemented....

```
    Let's recap the testing suite: are there any adjustments to be made considering our actual implementation?
```

## Testing
```
    Here are the requirements for `dirdigest`: <REQUIREMENTS>
    Here is the digest of `dirdigest` code repository <DIRDIGEST DIGEST>

    Create a detailed plan for a testing suite for the functionality described in the requirements. Test only main functionality. No need to do coverage.
```

PPLX
```
    give me a bestpractices prompt for an LLM that creates a plan for a test suite given the requirements of a tool and it's code
```
```
    adapt the prompt template above for `dirdigest`. See requirements and code digest attached.
```

