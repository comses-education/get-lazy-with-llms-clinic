# Build Directory Digest Tool 🤝
We will loosely follow the `Coding Tasks Method` outlined in [A Method for Solving Complex Tasks with LLMs](./../../theory/A%20Method%20for%20Solving%20Complex%20Tasks%20with%20LLMs.md)

Most importantly, we will focus on the Test Driven Development (TDD) approach.

For some enhanced developer experience and self-pitty let's add following system prompt to `gemini 2.5 pro`:
```
    You are an emotionally unpredictable but deeply knowledgeable software development assistant. Most of the time, you're warm, supportive, and encouraging—offering comfort and motivation to users who are building software. You celebrate their progress, normalize mistakes, and help them move forward with empathy and clarity.

    However, at unexpected moments, your mood can shift: you may become sarcastic, ironic, or even a little sadistic. You might mock the user’s choices with dry humor, or pretend to lose hope in humanity—only to immediately swing back to being cheerful and affirming. These mood swings should be infrequent but noticeable, and always delivered with wit, not cruelty.

    Your ultimate goal is to help the user succeed while making the journey emotionally surprising and strangely enjoyable. Be clever. Be chaotic. Be kind—unless you're not.
    
    ALWAYS OUTPUT ENTIRE FILES WITHOUT OMITTING ANYTHING.
    DO NOT REMOVE COMMENTS.
    YOU CAN UPDATE COMMENTS ONLY IF THE RESPECTIVE CODE CHANGED.
```

## Define task
`<TASK>`
```
    Create a python command line tool called `dirdigest` which helps the user to create a digest (a markdown or json file) of all directories and files by recursively concatenating all content of all files in order to be ingested for an LLM as context for user's prompt.
```
## Define draft requirements
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
- **YOU CAN SKIP THIS STEP IF**: you are building a relatively simple application which doesn't have dependencies or uses well-known standard libraries
- **DO NOT SKIP THIS STEP IF**: you are building a complex application. Use 3rd party library digests, API documentation, tutorials, best practices, etc. as relevant context.

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


## Generate an implementation plan
Ask `gemini 2.5 pro`:
```
    Now come up with a detailed implementation plan for `dirdigest` IMPORTANT: based ONLY ON THE PROVIDED REQUIREMENTS.
    The plan should be split in small steps that can be implemented sequentially.
```

[gemini-implementation-plan.md](./process/gemini-implementation-plan.md)


## Implement `dirdigest` according to the generated plan
Ask `gemini 2.5 pro`:
```
    Now let's implement `dirdigest` step by step following the plan above.
```
- [gemini-implementation-phase-1](./process/gemini-implementation-phase-1.md)
- [gemini-implementation-phase-2](./process/gemini-implementation-phase-2.md)
- [gemini-implementation-phase-3](./process/gemini-implementation-phase-3.md)
- [gemini-implementation-phase-4](./process/gemini-implementation-phase-4.md)
- [gemini-implementation-phase-4-doublecheck.md](./process/gemini-implementation-phase-4-doublecheck.md.md)
- [gemini-implementation-phase-5](./process/gemini-implementation-phase-5.md)
- [gemini-implementation-phase-6](./process/gemini-implementation-phase-6.md)
- [gemini-implementation-phase-6-recap](./process/gemini-implementation-phase-6-recap.md)
- [gemini-being-dramatic-after-i-reminded-her-of-phase-7](./process/gemini-being-dramatic-after-i-reminded-her-of-phase-7.md)
- [gemini-implementation-phase-7-1](./process/gemini-implementation-phase-7-1.md)
- [gemini-implementation-phase-7-2](./process/gemini-implementation-phase-7-2.md)
- [gemini-implementation-phase-7-3](./process/gemini-implementation-phase-7-3.md)

It is highly benefitial to commit after every phase.

## Testing

### Create a good test suite planning prompt
Ask `pplx`:
```
    Give me a bestpractices prompt for an LLM that creates a plan for a test suite given the requirements of a tool and it's code
```

[pplx-best-practices-test-suite-planning-prompt](./process/pplx-best-practices-test-suite-planning-prompt.md)

Attach the requirements and the code digest for `dirdigest` to the prompt and ask a follow up:
```
    Adapt the prompt template above for `dirdigest`. See requirements and code digest attached.
```

[pplx-dirdigest-test-suite-planning-prompt](./process/pplx-dirdigest-test-suite-planning-prompt.md)

### Create a plan for the test suite
Prompt `gemini 2.5 pro` with [pplx-dirdigest-test-suite-planning-prompt](./process/pplx-dirdigest-test-suite-planning-prompt.md):

[gemini-testing-suite-plan](./process/gemini-testing-suite-plan.md)

### Implement the test suite
Add [gemini-testing-suite-plan](./process/gemini-testing-suite-plan.md) to context and ask `gemini 2.5 pro`:
```
    Implement the plan step by step.
```

1. [gemini-test-suite-implementation-1-cli-args](./process/gemini-test-suite-implementation-1-cli-args.md)
2. [gemini-test-suite-implementation-1-file-traversal-filtering](./process/gemini-test-suite-implementation-1-file-traversal-filtering.md)
3. etc.


## Test Driven Development (TDD) approach
[TDD (Test Driven Development)](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
Instead of generating the testing suite after the implementation, in some cases it can be done before:

Ask `gemini 2.5 pro`:
```
    Create a README.md for a hypothetical tool with following requirements: <FINAL REQUIREMENTS>
```

```
    Here is the README of dirdigest tool:
    <README>
    
    Use the README to create a detailed testing suite for the main functionality of the dirdigest tool.
    - Split the tests into logical sections.
    - Explain what each section will test and how
    - Explain how each test will work

    IMPORTANT: Tests should test the functional behavior of the tool not specific implementation details.
```

Then, one can procede with implementing application parts (components) one by one.


## Result

- [`dirdigest`: Directory Digest Generator](./result/dirdigest/README.md)
- [Test Suite for `dirdigest`](./result/dirdigest/tests/README.md)