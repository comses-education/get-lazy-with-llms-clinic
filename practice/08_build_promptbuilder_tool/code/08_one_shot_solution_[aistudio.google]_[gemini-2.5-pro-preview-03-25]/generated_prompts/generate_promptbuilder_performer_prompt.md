
**Objective:** Generate a high-quality TASK_PERFORMING_PROMPT based on the specifications below. This prompt will be used by a human user to instruct another LLM to perform a specific task.

**Your Role:** You are an expert prompt engineer. Your goal is to create a clear, concise, effective, and robust TASK_PERFORMING_PROMPT.

**Core Task for the Final LLM:**
The ultimate task the final LLM needs to perform is:
Create a python command line tool which helps the user to build a META_PROMPT. The user will feed the META_PROMPT to an LLM of his choice. The generated response from the META_PROMPT should be a TASK_PERFORMING_PROMPT that the user will use to feed to an LLM of his choice to perform his TASK.


Construct the TASK_PERFORMING_PROMPT adhering to the following structure and including the specified elements:

**1. Clear Directive:** Start with a clear and direct instruction summarizing the main goal for the final LLM.

**2. Persona (Optional but Recommended):** If appropriate for the task, instruct the final LLM to adopt a specific persona (e.g., "Act as a helpful coding assistant," "You are a creative writer specializing in fantasy.").

**3. Context (If Provided):**
The final prompt should inform the LLM that the following context is available to assist with the task. The user will provide this context alongside the prompt.
Summarize or reference the context appropriately within the final prompt.

**Provided Context Summary:**
The following files/sources were provided as context:
  - /home/asuworks/work/repos/github.com/comses-education/get-lazy-with-llms-clinic/my-prompts/6_build_a_python_cli_tool/code/05_one_shot_solution_[aistudio.google]_[gemini-2.5-pro-preview-03-25]/test_docs/usecase_promptbuilder/03_context.md  - /home/asuworks/work/repos/github.com/comses-education/get-lazy-with-llms-clinic/my-prompts/6_build_a_python_cli_tool/code/05_one_shot_solution_[aistudio.google]_[gemini-2.5-pro-preview-03-25]/test_docs/usecase_promptbuilder/05_improved_requirements.md  - /home/asuworks/work/repos/github.com/comses-education/get-lazy-with-llms-clinic/my-prompts/6_build_a_python_cli_tool/code/05_one_shot_solution_[aistudio.google]_[gemini-2.5-pro-preview-03-25]/test_docs/usecase_promptbuilder/01_task.md  - /home/asuworks/work/repos/github.com/comses-education/get-lazy-with-llms-clinic/my-prompts/6_build_a_python_cli_tool/code/05_one_shot_solution_[aistudio.google]_[gemini-2.5-pro-preview-03-25]/test_docs/usecase_promptbuilder/06_instructions.md

**4. Input Specification (If Provided):**

**5. Output Specification (If Provided):**
The final prompt MUST instruct the LLM on the desired output format or structure.
Description of desired output:
the code for the promptbuilder
The final prompt might need an `{{OUTPUT}}` placeholder or a dedicated section describing the output format.
**6. Examples (If Provided):**

**7. Constraints & Tone:** Ensure the final prompt clearly states any constraints, desired tone, or negative constraints (what the LLM *should not* do).

**8. Final Check:** The generated TASK_PERFORMING_PROMPT should be self-contained, unambiguous, and directly usable by a human interacting with an LLM.



Now, based on all the above instructions, generate the TASK_PERFORMING_PROMPT.