# Process Outline

1. **Define Task** (by hand) 🠚 `TASK`
2. **Define Requirements** (by hand ) 🠚 `REQUIREMENTS`
3. **Find Relevant Context** (ask PPLX): *"Give me best practices on how to do `TASK`"* 🠚 `CONTEXT`
4. **Improve requirements** (ask PPLX): *"I want to `TASK` with following requirements: `REQUIREMENTS`. Use this context: `CONTEXT` to create an improved set of requirements that would improve usability, reliability and maintanability of the tool."*
5. **Revise the generated requirements** (by hand) CAREFULLY! revise the `GENERATED_REQUIREMENTS` 🠚 `IMPROVED_REQUIREMENTS`
6. **Supply general instructions** (by hand or ask PPLX): general instructions/guidelines/preferences on **HOW** to solve the `TASK`.
6. **Create the performing prompt** (by hand) `TASK`+`IMPROVED_REQUIREMENTS`+ `INSTRUCTIONS` 🠚 `PERFORMING_PROMPT`
7. **Use the `PERFORMING_PROMPT`** 🠚 `SOLUTION`

# Process Execution:

## **1. Define Task** (by hand) 🠚 `TASK`
> [`TASK`](./prompting_log/01_task.md)

## **2. Define Requirements** (by hand ) 🠚 `REQUIREMENTS`
> [`REQUIREMENTS`](./prompting_log/02_requirements.md)

## **3. Get Some Relevant Context** (ask PPLX) 🠚 `CONTEXT`
```yml
"I want to <TASK> with folowing requirements: <REQUIREMENTS>. Give me best practices on how to perform tasks like <TASK>"
```
> [`CONTEXT`](./prompting_log/03_context.md) 

## **4. Improve requirements** (ask PPLX, or Gemeni 2.5 Pro): 🠚 `GENERATED_REQUIREMENTS`
```yml
"I want to <TASK> with following <REQUIREMENTS>. Use this context <CONTEXT> to create an improved set of requirements that would improve usability, reliability and maintanability of the tool." 
```
| **Provider**    | **Model**                    | **File Link**                                                                                              | **Subjective Rating** |
| --------------- | ---------------------------- | ---------------------------------------------------------------------------------------------------------- | ---------- |
| aistudio.google | gemini-2.5-pro-preview-03-25 | [`GENERATED_REQUIREMENTS`](./prompting_log/04_generated_requirements_[aistudio.google]_[gemini-2.5-pro-preview-03-25].md) |    ★ ★ ★         |
| cursor          | claude-3.7-sonnet            | [`GENERATED_REQUIREMENTS`](./prompting_log/04_generated_requirements_[cursor]_[claude-3.7-sonnet].md)                     |       ★      |
| cursor          | gemini-2.5-pro-preview-03-25 | [`GENERATED_REQUIREMENTS`](./prompting_log/04_generated_requirements_[cursor]_[gemini-2.5-pro-preview-03-25].md)          |        ★ ★     |
| perplexity-pro  | claude-3.7-sonnet-thinking   | [`GENERATED_REQUIREMENTS`](./prompting_log/04_generated_requirements_[perplexity-pro]_[claude-3.7-sonnet-thinking].md)    |       ★      |
| perplexity-pro  | research                     | [`GENERATED_REQUIREMENTS`](./prompting_log/04_generated_requirements_[perplexity-pro]_[research].md)                      |       ★      |


## **5. Revise the generated requirements** (by hand) 🠚 `IMPROVED_REQUIREMENTS`
- carefully revise all suggested `GENERATED_REQUIREMENTS`
- mix and match best parts
- ask follow up queries to improve parts of the `GENERATED REQUIREMENTS` like: 
```yml
"add interactive mode to functional requirements and write a detailed specification for it. Emphasize importance of modular and easily testable architecture."
```
> [`IMPROVED_REQUIREMENTS`](./prompting_log/05_improved_requirements.md)

## **6. Supply general instructions** (by hand or ask PPLX): general instructions/guidelines/preferences on HOW to solve the `TASK`.
Let's create some general implementation instructions for a `python cli tool`:

```yml
Give me some general best practices implementations for a python cli tool. Continue the list:
    - use uv as dependency manager https://docs.astral.sh/uv/concepts/tools/
    - use pytest to create unit tests for main functionality
    - use latest versions of packages, provide links to their documentation
```
> [`INSTRUCTIONS`](./prompting_log/06_instructions.md)

## **7. Create the performing prompt** (by hand) 🠚 `PERFORMING_PROMPT`
**What do we actually want to "perform"?** Our [`TASK`](./prompting_log/01_task.md), of course!

At this point we might ask the LLM to implement everything in one go:
```yml
"Implement the promptbuilder tool with following requirements: <IMPROVED_REQUIREMENTS>"
```


Finally, let's build the `TASK_PERFORMING_PROMPT` with following structure:
```yaml
    TASK
    IMPROVED_REQUIREMENTS
    INSTRUCTIONS
```
> [`PERFORMING_PROMPT`](./prompting_log/07_performing_prompt.md)

## **8. Use the `PERFORMING_PROMPT`** 🠚 `SOLUTION`

Let's actually do the `TASK`!

> [`SOLUTION`](./prompting_log/05_one_shot_solution_[aistudio.google]_[gemini-2.5-pro-preview-03-25].md)

### Notes
Surprisingly, Gemini 2.5 Pro generated a usable probmptbuilder tool in one go. I encountered minor python/poetry errors, which were easily solved with a couple of follow up questions to LLM.