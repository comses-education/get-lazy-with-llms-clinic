import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Rich imports (only needed for direct printing, logger handles most)
# from rich.console import Console

from jinja2 import Environment, FileSystemLoader, TemplateNotFound, select_autoescape

from .config import Config

# Use logger configured in cli.py
logger = logging.getLogger(__name__)

def render_meta_prompt(
    template_path: Path,
    data: Dict[str, Any],
    config: Config,
    console: 'Console' # Type hint for console
) -> Optional[str]:
    """Renders the meta prompt using Jinja2."""
    try:
        # Ensure template_path is absolute or relative to CWD if not found directly
        if not template_path.is_absolute():
            # Try relative to CWD first
            lookup_path_cwd = Path.cwd() / template_path
            # Try relative to config file location? (More complex)
            # Try relative to default template dir? (Maybe confusing)
            if lookup_path_cwd.is_file():
                 template_path = lookup_path_cwd
            # If still not found, FileSystemLoader might find it if it's relative to *its* search path (template_dir)

        if not template_path.is_file():
             # Use logger for error, RichHandler will format it
             logger.error(f"Template file not found: [red]{template_path}[/red]")
             # Maybe try the default template as a fallback?
             default_template = config.default_meta_prompt_template_path
             if default_template.is_file() and template_path != default_template:
                 logger.warning(f"Falling back to default template: [blue]{default_template}[/blue]")
                 template_path = default_template
             else:
                 logger.error("Default template also not found or is the same as the missing one. Cannot render.")
                 return None # Exit if no template is usable


        logger.info(f"Using template file: [blue]{template_path.resolve()}[/blue]")
        template_dir = template_path.parent
        template_filename = template_path.name

        env = Environment(
            loader=FileSystemLoader(template_dir, followlinks=True), # Allow symlinks if needed
            autoescape=select_autoescape(['html', 'xml']), # Autoescape common web formats if template generates them
            trim_blocks=True,
            lstrip_blocks=True,
            enable_async=False # Ensure Jinja2 runs synchronously
        )

        # Add placeholder function directly to the template context
        data['placeholder'] = lambda name: config.placeholder_format % name.upper()
        # Add config object directly to context
        data['config'] = config

        template = env.get_template(template_filename)
        rendered_prompt = template.render(data)
        logger.debug("Template rendering successful.")
        return rendered_prompt.strip() # Strip leading/trailing whitespace from final render

    except TemplateNotFound:
        logger.error(f"Template [red]{template_filename}[/red] not found in directory [blue]{template_dir}[/blue]")
        return None
    except Exception as e:
        # Log the error with traceback using RichHandler
        logger.error(f"Error rendering template [red]{template_path}[/red]: {e}", exc_info=True)
        return None