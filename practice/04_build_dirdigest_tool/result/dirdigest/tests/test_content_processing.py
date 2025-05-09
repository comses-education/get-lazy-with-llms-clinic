# tests/test_content_processing.py

import pytest
import json
from click.testing import CliRunner
from pathlib import Path
from unittest import mock
import os # For os.chmod
import stat # For permission bits

from dirdigest import cli as dirdigest_cli

# Helper functions (get_file_node_from_json, get_all_included_file_paths) remain the same...
# For brevity, I'll omit them here. Assume they are present and correct.

def get_file_node_from_json(json_output_str: str, relative_path: str) -> dict | None:
    try:
        data = json.loads(json_output_str)
    except json.JSONDecodeError:
        pytest.fail(f"Output was not valid JSON for get_file_node: {json_output_str}")
    queue = [data.get("root")]
    while queue:
        node = queue.pop(0)
        if not node: continue
        if node.get("type") == "file" and node.get("relative_path") == relative_path:
            return node
        if "children" in node and isinstance(node["children"], list):
            queue.extend(node["children"])
    return None

def get_all_included_file_paths(json_output_str: str) -> set[str]:
    try:
        data = json.loads(json_output_str)
    except json.JSONDecodeError as e: 
        pytest.fail(f"Output was not valid JSON for helper. Error: {e}. Output: '{json_output_str[:500]}...'")
    included_files = set()
    def recurse_node(node):
        if node.get("type") == "file" and "relative_path" in node:
            included_files.add(node["relative_path"])
        if "children" in node and isinstance(node["children"], list):
            for child in node["children"]:
                recurse_node(child)
    if "root" in data:
        recurse_node(data["root"])
    return included_files

# TestMaxSizeHandling class remains the same... (assuming it was correct)
@pytest.mark.parametrize("temp_test_dir", ["content_processing_dir"], indirect=True)
class TestMaxSizeHandling:
    def run_dirdigest_and_get_json(self, runner: CliRunner, max_size_kb: int) -> str:
        json_output_str = ""
        cli_args = ["--format", "json", "--no-default-ignore", "--max-size", str(max_size_kb), "--no-clipboard"]
        with mock.patch("dirdigest.utils.logger.stdout_console.print") as mock_rich_print:
            result = runner.invoke(dirdigest_cli.main_cli, cli_args)
            if mock_rich_print.call_args_list:
                json_output_str = "".join(str(call.args[0]) for call in mock_rich_print.call_args_list if call.args)
        assert result.exit_code == 0, f"CLI failed for max-size {max_size_kb}. Stderr: {result.stderr}"
        return json_output_str

    def test_file_below_max_size(self, runner: CliRunner, temp_test_dir: Path):
        json_output = self.run_dirdigest_and_get_json(runner, 10)
        included_files = get_all_included_file_paths(json_output)
        assert "small_file.txt" in included_files
        file_node = get_file_node_from_json(json_output, "small_file.txt")
        assert file_node is not None and "content" in file_node and file_node["content"] is not None

    def test_file_at_max_size(self, runner: CliRunner, temp_test_dir: Path):
        json_output = self.run_dirdigest_and_get_json(runner, 10)
        included_files = get_all_included_file_paths(json_output)
        assert "exact_size_file.txt" in included_files
        file_node = get_file_node_from_json(json_output, "exact_size_file.txt")
        assert file_node is not None and "content" in file_node and file_node["content"] is not None

    def test_file_above_max_size(self, runner: CliRunner, temp_test_dir: Path):
        json_output = self.run_dirdigest_and_get_json(runner, 10)
        included_files = get_all_included_file_paths(json_output)
        assert "large_file.txt" not in included_files

    def test_empty_file_inclusion(self, runner: CliRunner, temp_test_dir: Path):
        json_output = self.run_dirdigest_and_get_json(runner, 300)
        included_files = get_all_included_file_paths(json_output)
        assert "empty_file.txt" in included_files
        file_node = get_file_node_from_json(json_output, "empty_file.txt")
        assert file_node is not None and file_node.get("content") == ""
        assert file_node.get("size_kb") == 0.0


@pytest.mark.parametrize("temp_test_dir", ["content_processing_dir"], indirect=True)
class TestErrorHandling:
    """Tests for --ignore-errors and handling of unreadable/problematic files."""

    def run_dirdigest_get_json_and_node(
        self, 
        runner: CliRunner, 
        temp_dir_path: Path, # temp_test_dir fixture value
        file_to_check: str, 
        cli_flags: list[str],
        make_unreadable: bool = False # New flag
    ):
        json_output_str = ""
        base_args = ["--format", "json", "--no-default-ignore", "--no-clipboard"] + cli_flags
        
        # Path to the file within the temporary test directory
        # The temp_test_dir fixture has already changed CWD to temp_dir_path
        file_in_temp_dir = Path(file_to_check) 

        original_permissions = None
        if make_unreadable and file_in_temp_dir.exists():
            try:
                original_permissions = file_in_temp_dir.stat().st_mode
                # Remove all permissions: 000
                os.chmod(file_in_temp_dir, 0o000) 
            except OSError as e:
                pytest.skip(f"Could not set permissions for {file_in_temp_dir} to test permission denial. Error: {e}")


        try:
            with mock.patch("dirdigest.utils.logger.stdout_console.print") as mock_rich_print:
                # Important: dirdigest will run in the CWD, which is temp_dir_path
                result = runner.invoke(dirdigest_cli.main_cli, base_args) # Uses current dir (temp_dir_path)
                if mock_rich_print.call_args_list:
                    json_output_str = "".join(str(call.args[0]) for call in mock_rich_print.call_args_list if call.args)
            assert result.exit_code == 0, f"CLI failed. Args:{base_args}. Stderr: {result.stderr}"
            
            parsed_json = json.loads(json_output_str)
            file_node = get_file_node_from_json(json_output_str, file_to_check)
            return parsed_json, file_node

        finally:
            # Restore permissions if they were changed
            if make_unreadable and original_permissions is not None and file_in_temp_dir.exists():
                try:
                    os.chmod(file_in_temp_dir, original_permissions)
                except OSError as e:
                    # Log or note this, but don't fail the test itself if restoration fails
                    print(f"Warning: Failed to restore permissions for {file_in_temp_dir}. Error: {e}")


    def test_permission_denied_no_ignore_errors(self, runner: CliRunner, temp_test_dir: Path):
        """Test ID: CPS-005. File with permission error is excluded if --ignore-errors is false (default)."""
        _full_json, file_node = self.run_dirdigest_get_json_and_node(
            runner, temp_test_dir, "permission_denied_file.txt", [], make_unreadable=True
        )
        assert file_node is None, "File with permission error was included when it should be excluded."

    def test_permission_denied_with_ignore_errors(self, runner: CliRunner, temp_test_dir: Path):
        """Test ID: CPS-006. File with permission error is included (with error noted) if --ignore-errors is true."""
        _full_json, file_node = self.run_dirdigest_get_json_and_node(
            runner, temp_test_dir, "permission_denied_file.txt", ["--ignore-errors"], make_unreadable=True
        )
        assert file_node is not None, "File with permission error was not included with --ignore-errors."
        assert "read_error" in file_node, "Read error not noted for permission_denied_file."
        assert file_node.get("content") is None 

    def test_binary_file_no_ignore_errors(self, runner: CliRunner, temp_test_dir: Path):
        """Test ID: CPS-007. Binary file (decode error) is excluded if --ignore-errors is false."""
        _full_json, file_node = self.run_dirdigest_get_json_and_node(
            runner, temp_test_dir, "binary_file.bin", []
        )
        assert file_node is None, "Binary file was included when it should be excluded due to decode error."

    def test_binary_file_with_ignore_errors(self, runner: CliRunner, temp_test_dir: Path):
        """Test ID: CPS-008. Binary file (decode error) is included (with error noted) if --ignore-errors is true."""
        _full_json, file_node = self.run_dirdigest_get_json_and_node(
            runner, temp_test_dir, "binary_file.bin", ["--ignore-errors"]
        )
        assert file_node is not None, "Binary file was not included with --ignore-errors."
        assert "read_error" in file_node, "Read error not noted for binary_file."
        assert "UnicodeDecodeError" in file_node["read_error"], "Error message should mention UnicodeDecodeError."
        assert file_node.get("content") is None

    def test_utf8_chars_file_reading(self, runner: CliRunner, temp_test_dir: Path):
        """Test ID: CPS-009 (Conceptual). Standard UTF-8 file with various characters is read correctly."""
        _full_json, file_node = self.run_dirdigest_get_json_and_node(
            runner, temp_test_dir, "utf8_chars.txt", []
        )
        assert file_node is not None, "UTF-8 test file not included."
        assert "read_error" not in file_node, "UTF-8 test file has unexpected read_error."
        assert "你好世界" in file_node.get("content", ""), "UTF-8 content not read correctly."
        assert "Привет" in file_node.get("content", "")
        assert "€αβγ" in file_node.get("content", "")