import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

from .config import Config
from .utils import get_multiline_input, validate_path_input

logger = logging.getLogger(__name__)

def run_interactive_mode(cli_args: Any, config: Config) -> Optional[Dict[str, Any]]:
    """Runs the interactive prompting session."""
    collected_data: Dict[str, Any] = {}
    final_actions = {'save_path': None, 'copy_flag': False}

    print("--- PromptBuilder Interactive Mode ---")
    print("Please provide the following details to build the meta-prompt.")
    print("(Leave optional fields blank and press Enter to skip)")

    # 1. Task (Required)
    if cli_args.task:
        print(f"Using Task from command line: {cli_args.task}")
        collected_data['task'] = cli_args.task
    else:
        while not collected_data.get('task'):
            task = input("Enter the ultimate task description (Required): ").strip()
            if task:
                collected_data['task'] = task
            else:
                print("Task description cannot be empty.")

    # 2. Context (Optional, Multiple)
    if cli_args.context:
        print(f"Using Context paths from command line: {', '.join(cli_args.context)}")
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
            # Basic validation - check existence? utils.validate_path_input can do this
            validated_path = validate_path_input(path_str, check_exists=True)
            if validated_path:
                 context_paths.append(str(validated_path)) # Store as string initially
            # else: Error message printed by validate_path_input
        if context_paths:
             collected_data['context_paths'] = context_paths

    # 3. Meta Instructions (Optional)
    if cli_args.meta_instructions:
        print("\nUsing Meta Instructions from command line/file.")
        # Reading happens later in cli.py based on collected path/text
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

    # 8. Example Input (Optional)
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

    # 9. Example Output (Optional)
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
        # Allow relative paths, resolve later in cli.py
        final_actions['save_path'] = save_path_str

    # Copy to clipboard
    copy_default = 'y' if config.copy_to_clipboard_default else 'n'
    copy_prompt = f"Copy prompt to clipboard? [{copy_default.upper()}/{copy_default.lower()}]: "
    copy_choice = cli_args.copy or input(copy_prompt).strip().lower()
    if cli_args.copy: # If flag is set, force copy
         final_actions['copy_flag'] = True
    elif copy_choice in ('y', 'yes'):
        final_actions['copy_flag'] = True
    elif not copy_choice and config.copy_to_clipboard_default: # Default applies if blank
         final_actions['copy_flag'] = True
    else:
         final_actions['copy_flag'] = False


    # Attach final actions to the collected data
    collected_data.update(final_actions)

    return collected_data