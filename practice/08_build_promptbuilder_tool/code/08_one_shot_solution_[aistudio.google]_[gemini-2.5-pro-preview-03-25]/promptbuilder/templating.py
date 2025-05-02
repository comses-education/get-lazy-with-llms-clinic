import logging
from pathlib import Path
from typing import Dict, Any, Optional

from jinja2 import Environment, FileSystemLoader, TemplateNotFound, select_autoescape

from .config import Config

logger = logging.getLogger(__name__)

def render_meta_prompt(
    template_path: Path,
    data: Dict[str, Any],
    config: Config
) -> Optional[str]:
    """Renders the meta prompt using Jinja2."""
    try:
        # Ensure template_path is absolute or relative to CWD if not found directly
        if not template_path.is_absolute() and not template_path.exists():
             lookup_path = Path.cwd() / template_path
             if lookup_path.exists():
                 template_path = lookup_path

        if not template_path.is_file():
             logger.error(f"Template file not found: {template_path}")
             return None

        logger.info(f"Using template file: {template_path}")
        template_dir = template_path.parent
        template_filename = template_path.name

        env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(), # Basic protection
            trim_blocks=True,
            lstrip_blocks=True
        )

        # Add placeholder format to the data for easy access in the template
        data['placeholder'] = lambda name: config.placeholder_format % name.upper()

        template = env.get_template(template_filename)
        rendered_prompt = template.render(data)
        logger.debug("Template rendering successful.")
        return rendered_prompt

    except TemplateNotFound:
        logger.error(f"Template not found in directory {template_dir}: {template_filename}")
        return None
    except Exception as e:
        logger.error(f"Error rendering template {template_path}: {e}")
        return None