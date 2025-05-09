# promptbuilder/interactive.py
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

from .config import Config
from .utils import get_multiline_input, validate_path_input, read_text_or_path # Added read_text_or_path

logger = logging.getLogger(__name__)

def run_interactive_mode(cli_args: Any, config: Config) -> Optional[Dict[str, Any]]:
    """Runs the interactive prompting session."""
    collected_data: Dict[str, Any] = {}
    final_actions = {'save_path': None, 'copy_flag': False}

    print("--- PromptBuilder Interactive Mode ---")
    print("Please provide the following details to build the meta-prompt.")
    print("(Leave optional fields blank and press Enter to skip)")
    print(f"(For multi-line input, type '{config.interactive_multiline_end_marker}' on a new line to finish)")

    # 1. Task (Required)
    if cli_args.task:
        print(f"\nUsing Task from command line: {cli_args.task}")
        collected_data['task'] = cli_args.task
    else:
        while not collected_data.get('task'):
            task = input("\nEnter the ultimate task description (Required): ").strip()
            if task:
                collected_data['task'] = task
            else:
                print("Task description cannot be empty.")

    # 2. Context (Optional, Multiple)
    if cli_args.context:
        print(f"\nUsing Context paths from command line: {', '.join(cli_args.context)}")
        collected_data['context_paths'] = cli_args.context
    else:
        context_paths = []
        print("\n--- Context Files/Folders ---")
        print("Enter paths to files or folders for context. Directories will be searched recursively.")
        print("Supported extensions:", ", ".join(config.context_supported_extensions))
        print("Enter 'done' or leave blank when finished.")
        while True:
            path_str = input("Add context path (or 'done'): ").strip()
            if not path_str or path_str.lower() == 'done':
                break
            validated_path = validate_path_input(path_str, check_exists=True)
            if validated_path:
                 context_paths.append(str(validated_path)) # Store as string
        if context_paths:
             collected_data['context_paths'] = context_paths

    # 3. Meta Instructions (Optional)
    if cli_args.meta_instructions:
        print("\nUsing Meta Instructions from command line/file.")
        collected_data['meta_instructions_src'] = cli_args.meta_instructions
    else:
        meta_instr = get_multiline_input(
            "\n[Optional] Enter Meta Instructions (guidance for the prompt *generator*):",
            config.interactive_multiline_end_marker
        ).strip()
        if meta_instr:
            collected_data['meta_instructions_src'] = meta_instr

    # 4. Input Description (Optional)
    if cli_args.input:
        print("\nUsing Input Description from command line/file.")
        collected_data['input_desc_src'] = cli_args.input
    else:
        input_desc = get_multiline_input(
             "\n[Optional] Describe the expected INPUT for the final prompt:",
             config.interactive_multiline_end_marker
        ).strip()
        if input_desc:
            collected_data['input_desc_src'] = input_desc

    # 5. Input Instructions (Optional)
    if cli_args.input_instructions:
         print("\nUsing Input Instructions from command line/file.")
         collected_data['input_instr_src'] = cli_args.input_instructions
    elif collected_data.get('input_desc_src'): # Only ask if input description exists
        input_instr = get_multiline_input(
            "\n[Optional] Enter instructions for the USER on HOW to provide input:",
            config.interactive_multiline_end_marker
        ).strip()
        if input_instr:
            collected_data['input_instr_src'] = input_instr

    # 6. Output Description (Optional)
    if cli_args.output:
        print("\nUsing Output Description from command line/file.")
        collected_data['output_desc_src'] = cli_args.output
    else:
        output_desc = get_multiline_input(
             "\n[Optional] Describe the desired OUTPUT from the final prompt:",
             config.interactive_multiline_end_marker
        ).strip()
        if output_desc:
            collected_data['output_desc_src'] = output_desc

    # 7. Output Instructions (Optional)
    if cli_args.output_instructions:
         print("\nUsing Output Instructions from command line/file.")
         collected_data['output_instr_src'] = cli_args.output_instructions
    elif collected_data.get('output_desc_src'): # Only ask if output description exists
         output_instr = get_multiline_input(
             "\n[Optional] Enter instructions for the LLM on HOW to format output:",
             config.interactive_multiline_end_marker
         ).strip()
         if output_instr:
            collected_data['output_instr_src'] = output_instr

    # --- Prompt Characteristics ---
    print("\n--- Final Prompt Characteristics ---")

    # 8. Persona (Optional)
    if cli_args.persona:
        print("\nUsing Persona from command line/file.")
        collected_data['persona_src'] = cli_args.persona
    else:
        persona_input = input("\n[Optional] Specify the Persona for the final LLM (e.g., 'Helpful Assistant'): ").strip()
        if persona_input:
             collected_data['persona_src'] = persona_input # Store text or path string

    # 9. Constraints (Optional)
    if cli_args.constraints:
        print("\nUsing Constraints from command line/file.")
        collected_data['constraints_src'] = cli_args.constraints
    else:
        constraints_input = get_multiline_input(
             "\n[Optional] Enter general Constraints for the final LLM:",
             config.interactive_multiline_end_marker
         ).strip()
        if constraints_input:
             collected_data['constraints_src'] = constraints_input

    # 10. Tone (Optional)
    if cli_args.tone:
        print("\nUsing Tone from command line/file.")
        collected_data['tone_src'] = cli_args.tone
    else:
        tone_input = input("\n[Optional] Specify the desired Tone (e.g., 'Formal', 'Casual'): ").strip()
        if tone_input:
             collected_data['tone_src'] = tone_input

    # 11. Negative Constraints (Optional)
    if cli_args.negative_constraints:
        print("\nUsing Negative Constraints from command line/file.")
        collected_data['negative_constraints_src'] = cli_args.negative_constraints
    else:
        neg_constraints_input = get_multiline_input(
             "\n[Optional] Enter things the final LLM should NOT do (Negative Constraints):",
             config.interactive_multiline_end_marker
         ).strip()
        if neg_constraints_input:
             collected_data['negative_constraints_src'] = neg_constraints_input


    # --- Examples ---
    print("\n--- Examples ---")
    # 12. Example Input (Optional)
    if cli_args.example_input:
        print("\nUsing Example Input from command line/file.")
        collected_data['example_input_src'] = cli_args.example_input
    else:
        example_input = get_multiline_input(
             "\n[Optional] Provide an EXAMPLE of valid input:",
             config.interactive_multiline_end_marker
        ).strip()
        if example_input:
             collected_data['example_input_src'] = example_input

    # 13. Example Output (Optional)
    if cli_args.example_output:
        print("\nUsing Example Output from command line/file.")
        collected_data['example_output_src'] = cli_args.example_output
    else:
        example_output = get_multiline_input(
             "\n[Optional] Provide an EXAMPLE of desired output:",
             config.interactive_multiline_end_marker
         ).strip()
        if example_output:
             collected_data['example_output_src'] = example_output


    # --- Confirmation ---
    print("\n--- Summary of Collected Information ---")
    print(f"Task: {collected_data.get('task')}")
    print(f"Context Paths: {collected_data.get('context_paths', 'None')}")
    print(f"Meta Instructions Source: {'Provided' if collected_data.get('meta_instructions_src') else 'None'}")
    print(f"Input Description Source: {'Provided' if collected_data.get('input_desc_src') else 'None'}")
    print(f"Input Instructions Source: {'Provided' if collected_data.get('input_instr_src') else 'None'}")
    print(f"Output Description Source: {'Provided' if collected_data.get('output_desc_src') else 'None'}")
    print(f"Output Instructions Source: {'Provided' if collected_data.get('output_instr_src') else 'None'}")
    # Display summary for new fields
    print(f"Persona Source: {'Provided' if collected_data.get('persona_src') else 'None'}")
    print(f"Constraints Source: {'Provided' if collected_data.get('constraints_src') else 'None'}")
    print(f"Tone Source: {'Provided' if collected_data.get('tone_src') else 'None'}")
    print(f"Negative Constraints Source: {'Provided' if collected_data.get('negative_constraints_src') else 'None'}")
    print(f"Example Input Source: {'Provided' if collected_data.get('example_input_src') else 'None'}")
    print(f"Example Output Source: {'Provided' if collected_data.get('example_output_src') else 'None'}")
    print("-" * 30)

    confirm = input("Proceed with generation? [Y/n]: ").strip().lower()
    if confirm not in ('', 'y', 'yes'):
        print("Generation cancelled.")
        return None

    # --- Final Actions ---
    print("\n--- Final Actions ---")
    # Save to disk
    save_path_str = cli_args.save_on_disk or input("Save prompt to disk? (Enter path or leave blank for stdout): ").strip()
    if save_path_str:
        final_actions['save_path'] = save_path_str

    # Copy to clipboard
    copy_default_char = 'Y' if config.copy_to_clipboard_default else 'N'
    copy_prompt = f"Copy prompt to clipboard? [{copy_default_char}/{copy_default_char.lower()}]: " # Fixed prompt display
    copy_input_str = input(copy_prompt).strip().lower()

    # Logic for determining copy action in interactive mode
    should_copy = False
    if cli_args.copy: # CLI flag overrides interactive prompt
        should_copy = True
        print("Copying to clipboard (specified via --copy flag).")
    elif copy_input_str in ('y', 'yes'):
        should_copy = True
    elif copy_input_str == '' and config.copy_to_clipboard_default: # Enter defaults to config value
        should_copy = True
    # Otherwise (n, no, or other input when default is false), should_copy remains False

    final_actions['copy_flag'] = should_copy


    # Attach final actions to the collected data
    collected_data.update(final_actions)

    return collected_data