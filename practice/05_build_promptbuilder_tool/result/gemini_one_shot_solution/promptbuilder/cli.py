# promptbuilder/cli.py
import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional

from . import config as cfg
from . import context
from . import templating
from . import utils
from . import interactive

# Setup basic logging configuration
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.WARNING, format=log_format)
logger = logging.getLogger(__name__) # Get logger for this module

def setup_logging(verbose_level: int):
    """Configures logging level based on verbosity."""
    if verbose_level == 1:
        logging.getLogger('promptbuilder').setLevel(logging.INFO)
        logger.info("Verbose mode enabled (INFO level)")
    elif verbose_level >= 2:
        logging.getLogger('promptbuilder').setLevel(logging.DEBUG)
        logger.info("Verbose mode enabled (DEBUG level)")
    # Else: keep default (WARNING)


def create_parser() -> argparse.ArgumentParser:
    """Creates the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="Generate META_PROMPTs for instructing LLMs to create task-performing prompts.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Core arguments
    core_group = parser.add_argument_group('Core arguments')
    core_group.add_argument(
        "--task",
        type=str,
        help="**(Required unless interactive)** Concise description of the ultimate task for the final LLM."
    )
    core_group.add_argument(
        "--context",
        type=str,
        nargs='+',  # Allows one or more paths
        help="One or more file or directory paths for context. Dirs parsed recursively for supported types."
    )
    core_group.add_argument(
        "--meta-instructions",
        metavar="TEXT_OR_PATH",
        help="Instructions for the META_PROMPT generator (how to build the final prompt). Text or file path."
    )

    # Input/Output Specification
    io_group = parser.add_argument_group('Input/Output Specification')
    io_group.add_argument(
        "--input",
        metavar="TEXT_OR_PATH",
        help="Description of the expected input for the final prompt. Text or file path."
    )
    io_group.add_argument(
        "--output",
        metavar="TEXT_OR_PATH",
        help="Description of the desired output from the final prompt. Text or file path."
    )
    io_group.add_argument(
        "--input-instructions",
        metavar="TEXT_OR_PATH",
        help="Instructions for the USER on how to provide input. Text or file path."
    )
    io_group.add_argument(
        "--output-instructions",
        metavar="TEXT_OR_PATH",
        help="Instructions for the LLM on how to format output. Text or file path."
    )

    # Prompt Characteristics (NEW GROUP)
    char_group = parser.add_argument_group('Prompt Characteristics (for the final prompt)')
    char_group.add_argument(
        "--persona",
        metavar="TEXT_OR_PATH",
        help="Specify the persona the final LLM should adopt (e.g., 'Helpful assistant', 'Expert Python programmer'). Text or file path."
    )
    char_group.add_argument(
        "--constraints",
        metavar="TEXT_OR_PATH",
        help="General constraints the final LLM must adhere to (e.g., 'Answer in under 100 words', 'Use only information from the context'). Text or file path."
    )
    char_group.add_argument(
        "--tone",
        metavar="TEXT_OR_PATH", # Allow file path for more complex tone descriptions
        help="Specify the desired tone for the final LLM's output (e.g., 'Formal', 'Casual and friendly', 'Technical'). Text or file path."
    )
    char_group.add_argument(
        "--negative-constraints",
        metavar="TEXT_OR_PATH",
        help="Specify what the final LLM should NOT do (e.g., 'Do not mention pricing', 'Avoid using jargon'). Text or file path."
    )

    # Examples
    example_group = parser.add_argument_group('Examples')
    example_group.add_argument(
        "--example-input",
        metavar="TEXT_OR_PATH",
        help="An example of valid input for the final prompt. Text or file path."
    )
    example_group.add_argument(
        "--example-output",
        metavar="TEXT_OR_PATH",
        help="An example of desired output from the final prompt. Text or file path."
    )

    # Output and Configuration
    output_group = parser.add_argument_group('Output and Configuration')
    output_group.add_argument(
        "--save-on-disk",
        metavar="PATH",
        help="Save the generated META_PROMPT to this file path instead of printing to stdout."
    )
    output_group.add_argument(
        "--copy",
        action="store_true",
        help="Copy the generated META_PROMPT to the system clipboard."
    )
    output_group.add_argument(
        "--config",
        metavar="PATH",
        help=f"Specify a configuration file path (default search: ./{cfg.DEFAULT_CONFIG_FILENAME}, {cfg.CONFIG_SEARCH_PATHS[1]})."
    )
    output_group.add_argument(
        "--template",
        metavar="PATH",
        help="Specify a custom META_PROMPT Jinja2 template file."
    )

    # Modes and Verbosity
    mode_group = parser.add_argument_group('Modes and Verbosity')
    mode_group.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Activate Interactive Mode to gather inputs via prompts."
    )
    mode_group.add_argument(
        "-v", "--verbose",
        action="count",
        default=0,
        help="Increase output verbosity (-v for INFO, -vv for DEBUG)."
    )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    setup_logging(args.verbose)

    # Load configuration
    config = cfg.Config.load(args.config)
    if args.verbose > 0:
        logger.info(f"Loaded configuration: {config}")


    collected_data: Optional[Dict[str, Any]] = None
    final_actions = {
        'save_path': args.save_on_disk,
        'copy_flag': args.copy or (config.copy_to_clipboard_default and not args.copy),
    }

    if args.interactive:
        logger.info("Starting interactive mode...")
        interactive_results = interactive.run_interactive_mode(args, config)
        if interactive_results is None:
            sys.exit(0) # User cancelled
        collected_data = interactive_results
        final_actions['save_path'] = collected_data.pop('save_path', None)
        final_actions['copy_flag'] = collected_data.pop('copy_flag', False)
    else:
        # CLI Mode
        if not args.task:
            parser.error("--task is required in non-interactive mode.")
            # sys.exit(1) # Unreachable due to parser.error

        logger.info("Running in CLI mode...")
        collected_data = {
            'task_description': args.task,
            'context_paths': args.context,
            'meta_instructions_src': args.meta_instructions,
            'input_desc_src': args.input,
            'input_instr_src': args.input_instructions,
            'output_desc_src': args.output,
            'output_instr_src': args.output_instructions,
            # Add sources for new args
            'persona_src': args.persona,
            'constraints_src': args.constraints,
            'tone_src': args.tone,
            'negative_constraints_src': args.negative_constraints,
            'example_input_src': args.example_input,
            'example_output_src': args.example_output,
        }
        # final_actions already set from args/config

    # --- Common Processing (Both Modes) ---

    # Resolve text/path arguments
    template_data: Dict[str, Any] = {
         'task_description': collected_data.get('task') or collected_data.get('task_description'),
         'meta_instructions': utils.read_text_or_path(collected_data.get('meta_instructions_src'), config.context_encoding, 'meta-instructions'),
         'input_description': utils.read_text_or_path(collected_data.get('input_desc_src'), config.context_encoding, 'input description'),
         'input_instructions': utils.read_text_or_path(collected_data.get('input_instr_src'), config.context_encoding, 'input instructions'),
         'output_description': utils.read_text_or_path(collected_data.get('output_desc_src'), config.context_encoding, 'output description'),
         'output_instructions': utils.read_text_or_path(collected_data.get('output_instr_src'), config.context_encoding, 'output instructions'),
         # Read new args
         'persona': utils.read_text_or_path(collected_data.get('persona_src'), config.context_encoding, 'persona'),
         'constraints': utils.read_text_or_path(collected_data.get('constraints_src'), config.context_encoding, 'constraints'),
         'tone': utils.read_text_or_path(collected_data.get('tone_src'), config.context_encoding, 'tone'),
         'negative_constraints': utils.read_text_or_path(collected_data.get('negative_constraints_src'), config.context_encoding, 'negative constraints'),
         'example_input': utils.read_text_or_path(collected_data.get('example_input_src'), config.context_encoding, 'example input'),
         'example_output': utils.read_text_or_path(collected_data.get('example_output_src'), config.context_encoding, 'example output'),
         'verbose_level': args.verbose,
         'config': config, # Pass config object to template
    }

    # Process context
    context_items = []
    context_files_processed = 0
    context_files_skipped = 0
    context_paths_to_parse = collected_data.get('context_paths', [])
    if context_paths_to_parse:
         logger.info("Processing context paths...")
         context_items, context_files_processed, context_files_skipped = context.parse_context_paths(
             context_paths_to_parse,
             config,
             args.verbose
         )
    template_data['context_items'] = context_items
    template_data['context_files_processed'] = context_files_processed
    template_data['context_files_skipped'] = context_files_skipped


    # Determine template path
    template_path = Path(args.template) if args.template else config.default_meta_prompt_template_path

    # Generate META_PROMPT
    logger.info("Generating META_PROMPT...")
    meta_prompt = templating.render_meta_prompt(template_path, template_data, config)

    if not meta_prompt:
        logger.error("Failed to generate META_PROMPT.")
        sys.exit(1)

    # --- Output Actions ---
    output_performed = False
    # 1. Save to Disk
    save_target_str = final_actions.get('save_path')
    if save_target_str:
        save_path = Path(save_target_str)
        if not save_path.is_absolute():
             save_path = config.output_dir / save_path
        if utils.save_to_disk(meta_prompt, save_path.resolve()):
             output_performed = True
        else:
             logger.warning(f"Proceeding without saving to disk due to error.")


    # 2. Copy to Clipboard
    if final_actions.get('copy_flag'):
        if utils.copy_to_clipboard(meta_prompt):
            output_performed = True
        else:
             logger.warning(f"Proceeding without copying to clipboard due to error.")

    # 3. Print to Stdout
    if not output_performed or (not save_target_str and not final_actions.get('copy_flag')):
         if output_performed: # Add a separator only if other actions *succeeded* but stdout is still needed
              print("\n--- Generated META_PROMPT ---")
         elif save_target_str or final_actions.get('copy_flag'): # Add separator if actions were *attempted* but maybe failed
              print("\n--- Generated META_PROMPT (stdout fallback) ---")

         print(meta_prompt)

    logger.info("PromptBuilder finished.")
    sys.exit(0)


if __name__ == '__main__':
    main()