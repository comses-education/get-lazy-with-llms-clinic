# src/promptbuilder/interactive.py

import logging
import shlex
import os  # Needed for os.path.sep
import sys  # For sys.exit
from pathlib import Path
from typing import Dict, Any, Optional, List

# Rich imports (Only for OUTPUT formatting now)
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text
from rich.syntax import Syntax
from rich.markup import escape  # To safely display user input

from .config import Config

# Import ALL input functions from utils now AND path_completer
from .utils import (
    get_single_line_input,
    get_multiline_input,
    get_yesno_confirmation,
    validate_path_input,
    path_completer,
)

# Use the logger configured in cli.py
logger = logging.getLogger(__name__)

# Multi-line prompt guide (remains the same)
MULTILINE_PROMPT_GUIDE = Text.from_markup(
    "\n[dim]Enter text below. Press [bold]Esc[/bold] then [bold]Enter[/bold] to finish.[/dim]"
    "\n[dim](Allows multi-line editing with arrow keys, Home/End, etc.)[/dim]"
)


def run_interactive_mode(
    cli_args: Any, config: Config, console: Console
) -> Optional[Dict[str, Any]]:
    """Runs the interactive prompting session using ONLY prompt_toolkit for input."""
    collected_data: Dict[str, Any] = {}
    # Initialize actions based on CLI args and config defaults
    final_actions = {
        "save_path": cli_args.save_on_disk,
        "copy_flag": True,  # Default to True for interactive mode
    }

    console.print(Rule("[bold cyan]PromptBuilder Interactive Mode[/bold cyan]"))
    console.print()
    console.print(
        Panel(  # Rich Panel for output
            Text.from_markup(
                "This interactive mode will guide you through providing the details needed to generate a [bold]META_PROMPT[/bold].\n"
                "The META_PROMPT contains instructions for a Large Language Model (LLM) to create a final, task-specific prompt for you.\n\n"
                "[yellow]Tip:[/yellow] You can provide file paths for many fields. If the path exists, its content will be read.\n"
                "[yellow]Tip:[/yellow] Press [bold]Ctrl+C[/bold] at any prompt to cancel and exit."
            ),
            title="Welcome!",
            border_style="blue",
            expand=False,
        )
    )
    console.print(
        "[dim](Leave optional fields blank and press Enter to skip)[/dim]"
    )

    # --- Main Interactive Loop ---
    try:  # Wrap the main input gathering in try...except KeyboardInterrupt
        # 1. Task (Required)
        console.print()  # Add space before
        console.print(Rule("Core Task"))
        console.print()
        if cli_args.task:
            console.print(
                f"Using Task from command line: [green]'{escape(cli_args.task)}'[/green]"
            )
            collected_data["task"] = cli_args.task
        else:
            while "task" not in collected_data or not collected_data["task"]:
                task = get_single_line_input(
                    console, "Enter the ultimate task description (Required): "
                )
                if task:
                    collected_data["task"] = task
                else:
                    console.print(
                        "[prompt.invalid]Task description cannot be empty."
                    )
        # console.print() # Space after task input (optional, rule provides separation)

        # 2. Context (Optional, Multiple) - Use path_completer
        console.print()  # Add space before
        console.print(Rule("Context Files/Folders"))
        console.print()
        if cli_args.context:
            console.print(
                f"Using Context paths from command line: [green]{', '.join(escape(p) for p in cli_args.context)}[/green]"
            )
            collected_data["context_paths"] = cli_args.context
        else:
            context_paths = []
            console.print(
                "[dim]Enter paths to files or folders for context. Dirs searched recursively.[/dim]"
            )
            console.print(
                f"[dim]Supported extensions: {', '.join(config.context_supported_extensions)}[/dim]"
            )
            console.print(
                "[dim]Enter a blank line when finished. Press TAB to autocomplete paths.[/dim]"
            )
            while True:
                path_str = get_single_line_input(
                    console, "Add context path: ", completer=path_completer
                )
                if not path_str:
                    break  # Finished
                validated_path = validate_path_input(
                    path_str, check_exists=True, console=None
                )
                if validated_path:
                    if validated_path.exists():
                        context_paths.append(str(validated_path))
                        console.print(  # Feedback is okay close to input
                            f"[info]Added: {escape(str(validated_path))}[/info]"
                        )
                    else:
                        console.print(
                            f"[warning]Path does not exist or is not accessible: [yellow]{escape(str(validated_path))}[/yellow][/warning]"
                        )
                else:
                    console.print(
                        f"[error]Invalid path format: [yellow]{escape(path_str)}[/yellow][/error]"
                    )
            # Print summary of context paths after loop
            console.print()  # Add space after loop
            if context_paths:
                collected_data["context_paths"] = context_paths
                console.print(f"Collected {len(context_paths)} context path(s).")
            else:
                console.print("No context paths provided.")
                collected_data["context_paths"] = None

        # Define fields to iterate through
        fields_to_ask = [
            (
                "meta_instructions_src",
                "Meta Instructions",
                "Guidance for the prompt generator (how to build the final prompt).",
                "> ",
                True,
                None,
            ),
            (
                "input_desc_src",
                "Input Description",
                "What the final prompt expects as input.",
                "> ",
                True,
                None,
            ),
            (
                "input_instr_src",
                "Input Instructions",
                "How the end-user should provide input to the final prompt.",
                "> ",
                True,
                "input_desc_src",
            ),
            (
                "output_desc_src",
                "Output Description",
                "What the final prompt should produce as output.",
                "> ",
                True,
                None,
            ),
            (
                "output_instr_src",
                "Output Instructions",
                "How the LLM should format the output of the final prompt.",
                "> ",
                True,
                "output_desc_src",
            ),
            (
                "persona_src",
                "Persona",
                "Specify the persona the final LLM should adopt (e.g., 'Expert Python programmer').",
                "Persona: ",
                False,
                None,
            ),
            (
                "constraints_src",
                "Constraints",
                "General constraints the final LLM must adhere to (e.g., 'Answer in under 100 words').",
                "> ",
                True,
                None,
            ),
            (
                "tone_src",
                "Tone",
                "Specify the desired tone for the final LLM's output (e.g., 'Formal', 'Casual').",
                "Tone: ",
                False,
                None,
            ),
            (
                "negative_constraints_src",
                "Negative Constraints",
                "Specify what the final LLM should NOT do (e.g., 'Do not mention pricing').",
                "> ",
                True,
                None,
            ),
            (
                "example_input_src",
                "Example Input",
                "An example of valid input for the final prompt.",
                "> ",
                True,
                None,
            ),
            (
                "example_output_src",
                "Example Output",
                "An example of desired output from the final prompt.",
                "> ",
                True,
                None,
            ),
        ]

        # Iterate through optional fields
        for (
            key,
            rule_title,
            description_dim,
            input_prompt,
            is_multiline,
            depends_on_key,
        ) in fields_to_ask:
            dependency_key_base = (
                depends_on_key.replace("_src", "") if depends_on_key else None
            )
            if depends_on_key and not (
                collected_data.get(depends_on_key)
                or getattr(cli_args, dependency_key_base, None)
            ):
                logger.debug(
                    f"Skipping '{rule_title}' because dependency '{depends_on_key}' is not met."
                )
                collected_data[key] = None
                continue

            console.print()  # Add space before rule
            console.print(Rule(rule_title))
            cli_arg_name = key.replace("_src", "")
            cli_value = getattr(cli_args, cli_arg_name, None)

            if cli_value:
                console.print(
                    f"Using value from command line: [green]'{escape(str(cli_value))}'[/green]"
                )
                collected_data[key] = cli_value
                # No input needed, maybe add space after this message?
                # console.print() # Optional space after CLI value message
            else:
                console.print(
                    f"[dim]{description_dim} (Optional, leave blank to skip)[/dim]"
                )

                if is_multiline:
                    console.print(
                        MULTILINE_PROMPT_GUIDE
                    )  # Shows simplified instruction now
                    user_input = get_multiline_input(console, input_prompt)
                else:
                    # No completer needed for these general single-line fields
                    user_input = get_single_line_input(console, input_prompt)

                if user_input:
                    collected_data[key] = user_input.strip()
                else:
                    collected_data[key] = None
                # console.print() # Optional space after input field

        # --- Confirmation ---
        console.print()  # Add space before summary
        console.print(Rule("Summary"))
        console.print()

        # Helper function (no changes needed)
        def format_summary_value(
            key: str, data: dict, max_len=100
        ) -> Text:
            # (implementation unchanged)
            value = data.get(key)
            if key == "context_paths":
                if value and isinstance(value, list):
                    paths_str = ", ".join(f"'{escape(p)}'" for p in value)
                    if len(paths_str) > max_len:
                        paths_str = paths_str[: max_len - 3] + "..."
                    return Text(
                        f"{len(value)} path(s): {paths_str}", style="green"
                    )
                else:
                    return Text("None", style="dim")
            elif isinstance(value, str) and value:
                escaped_value = escape(value)
                display_value = escaped_value.replace("\n", "\\n")
                if len(display_value) > max_len:
                    display_value = display_value[: max_len - 3] + "..."
                return Text(f"'{display_value}'", style="green")
            elif value:
                return Text(f"{escape(str(value))}", style="green")
            else:
                return Text("None", style="dim")

        # Build the summary content (no changes needed)
        summary_content = Text()
        key_display_map = {
            "task": "Task",
            "context_paths": "Context Paths",
            "meta_instructions_src": "Meta Instructions",
            "input_desc_src": "Input Description",
            "input_instr_src": "Input Instructions",
            "output_desc_src": "Output Description",
            "output_instr_src": "Output Instructions",
            "persona_src": "Persona",
            "constraints_src": "Constraints",
            "tone_src": "Tone",
            "negative_constraints_src": "Negative Constraints",
            "example_input_src": "Example Input",
            "example_output_src": "Example Output",
        }
        num_items = len(key_display_map)
        for i, (key, display_name) in enumerate(key_display_map.items()):
            value_text = format_summary_value(key, collected_data)
            summary_content.append(f"{display_name}: ", style="bold")
            summary_content.append(value_text)
            if i < num_items - 1:
                summary_content.append("\n")

        console.print(
            Panel(
                summary_content,
                title="Collected Information",
                border_style="blue",
                expand=False,
            )
        )

        # --- Proceed Prompt (using standard input) ---
        console.print(
            # Use Markup directly here for the prompt text
            "\n[white]Press [bold]ENTER[/bold] to generate the prompt, or [bold]Ctrl+C[/bold] to cancel.[/white]"
        )
        input()  # Wait for Enter or Ctrl+C
        console.print()  # Add space after proceed confirmation

        # --- Final Actions ---
        console.print(Rule("Final Actions"))
        console.print()
        # Save to disk
        if not cli_args.save_on_disk:
            # Print the prompt text manually using console.print
            console.print(
                "Save prompt to disk? (Enter path or leave blank for stdout): ",
                end="",  # Prevent extra newline before input()
            )
            # Use standard input()
            save_path_str = input()

            if save_path_str:
                save_path_str = save_path_str.strip()
                validated_save_path = validate_path_input(
                    save_path_str, check_exists=False, console=None
                )
                if validated_save_path:
                    try:
                        abs_path = Path(save_path_str).resolve()
                        final_actions["save_path"] = str(abs_path)
                        console.print(
                            f"[info]Will save to: {escape(str(abs_path))}[/info]"
                        )
                    except Exception as e:
                        final_actions["save_path"] = str(
                            validated_save_path
                        )  # Fallback
                        console.print(
                            f"[info]Will save to (relative): {escape(str(validated_save_path))}[/info]"
                        )
                        logger.warning(
                            f"Could not resolve save path {validated_save_path}: {e}"
                        )
                else:
                    console.print(
                        f"[error]Invalid save path format: [yellow]{escape(save_path_str)}[/yellow]. Will print to stdout.[/error]"
                    )
                    final_actions["save_path"] = None
            else:  # User pressed Enter with no input
                final_actions["save_path"] = None
                console.print("[info]Will print to stdout.[/info]")
            console.print()  # Add space after save path interaction

        else:  # Path provided via CLI arg
            console.print(
                f"Will save to disk (from --save-on-disk): [green]{escape(str(cli_args.save_on_disk))}[/green]"
            )
            # Add space after CLI message
            console.print()

        # Copy to Clipboard - No longer asked, default is True
        if final_actions.get("copy_flag"):
            console.print("[info]Will copy prompt to clipboard.[/info]")
            console.print()  # Add space after copy message

        # --- Generate Equivalent Command --- (No changes needed)
        command_parts = ["promptbuilder"]

        def add_arg(flag: str, value: Optional[Any]):
            if value:
                command_parts.append(flag)
                command_parts.append(shlex.quote(str(value)))

        arg_map = {
            "task": "--task",
            "meta_instructions_src": "--meta-instructions",
            "input_desc_src": "--input",
            "input_instr_src": "--input-instructions",
            "output_desc_src": "--output",
            "output_instr_src": "--output-instructions",
            "persona_src": "--persona",
            "constraints_src": "--constraints",
            "tone_src": "--tone",
            "negative_constraints_src": "--negative-constraints",
            "example_input_src": "--example-input",
            "example_output_src": "--example-output",
        }
        for key, flag in arg_map.items():
            add_arg(flag, collected_data.get(key))
        context_paths_final = collected_data.get("context_paths")
        if context_paths_final and isinstance(context_paths_final, list):
            command_parts.append("--context")
            for path in context_paths_final:
                command_parts.append(shlex.quote(path))
        if final_actions.get("save_path"):
            add_arg("--save-on-disk", final_actions["save_path"])
        if final_actions.get("copy_flag"):
            command_parts.append("--copy")
        if cli_args.template:
            add_arg("--template", cli_args.template)
        if cli_args.config:
            add_arg("--config", cli_args.config)
        if cli_args.verbose > 0:
            command_parts.append(f"-{'v' * cli_args.verbose}")
        equivalent_command = " ".join(command_parts)
        console.print(Rule("[bold blue]Equivalent Command[/bold blue]"))
        console.print()
        console.print(
            "You can use this command to reproduce the same meta-prompt without interactive mode:"
        )
        console.print(
            Syntax(
                equivalent_command,
                "bash",
                theme="default",
                line_numbers=False,
                word_wrap=True,
            )
        )
        console.print("")

        # Attach final actions determined above
        collected_data["save_path"] = final_actions.get("save_path")
        collected_data["copy_flag"] = final_actions.get("copy_flag")

        return collected_data

    except KeyboardInterrupt:
        # Catch Ctrl+C from any input function OR the standard input() calls
        console.print("\n[yellow]Interactive mode cancelled by user.[/yellow]")
        sys.exit(0)  # Exit gracefully