import click
import pathlib
import time 
import logging

from dirdigest.constants import TOOL_NAME, TOOL_VERSION
from dirdigest import core
from dirdigest import formatter as dirdigest_formatter
from dirdigest.utils import logger as dirdigest_logger
from dirdigest.utils import clipboard as dirdigest_clipboard
from dirdigest.utils import config as dirdigest_config


@click.command(
    name=TOOL_NAME,
    context_settings=dict(help_option_names=['-h', '--help']),
    help="Recursively processes directories and files, creating a structured digest suitable for LLM context ingestion."
)
@click.version_option(version=TOOL_VERSION, prog_name=TOOL_NAME, message="%(prog)s version %(version)s")
@click.pass_context 
@click.argument(
    'directory_arg',
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        path_type=pathlib.Path
    ),
    default='.',
    required=False,
    metavar='DIRECTORY'
)
@click.option(
    '--output', '-o',
    type=click.Path(dir_okay=False, writable=True, path_type=pathlib.Path),
    default=None,
    help='Path to the output file. If omitted, the digest is written to standard output (stdout).'
)
@click.option(
    '--format', '-f',
    type=click.Choice(['json', 'markdown'], case_sensitive=False),
    default='markdown',
    show_default=True,
    help="Output format for the digest. Choices: 'json', 'markdown'."
)
@click.option(
    '--include', '-i',
    multiple=True,
    help=("Glob pattern(s) for files/directories to INCLUDE. If specified, only items matching these "
          "patterns are processed. Can be used multiple times or comma-separated "
          "(e.g., -i '*.py' -i 'src/' or -i '*.py,src/'). Exclusions are applied first.")
)
@click.option(
    '--exclude', '-x',
    multiple=True,
    help=("Glob pattern(s) for files/directories to EXCLUDE. Takes precedence over include patterns. "
          "Can be used multiple times or comma-separated (e.g., -x '*.log' -x 'tests/' or "
          "-x '*.log,tests/'). Default ignores also apply unless --no-default-ignore is set.")
)
@click.option(
    '--max-size', '-s',
    type=click.IntRange(min=0),
    default=300,
    show_default=True,
    help="Maximum size (in KB) for individual files to be included. Larger files are excluded."
)
@click.option(
    '--max-depth', '-d',
    type=click.IntRange(min=0),
    default=None,
    show_default="unlimited",
    help="Maximum depth of directories to traverse. Depth 0 processes only the starting directory's files. Unlimited by default."
)
@click.option(
    '--no-default-ignore',
    is_flag=True,
    show_default=True, # Default is False
    help=("Disable all default ignore patterns (e.g., .git, __pycache__, node_modules, common "
          "binary/media files, hidden items). Use if you need to include items normally ignored by default.")
)
@click.option(
    '--follow-symlinks',
    is_flag=True,
    show_default=True, # Default is False
    help="Follow symbolic links to directories and files. By default, symlinks themselves are noted but not traversed/read."
)
@click.option(
    '--ignore-errors',
    is_flag=True,
    show_default=True, # Default is False
    help=("Continue processing if an error occurs while reading a file (e.g., permission denied, "
          "decoding error). The file's content will be omitted or noted as an error in the digest.")
)
@click.option(
    '--clipboard/--no-clipboard', '-c',
    default=True,
    show_default=True,
    help="Copy the generated digest to the system clipboard. Use --no-clipboard to disable."
)
@click.option(
    '--verbose', '-v',
    count=True,
    help='Increase verbosity. -v for INFO, -vv for DEBUG console output.'
)
@click.option(
    '--quiet', '-q',
    is_flag=True,
    help='Suppress all console output below ERROR level. Overrides -v.'
)
@click.option(
    '--log-file',
    type=click.Path(dir_okay=False, writable=True, path_type=pathlib.Path),
    default=None,
    help="Path to a file for detailed logging. All logs (including DEBUG level) will be written here, regardless of console verbosity."
)
@click.option(
    '--config', 'config_path_cli',
    type=click.Path(exists=True, dir_okay=False, readable=True, path_type=pathlib.Path),
    default=None,
    # Corrected help text:
    help=(f"Specify configuration file path. If omitted, tries to load "
          f"./{dirdigest_config.DEFAULT_CONFIG_FILENAME} from the current directory.")
)
def main_cli( # Parameters match the names of the click options
    ctx: click.Context,
    directory_arg: pathlib.Path,
    output: pathlib.Path | None,
    format: str,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    max_size: int,
    max_depth: int | None,
    no_default_ignore: bool,
    follow_symlinks: bool,
    ignore_errors: bool,
    clipboard: bool,
    verbose: int,
    quiet: bool,
    log_file: pathlib.Path | None,
    config_path_cli: pathlib.Path | None
):
    # ... (rest of the main_cli function remains the same) ...
    # (The logic for loading config, merging, setting up logging, processing, formatting, etc.)

# Need to ensure the main_cli body is here for completeness, though it doesn't change in this step.
# For brevity in this response, I'm omitting the body of main_cli as it was provided in the previous step's "full cli.py"
# and the focus here is only on the @click.option help strings.
# The actual implementation would have the full main_cli body here.
# For this step, only the help strings above are modified.
    start_time = time.monotonic()

    cfg_file_values = dirdigest_config.load_config_file(config_path_cli)
    cli_params_for_merge = ctx.params.copy()
    if 'directory_arg' in cli_params_for_merge and 'directory' not in cli_params_for_merge:
        cli_params_for_merge['directory'] = cli_params_for_merge.pop('directory_arg')
    if 'config_path_cli' in cli_params_for_merge and 'config' not in cli_params_for_merge:
         cli_params_for_merge['config'] = cli_params_for_merge.pop('config_path_cli')
    final_settings = dirdigest_config.merge_config(cli_params_for_merge, cfg_file_values, ctx)

    final_verbose = final_settings.get('verbose', 0)
    final_quiet = final_settings.get('quiet', False)
    final_log_file_val = final_settings.get('log_file') 
    if isinstance(final_log_file_val, str):
        final_log_file_val = pathlib.Path(final_log_file_val)

    dirdigest_logger.setup_logging(
        verbose_level=final_verbose, 
        quiet=final_quiet, 
        log_file_path=final_log_file_val
    )
    log = dirdigest_logger.logger

    final_directory = final_settings.get('directory', directory_arg)
    if isinstance(final_directory, str):
        final_directory = pathlib.Path(final_directory)
        if not final_directory.exists() or not final_directory.is_dir():
            log.error(f"Directory '{final_directory}' from config does not exist or is not a directory. Using CLI/default: '{directory_arg}'")
            final_directory = directory_arg
    
    final_output_path = final_settings.get('output', output)
    if isinstance(final_output_path, str):
        final_output_path = pathlib.Path(final_output_path)

    final_format = final_settings.get('format', format)
    final_include = final_settings.get('include', include if include else [])
    final_exclude = final_settings.get('exclude', exclude if exclude else [])
    final_max_size = final_settings.get('max_size', max_size)
    final_max_depth = final_settings.get('max_depth', max_depth)
    final_no_default_ignore = final_settings.get('no_default_ignore', no_default_ignore)
    final_follow_symlinks = final_settings.get('follow_symlinks', follow_symlinks)
    final_ignore_errors = final_settings.get('ignore_errors', ignore_errors)
    final_clipboard = final_settings.get('clipboard', clipboard)

    log.debug(f"CLI: Final effective settings after merge: {final_settings}")
    log.info(f"CLI: Processing directory: [log.path]{final_directory}[/log.path]")
    if final_output_path:
        log.info(f"CLI: Output will be written to: [log.path]{final_output_path}[/log.path]")
    else:
        log.info("CLI: Output will be written to stdout")
    log.info(f"CLI: Format: {final_format.upper()}")
    if final_verbose > 0 :
        log.info(f"CLI: Include patterns: {final_include if final_include else 'N/A'}")
        log.info(f"CLI: Exclude patterns: {final_exclude if final_exclude else 'N/A'}")
        log.info(f"CLI: Max size: {final_max_size}KB, Max depth: {final_max_depth if final_max_depth is not None else 'unlimited'}")
        log.info(f"CLI: Default ignores {'DISABLED' if final_no_default_ignore else 'ENABLED'}")
        log.info(f"CLI: Follow symlinks: {final_follow_symlinks}, Ignore errors: {final_ignore_errors}")
        log.info(f"CLI: Clipboard: {final_clipboard}")

    processed_items_generator, stats_from_core = core.process_directory_recursive(
        base_dir_path=final_directory,
        include_patterns=final_include,
        exclude_patterns=final_exclude,
        no_default_ignore=final_no_default_ignore,
        max_depth=final_max_depth,
        follow_symlinks=final_follow_symlinks,
        max_size_kb=final_max_size,
        ignore_read_errors=final_ignore_errors
    )

    log.info("CLI: Building digest tree...")
    root_node, metadata_for_output = core.build_digest_tree(
        final_directory,
        processed_items_generator,
        stats_from_core
    )
    log.debug(f"CLI: Digest tree built. Root node children: {len(root_node.get('children',[]))}")
    log.debug(f"CLI: Metadata for output: {metadata_for_output}")

    selected_formatter: dirdigest_formatter.BaseFormatter
    if final_format.lower() == 'json':
        selected_formatter = dirdigest_formatter.JsonFormatter(final_directory, metadata_for_output)
    elif final_format.lower() == 'markdown':
        selected_formatter = dirdigest_formatter.MarkdownFormatter(final_directory, metadata_for_output)
    else: 
        log.critical(f"CLI: Invalid format '{final_format}' encountered. Exiting.")
        ctx.exit(1)
        return 

    log.info(f"CLI: Formatting output as {final_format.upper()}...")
    
    final_output_str = "" 
    output_generation_succeeded = False 

    try:
        generated_digest = selected_formatter.format(root_node)
        
        if final_output_path: 
            with open(final_output_path, 'w', encoding='utf-8') as f_out:
                f_out.write(generated_digest)
            log.info(f"CLI: Digest successfully written to [log.path]{final_output_path}[/log.path]")
        else: 
            dirdigest_logger.stdout_console.print(generated_digest, end="")
            if not generated_digest.endswith('\n'):
                dirdigest_logger.stdout_console.print()
        
        final_output_str = generated_digest 
        output_generation_succeeded = True

    except Exception as e:
        # ADD THIS LINE FOR SUPER EXPLICIT DEBUGGING:
        dirdigest_logger.stderr_console.print(f"[bold red reverse]DEBUG_EXCEPTION_CLIPBOARD: Exception caught in output block: {type(e).__name__} - {e}[/]")
        
        log.error(f"CLI: Error during output formatting or writing: {e}", exc_info=True)
        final_output_str = f"Error generating output: {e}" 
        # output_generation_succeeded remains False (its initial value)

    # --- Clipboard ---
    if final_clipboard:
        # Add a debug log here too to see the state
        log.debug(f"CLI_CLIPBOARD_CHECK: output_generation_succeeded={output_generation_succeeded}, final_output_str starts with '{final_output_str[:30]}...'")
        if output_generation_succeeded and final_output_str: 
            dirdigest_clipboard.copy_to_clipboard(final_output_str)
        elif not output_generation_succeeded: 
            log.warning("CLI: Output generation failed (see error above), not copying to clipboard.")
        else: 
            log.debug("CLI: Output is empty, nothing to copy to clipboard.")
    else:
        log.debug("CLI: Clipboard copy disabled.")

    execution_time = time.monotonic() - start_time
    inc_count = metadata_for_output.get("included_files_count", 0)
    exc_count = metadata_for_output.get("excluded_files_count", 0)
    total_size = metadata_for_output.get("total_content_size_kb", 0.0)

    log.info("-" * 30 + " SUMMARY " + "-" * 30)
    log.info(f"[log.summary_key]Total files included:[/log.summary_key] [log.summary_value_inc]{inc_count}[/log.summary_value_inc]")
    log.info(f"[log.summary_key]Total items excluded (files/dirs):[/log.summary_key] [log.summary_value_exc]{exc_count}[/log.summary_value_exc]")
    log.info(f"[log.summary_key]Total content size:[/log.summary_key] [log.summary_value_neutral]{total_size:.2f} KB[/log.summary_value_neutral]")
    log.info(f"[log.summary_key]Execution time:[/log.summary_key] [log.summary_value_neutral]{execution_time:.2f} seconds[/log.summary_value_neutral]")
    log.info("-" * (60 + len(" SUMMARY ")))
    
    will_log_debug_tree = False
    if log.isEnabledFor(logging.DEBUG):
        for handler in log.handlers:
            if handler.level <= logging.DEBUG:
                will_log_debug_tree = True
                break
    
    if will_log_debug_tree:
        import json as json_debugger 
        def json_default_serializer(obj):
            if isinstance(obj, pathlib.Path): return str(obj)
            return f"<not serializable: {type(obj).__name__}>"
        log.debug("CLI: --- Generated Data Tree (Debug from CLI) ---")
        try:
            json_tree_str = json_debugger.dumps(root_node, indent=2, default=json_default_serializer)
            log.debug(json_tree_str)
        except TypeError as e:
            log.debug(f"CLI: Error serializing data tree to JSON for debug: {e}")
        log.debug("CLI: --- End Generated Data Tree ---")

if __name__ == '__main__':
    main_cli()