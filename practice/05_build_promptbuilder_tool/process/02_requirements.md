```bash
    promptbuilder args:
        --task: short task description
        --context: list of local files or entire folders that should be parsed recursively
        --instructions: str or local instructions file
        --input: str or local file describing the input to the PERFORMING PROMPT
        --output: str or local file describing the output to the PERFORMING PROMPT
        --input_instructions: str or local file describing the input instructions to the PERFORMING PROMPT
        --output_instructions: str or local file describing the output instructions to the PERFORMING PROMPT
        --save_on_disk: path where the META_PROMPT should be stored
```

REASONABLE DEFAULTS and CONFIGS SHOULD BE PROVIDED in a config file: .promptbuilder

## Functional Requirements
- output META_PROMPT to the stdout or to disk if --save_on_disk
- copy prompt to clipboard after the command has executed
- if input/output or input_instructions/output_instructions are specified, the META_PROMPT should CLEARLY MENTION TO USE THEM AS PLACEHOLDERS in the PERFORMING_PROMPT.

## Non-Functional Requirements
