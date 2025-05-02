Create an improved set of requirements that would improve usability, reliability and maintanability of the promptbuilder. This requirements will be fed to an LLM, so be structured and very specific.
Emphasize importance of testability, maintanability and usability of the code.

Code must be structured and implemented in a easy testable way. A test framework will be required.


# TASK
I want to create a python command line tool which helps the user to build a META_PROMPT.
The user will feed the META_PROMPT to an LLM of his choice. The generated response from the META_PROMPT should be a TASK_PERFORMING_PROMPT that the user will use to feed to an LLM of his choice to perform his TASK.

with following requirements:
## Requirements

promptbuilder args: 
    --task: short task description
    --context: list of local files or entire folders that should be parsed recursively
    --instructions: str or local instructions file
    --input: str or local file describing the input to the PERFORMING PROMPT
    --output: str or local file describing the output to the PERFORMING PROMPT
    --input_instructions: str or local file describing the input instructions to the PERFORMING PROMPT
    --output_instructions: str or local file describing the output instructions to the PERFORMING PROMPT
    --save_on_disk: path where the META_PROMPT should be stored


REASONABLE DEFAULTS and CONFIGS SHOULD BE PROVIDED in a config file: .promptbuilder

### Functional Requirements
- output META_PROMPT to the stdout or to disk if --save_on_disk
- copy prompt to clipboard after the command has executed
- if input/output or input_instructions/output_instructions are specified, the META_PROMPT should CLEARLY MENTION TO USE THEM AS PLACEHOLDERS in the PERFORMING_PROMPT.


# Context:
```
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

```