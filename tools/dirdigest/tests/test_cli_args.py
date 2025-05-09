import pytest
from click.testing import CliRunner
from unittest import mock
from pathlib import Path 
from dirdigest import cli as dirdigest_cli
from dirdigest.constants import TOOL_NAME, TOOL_VERSION

# --- Existing passing tests ---

def test_cli_help_short_option(runner: CliRunner):
    """
    Test ID: CLI-023 (Conceptual)
    Description: Verifies that the '-h' option displays the help message and exits successfully.
    Checks for basic usage string and presence of a known option in the output.
    """
    result = runner.invoke(dirdigest_cli.main_cli, ["-h"])
    assert result.exit_code == 0
    assert "Usage: dirdigest [OPTIONS] DIRECTORY" in result.output 
    assert TOOL_NAME in result.output 
    assert "--output" in result.output

def test_cli_help_long_option(runner: CliRunner):
    """
    Test ID: CLI-023 (Conceptual)
    Description: Verifies that the '--help' option displays the help message and exits successfully.
    Checks for basic usage string and presence of a known option in the output.
    """
    result = runner.invoke(dirdigest_cli.main_cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage: dirdigest [OPTIONS] DIRECTORY" in result.output
    assert "--include" in result.output

def test_cli_version_option(runner: CliRunner):
    """
    Test ID: CLI-024 (Conceptual)
    Description: Verifies that the '--version' option displays the tool's name and version, then exits.
    """
    result = runner.invoke(dirdigest_cli.main_cli, ["--version"])
    assert result.exit_code == 0
    expected_output_start = f"{TOOL_NAME} version {TOOL_VERSION}"
    assert result.output.strip().startswith(expected_output_start)

@pytest.mark.parametrize("temp_test_dir", ["simple_project"], indirect=True)
def test_cli_basic_invocation_no_args(runner: CliRunner, temp_test_dir):
    """
    Test ID: CLI-001 (Conceptual)
    Description: Tests basic invocation with no arguments in a mock directory.
    Verifies that the tool runs successfully (exit code 0) and produces some expected Markdown output
    by checking for header and known filenames from the 'simple_project' fixture.
    Output is captured by mocking the Rich console's print method.
    """
    with mock.patch("dirdigest.utils.logger.stdout_console.print") as mock_rich_print:
        result = runner.invoke(dirdigest_cli.main_cli) 
    
        assert result.exit_code == 0, f"CLI failed with output:\n{result.output}\nStderr:\n{result.stderr}"
        
        printed_output_segments = []
        for call_args_item in mock_rich_print.call_args_list:
            if call_args_item.args:
                printed_output_segments.append(str(call_args_item.args[0]))
        actual_stdout_content = "".join(printed_output_segments)

        assert actual_stdout_content is not None, "stdout_console.print was not called"
        assert len(actual_stdout_content) > 0, "stdout_console.print was called with empty string or not captured"
        assert "# Directory Digest" in actual_stdout_content
        assert "file1.txt" in actual_stdout_content 
        assert "file2.md" in actual_stdout_content # Based on last passing test run output
        assert "sub_dir1/script.py" in actual_stdout_content

@pytest.mark.parametrize("temp_test_dir", ["simple_project"], indirect=True)
def test_cli_non_existent_directory_arg(runner: CliRunner, temp_test_dir):
    """
    Test ID: CLI-021 (Conceptual)
    Description: Verifies that providing a non-existent directory path as the main argument
    results in a non-zero exit code and an appropriate error message from Click.
    """
    result = runner.invoke(dirdigest_cli.main_cli, ["non_existent_dir"])
    assert result.exit_code != 0
    assert "Error" in result.output 
    assert "does not exist" in result.output


@pytest.mark.parametrize("temp_test_dir", ["simple_project"], indirect=True)
def test_cli_file_as_directory_arg(runner: CliRunner, temp_test_dir):
    """
    Test ID: CLI-022 (Conceptual)
    Description: Verifies that providing an existing file path (instead of a directory)
    as the main argument results in a non-zero exit code and an error message.
    """
    file_path_arg = "file1.txt" 
    result = runner.invoke(dirdigest_cli.main_cli, [file_path_arg])
    assert result.exit_code != 0
    assert "Error" in result.output
    assert "is a file" in result.output

# --- New tests for more CLI arguments ---

@pytest.mark.parametrize("temp_test_dir", ["simple_project"], indirect=True)
def test_cli_output_option(runner: CliRunner, temp_test_dir: Path):
    """
    Test ID: CLI-003 (Conceptual)
    Description: Tests the '--output <filepath>' option.
    Verifies that the command runs successfully and creates the specified output file
    containing expected digest content (e.g., Markdown header and a known filename).
    """
    output_filename = "my_digest.md"
    # temp_test_dir fixture changes CWD, so output_filename is relative to it.
    output_file_path = Path(output_filename) 

    result = runner.invoke(dirdigest_cli.main_cli, ["--output", output_filename])
    
    assert result.exit_code == 0, f"CLI failed. Stderr: {result.stderr}"
    assert output_file_path.exists(), f"Output file {output_file_path} was not created."
    assert output_file_path.is_file()
    
    content = output_file_path.read_text()
    assert "# Directory Digest" in content
    assert "file1.txt" in content

@pytest.mark.parametrize("temp_test_dir", ["simple_project"], indirect=True)
def test_cli_format_json_option(runner: CliRunner, temp_test_dir: Path):
    """
    Test ID: CLI-004 (Conceptual) / JSON-001 (Conceptual)
    Description: Tests the '--format json' option, directing output to a file.
    Verifies successful execution, creation of the JSON output file,
    valid JSON content, and presence of key structures ('metadata', 'root') and expected data.
    """
    output_filename = "digest.json"
    output_file_path = Path(output_filename)

    result = runner.invoke(dirdigest_cli.main_cli, ["--format", "json", "--output", output_filename])
    assert result.exit_code == 0, f"CLI failed. Stderr: {result.stderr}"
    
    assert output_file_path.exists()
    content = output_file_path.read_text()
    
    import json 
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"Output was not valid JSON: {content}")

    assert "metadata" in data
    assert "root" in data
    assert data["metadata"]["tool_version"] == TOOL_VERSION
    # Check for an expected file in the JSON structure's children
    found_file = False
    if "children" in data["root"]:
        for child in data["root"]["children"]:
            if child.get("type") == "file" and child.get("relative_path") == "file1.txt":
                found_file = True
                break
    assert found_file, "Expected file 'file1.txt' not found in JSON root children."


@pytest.mark.parametrize("temp_test_dir", ["simple_project"], indirect=True)
def test_cli_invalid_format_option(runner: CliRunner, temp_test_dir: Path):
    """
    Test ID: (Implied by CLI argument validation)
    Description: Tests providing an invalid value (e.g., 'xml') to the '--format' option.
    Verifies that the command fails with a non-zero exit code and Click displays
    an appropriate error message about the invalid choice.
    """
    result = runner.invoke(dirdigest_cli.main_cli, ["--format", "xml"]) 
    assert result.exit_code != 0 
    assert "Error" in result.output 
    assert "Invalid value for '--format' / '-f'" in result.output


@mock.patch("dirdigest.core.process_directory_recursive")
@mock.patch("dirdigest.core.build_digest_tree") 
@mock.patch("dirdigest.formatter.MarkdownFormatter.format", return_value="Mocked Markdown") 
@pytest.mark.parametrize("temp_test_dir", ["simple_project"], indirect=True)
def test_cli_include_option_parsing(
    mock_md_format, mock_build_tree, mock_process_dir, 
    runner: CliRunner, temp_test_dir: Path
):
    """
    Test ID: CLI-005 (Conceptual)
    Description: Verifies that multiple '--include' options are correctly parsed from the CLI
    and passed as a list of patterns to the core processing function.
    Mocks core functions to isolate CLI parsing.
    """
    mock_process_dir.return_value = (iter([]), {}) 
    mock_build_tree.return_value = ({}, {}) 

    runner.invoke(dirdigest_cli.main_cli, ["--include", "*.py", "--include", "docs/"])
    
    mock_process_dir.assert_called_once()
    kwargs = mock_process_dir.call_args.kwargs
    
    assert "*.py" in kwargs["include_patterns"]
    assert "docs/" in kwargs["include_patterns"]
    assert len(kwargs["include_patterns"]) == 2


@mock.patch("dirdigest.core.process_directory_recursive")
@mock.patch("dirdigest.core.build_digest_tree", return_value=({}, {}))
@mock.patch("dirdigest.formatter.MarkdownFormatter.format", return_value="Mocked Markdown")
@pytest.mark.parametrize("temp_test_dir", ["simple_project"], indirect=True)
def test_cli_exclude_option_parsing_comma_separated(
    mock_md_format, mock_build_tree, mock_process_dir,
    runner: CliRunner, temp_test_dir: Path
):
    """
    Test ID: CLI-008 (Conceptual)
    Description: Verifies that a comma-separated list provided to '--exclude' option
    is correctly parsed into multiple distinct patterns and passed to the core processing function.
    Mocks core functions.
    """
    mock_process_dir.return_value = (iter([]), {})
    
    runner.invoke(dirdigest_cli.main_cli, ["--exclude", "*.log,tmp/"])
    
    mock_process_dir.assert_called_once()
    kwargs = mock_process_dir.call_args.kwargs
    
    assert "*.log" in kwargs["exclude_patterns"]
    assert "tmp/" in kwargs["exclude_patterns"]
    assert len(kwargs["exclude_patterns"]) == 2


@mock.patch("dirdigest.core.process_directory_recursive")
@mock.patch("dirdigest.core.build_digest_tree", return_value=({}, {}))
@mock.patch("dirdigest.formatter.MarkdownFormatter.format", return_value="Mocked Markdown")
@pytest.mark.parametrize("temp_test_dir", ["simple_project"], indirect=True)
def test_cli_max_size_option_parsing(
    mock_md_format, mock_build_tree, mock_process_dir,
    runner: CliRunner, temp_test_dir: Path
):
    """
    Test ID: CLI-010 (Conceptual)
    Description: Verifies that the '--max-size' option (integer value) is correctly parsed
    and passed as 'max_size_kb' to the core processing function. Mocks core functions.
    """
    mock_process_dir.return_value = (iter([]), {})
    
    runner.invoke(dirdigest_cli.main_cli, ["--max-size", "500"]) 
    
    mock_process_dir.assert_called_once()
    kwargs = mock_process_dir.call_args.kwargs
    assert kwargs["max_size_kb"] == 500


@mock.patch("dirdigest.core.process_directory_recursive")
@mock.patch("dirdigest.core.build_digest_tree", return_value=({}, {}))
@mock.patch("dirdigest.formatter.MarkdownFormatter.format", return_value="Mocked Markdown")
@pytest.mark.parametrize("temp_test_dir", ["simple_project"], indirect=True)
def test_cli_max_depth_option_parsing(
    mock_md_format, mock_build_tree, mock_process_dir,
    runner: CliRunner, temp_test_dir: Path
):
    """
    Test ID: CLI-012 (Conceptual)
    Description: Verifies that the '--max-depth' option (integer value) is correctly parsed
    and passed to the core processing function. Mocks core functions.
    """
    mock_process_dir.return_value = (iter([]), {})

    runner.invoke(dirdigest_cli.main_cli, ["--max-depth", "3"])
    
    mock_process_dir.assert_called_once()
    kwargs = mock_process_dir.call_args.kwargs
    assert kwargs["max_depth"] == 3


@pytest.mark.parametrize(
    "flag_name, arg_name_in_core, expected_value",
    [
        ("--no-default-ignore", "no_default_ignore", True),    # CLI-013
        ("--follow-symlinks", "follow_symlinks", True),      # CLI-014
        ("--ignore-errors", "ignore_read_errors", True),      # CLI-015
    ]
)
@mock.patch("dirdigest.core.process_directory_recursive")
@mock.patch("dirdigest.core.build_digest_tree", return_value=({}, {}))
@mock.patch("dirdigest.formatter.MarkdownFormatter.format", return_value="Mocked Markdown")
@pytest.mark.parametrize("temp_test_dir", ["simple_project"], indirect=True) 
def test_cli_boolean_flags_for_core(
    mock_md_format, mock_build_tree, mock_process_dir, 
    runner: CliRunner, temp_test_dir: Path,              
    flag_name: str, arg_name_in_core: str, expected_value: bool 
):
    """
    Test IDs: CLI-013, CLI-014, CLI-015 (Conceptual)
    Description: Tests various boolean flags (e.g., '--no-default-ignore') and verifies
    that they correctly set the corresponding boolean argument in the call
    to the core processing function. Mocks core functions. Parametrized for different flags.
    """
    mock_process_dir.return_value = (iter([]), {})

    runner.invoke(dirdigest_cli.main_cli, [flag_name])
    
    mock_process_dir.assert_called_once()
    kwargs = mock_process_dir.call_args.kwargs
    assert kwargs.get(arg_name_in_core) == expected_value


@mock.patch("dirdigest.utils.clipboard.copy_to_clipboard")
@pytest.mark.parametrize("temp_test_dir", ["simple_project"], indirect=True)
def test_cli_no_clipboard_option(mock_copy_to_clipboard, runner: CliRunner, temp_test_dir: Path):
    """
    Test ID: CLI-016 (Conceptual)
    Description: Verifies that using the '--no-clipboard' option prevents the
    'copy_to_clipboard' function from being called. Mocks the clipboard function.
    """
    with mock.patch("dirdigest.utils.logger.stdout_console.print"): 
        result = runner.invoke(dirdigest_cli.main_cli, ["--no-clipboard"])

    assert result.exit_code == 0
    mock_copy_to_clipboard.assert_not_called()


@mock.patch("dirdigest.utils.clipboard.copy_to_clipboard")
@pytest.mark.parametrize("temp_test_dir", ["simple_project"], indirect=True)
def test_cli_clipboard_called_by_default(mock_copy_to_clipboard, runner: CliRunner, temp_test_dir: Path):
    """
    Test ID: (Implied by default behavior of -c/--clipboard)
    Description: Verifies that by default (without '--no-clipboard'), the 'copy_to_clipboard'
    function IS called, assuming successful output generation. Mocks the clipboard function.
    """
    with mock.patch("dirdigest.utils.logger.stdout_console.print"): 
        result = runner.invoke(dirdigest_cli.main_cli) 

    assert result.exit_code == 0
    mock_copy_to_clipboard.assert_called_once()
    # Optional: Check content passed to clipboard
    # args, _ = mock_copy_to_clipboard.call_args
    # assert "# Directory Digest" in args[0]