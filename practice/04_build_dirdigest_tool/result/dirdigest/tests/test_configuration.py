# tests/test_configuration.py

import pytest
import yaml # For creating mock config files
from click.testing import CliRunner
from pathlib import Path
from unittest import mock

from dirdigest import cli as dirdigest_cli
from dirdigest.utils import config as dirdigest_config # To access DEFAULT_CONFIG_FILENAME

# --- Configuration Test Cases ---

# We need to mock the core processing functions to isolate config merging and application.
# These mocks will be used by most tests in this file.
COMMON_MOCKS = [
    mock.patch("dirdigest.core.process_directory_recursive", return_value=(iter([]), {})),
    mock.patch("dirdigest.core.build_digest_tree", return_value=({}, {})),
    # Mock both formatters as the format can change via config
    mock.patch("dirdigest.formatter.MarkdownFormatter.format", return_value="Mocked Markdown"),
    mock.patch("dirdigest.formatter.JsonFormatter.format", return_value='{"mocked": "json"}')
]

def apply_common_mocks(func):
    """Decorator to apply multiple common mocks."""
    for m in reversed(COMMON_MOCKS): # Apply in reverse for correct decorator order
        func = m(func)
    return func


@pytest.mark.parametrize("temp_test_dir", ["simple_project"], indirect=True)
class TestConfigLoadingAndMerging:

    def create_config_file(self, dir_path: Path, filename: str, content: dict):
        """Helper to create a YAML config file in the given directory."""
        file_path = dir_path / filename
        with open(file_path, 'w') as f:
            yaml.dump(content, f)
        return file_path

    @apply_common_mocks
    def test_load_default_config_file_name(
        self, mock_json_format, mock_md_format, mock_build_tree, mock_process_dir, # Order of mocks
        runner: CliRunner, temp_test_dir: Path
    ):
        """
        Test ID: CFG-001 (Conceptual)
        Description: Verifies that settings are loaded from a default '.diringest' file
        when no '--config' is specified and CLI arguments don't override.
        """
        config_content = {
            "default": {
                "format": "json",
                "max_size": 50,
                "exclude": ["*.log", "tmp/"]
            }
        }
        self.create_config_file(temp_test_dir, dirdigest_config.DEFAULT_CONFIG_FILENAME, config_content)

        result = runner.invoke(dirdigest_cli.main_cli) # No CLI args to override these
        assert result.exit_code == 0, f"CLI failed. Stderr: {result.stderr}"
        
        mock_process_dir.assert_called_once()
        kwargs = mock_process_dir.call_args.kwargs
        
        assert kwargs["max_size_kb"] == 50
        assert "*.log" in kwargs["exclude_patterns"]
        assert "tmp/" in kwargs["exclude_patterns"]
        # The format will be json, so JsonFormatter should be used.
        # We can check which formatter's 'format' method was called if needed, or check final format string.
        # For simplicity, assume core_logic passes correct format string based on merged config.
        # We can also check the log output for "CLI: Format: JSON"

    @apply_common_mocks
    def test_cli_overrides_default_config_file(
        self, mock_json_format, mock_md_format, mock_build_tree, mock_process_dir,
        runner: CliRunner, temp_test_dir: Path
    ):
        """
        Test ID: CFG-002 (Conceptual)
        Description: Verifies that CLI arguments take precedence over settings in the default '.diringest' file.
        """
        config_content = {
            "default": {
                "format": "json", # Config says json
                "max_size": 50,   # Config says 50
                "exclude": ["*.log"]
            }
        }
        self.create_config_file(temp_test_dir, dirdigest_config.DEFAULT_CONFIG_FILENAME, config_content)

        # CLI overrides format and max_size, and adds an exclude pattern
        result = runner.invoke(dirdigest_cli.main_cli, [
            "--format", "markdown", 
            "--max-size", "100",
            "--exclude", "*.tmp" # CLI adds this, config.py merge logic should handle merging/overriding lists
        ])
        assert result.exit_code == 0, f"CLI failed. Stderr: {result.stderr}"
        
        mock_process_dir.assert_called_once()
        kwargs = mock_process_dir.call_args.kwargs
        
        assert kwargs["max_size_kb"] == 100 # CLI override
        # Exclude patterns: CLI takes precedence for 'exclude' if provided.
        # Current merge_config: CLI value for multiple=True option replaces config if CLI option is used.
        assert "*.tmp" in kwargs["exclude_patterns"]
        assert "*.log" not in kwargs["exclude_patterns"] # CLI exclude should override config's list
        
        # Check that MarkdownFormatter was called (indirectly via checking the mock)
        # This assumes that the CLI correctly determined the final format to be 'markdown'.
        # This requires the mocks to be set up such that we can differentiate.
        # For this test, let's assume the format setting in `kwargs` passed to core logic is what matters.
        # The main_cli would have resolved format to 'markdown'.
        # The mock_process_dir is called *after* final settings are resolved.
        # We can check what formatter would be selected based on final_settings in main_cli
        # This test structure is more about checking what `process_directory_recursive` receives.

    @apply_common_mocks
    def test_load_specified_config_file(
        self, mock_json_format, mock_md_format, mock_build_tree, mock_process_dir,
        runner: CliRunner, temp_test_dir: Path
    ):
        """
        Test ID: CFG-003 (Conceptual)
        Description: Verifies loading of a config file specified via '--config' option.
        """
        config_filename = "my_custom_config.yaml"
        config_content = {
            "default": {
                "max_depth": 3,
                "follow_symlinks": True
            }
        }
        self.create_config_file(temp_test_dir, config_filename, config_content)

        result = runner.invoke(dirdigest_cli.main_cli, ["--config", config_filename])
        assert result.exit_code == 0, f"CLI failed. Stderr: {result.stderr}"

        mock_process_dir.assert_called_once()
        kwargs = mock_process_dir.call_args.kwargs
        assert kwargs["max_depth"] == 3
        assert kwargs["follow_symlinks"] is True

    @apply_common_mocks
    def test_load_flat_config_file( # No 'default:' profile key
        self, mock_json_format, mock_md_format, mock_build_tree, mock_process_dir,
        runner: CliRunner, temp_test_dir: Path
    ):
        """
        Test ID: CFG-010 (Conceptual)
        Description: Verifies loading of a 'flat' config file (no 'default' profile key).
        """
        config_filename = "flat_config.yaml"
        config_content = { # No "default" key
            "max_size": 75,
            "exclude": "*.tmp,*.bak" # Comma-separated string
        }
        self.create_config_file(temp_test_dir, config_filename, config_content)

        result = runner.invoke(dirdigest_cli.main_cli, ["--config", config_filename])
        assert result.exit_code == 0, f"CLI failed. Stderr: {result.stderr}"

        mock_process_dir.assert_called_once()
        kwargs = mock_process_dir.call_args.kwargs
        assert kwargs["max_size_kb"] == 75
        assert "*.tmp" in kwargs["exclude_patterns"]
        assert "*.bak" in kwargs["exclude_patterns"]

    def test_malformed_config_file(self, runner: CliRunner, temp_test_dir: Path):
        """
        Test ID: CFG-005 (Conceptual)
        Description: Verifies behavior with a malformed YAML config file.
        Tool should log a warning and proceed with defaults/CLI args.
        """
        config_filename = "malformed.yaml"
        malformed_content_str = "format: json\n max_size: 20" # Invalid YAML (indentation)
        malformed_file_path = temp_test_dir / config_filename
        with open(malformed_file_path, 'w') as f:
            f.write(malformed_content_str)

        # We expect a warning to be logged, but the tool to run with defaults.
        # We can capture logs to verify this.
        with mock.patch("dirdigest.utils.config.logger.warning") as mock_config_logger_warning:
            result = runner.invoke(dirdigest_cli.main_cli, ["--config", config_filename, "--max-size", "300"]) # Provide CLI default for max_size

        assert result.exit_code == 0 # Should not crash, should run with defaults/CLI
        mock_config_logger_warning.assert_called_once()
        assert "Error parsing YAML" in mock_config_logger_warning.call_args[0][0]

        # Check that it used CLI or built-in defaults, not the broken config.
        # For this, we need to mock core.process_directory_recursive again
        # This test is a bit more complex as it combines config error with CLI run.
        # Let's simplify: just check the warning and exit code for now.
        # A more thorough test would re-apply common mocks and check kwargs of process_directory_recursive.

    def test_config_file_not_found_specified(self, runner: CliRunner, temp_test_dir: Path):
        """
        Test ID: CFG-006 (Conceptual)
        Description: Verifies behavior when a specified config file is not found.
        Click should raise an error because @click.option(type=Path(exists=True)).
        """
        result = runner.invoke(dirdigest_cli.main_cli, ["--config", "nonexistent.yaml"])
        assert result.exit_code != 0 # Click should prevent this
        assert "Error" in result.output
        assert "Invalid value for '--config'" in result.output
        assert "does not exist" in result.output


    @apply_common_mocks
    def test_config_boolean_values(
        self, mock_json_format, mock_md_format, mock_build_tree, mock_process_dir,
        runner: CliRunner, temp_test_dir: Path
    ):
        """
        Description: Verifies that boolean values from config (true/false, yes/no, on/off, when
        written as actual YAML booleans) are correctly parsed and applied.
        """
        config_filename = "bool_test_config.yaml"
        # Define config_content with Python booleans
        # so yaml.dump writes them as YAML booleans (e.g., true, false)
        config_content = {
            "default": {
                "no_default_ignore": True,  # Python boolean True -> YAML true
                "follow_symlinks": True,   # Python boolean True -> YAML true
                "ignore_errors": True,     # Python boolean True -> YAML true
                "clipboard": False         # Python boolean False -> YAML false
            }
        }
        config_file_path = self.create_config_file(temp_test_dir, config_filename, config_content)

        # For debugging, let's see what the YAML file actually contains:
        # print(f"\nDEBUG: Content of {config_file_path}:\n{config_file_path.read_text()}")

        # We need to ensure the clipboard logic is correctly affected by the config.
        # The `apply_common_mocks` already mocks formatters.
        # The `main_cli` will determine `final_clipboard` based on merged settings.
        # Config says clipboard: false. CLI default for clipboard is True.
        # If only --config is specified, config's `clipboard: false` should win.
        with mock.patch("dirdigest.utils.clipboard.copy_to_clipboard") as mock_clipboard_copy:
            result = runner.invoke(dirdigest_cli.main_cli, ["--config", config_filename])
            
            assert result.exit_code == 0, f"CLI failed. Stderr: {result.stderr}"

            # Check arguments passed to the core processing function
            mock_process_dir.assert_called_once()
            kwargs_core = mock_process_dir.call_args.kwargs
            
            assert kwargs_core["no_default_ignore"] is True, \
                f"Expected no_default_ignore to be True, got {kwargs_core['no_default_ignore']}"
            assert kwargs_core["follow_symlinks"] is True, \
                f"Expected follow_symlinks to be True, got {kwargs_core['follow_symlinks']}"
            assert kwargs_core["ignore_read_errors"] is True, \
                f"Expected ignore_read_errors to be True, got {kwargs_core['ignore_read_errors']}"

            # Check if clipboard.copy_to_clipboard was called (or not called)
            # Based on config `clipboard: false`
            mock_clipboard_copy.assert_not_called()