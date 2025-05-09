# tests/conftest.py
import pytest
import shutil
import os
from pathlib import Path
from click.testing import CliRunner
from unittest import mock

# Define the root for mock directory structures, relative to this conftest.py file
MOCK_DIRS_ROOT = Path(__file__).parent / "fixtures" / "test_dirs"

@pytest.fixture
def runner() -> CliRunner:
    """Provides a Click CliRunner instance for invoking CLI commands."""
    return CliRunner()

@pytest.fixture
def temp_test_dir(tmp_path: Path, request):
    """
    Creates a temporary directory, copies a specified mock directory structure into it,
    changes the current working directory to it for the duration of the test,
    and cleans up afterward.

    To use, decorate your test function with:
    @pytest.mark.parametrize("temp_test_dir", ["name_of_mock_dir"], indirect=True)
    'name_of_mock_dir' should be a subdirectory under tests/fixtures/test_dirs/
    The fixture will yield the Path object to the created temporary test directory.
    """
    mock_dir_name = request.param
    source_path = MOCK_DIRS_ROOT / mock_dir_name

    if not source_path.is_dir():
        # Oh, for crying out loud! If the mock directory isn't there, what are we even DOING?!
        # It's like planning a picnic and forgetting the food, the basket, AND the park.
        raise ValueError(
            f"Mock directory '{mock_dir_name}' not found at '{source_path}'. "
            "Did you create it under tests/fixtures/test_dirs/?"
        )

    test_specific_tmp_dir = tmp_path / mock_dir_name
    
    # CRITICAL FIX FOR SYMLINK TESTS: Add symlinks=True
    shutil.copytree(source_path, test_specific_tmp_dir, symlinks=True) 

    original_cwd = Path.cwd()
    os.chdir(test_specific_tmp_dir)
    
    try:
        yield test_specific_tmp_dir
    finally:
        os.chdir(original_cwd)

@pytest.fixture
def mock_pyperclip(monkeypatch):
    """
    Mocks pyperclip.copy and pyperclip.paste.
    The mock_copy function stores the copied text in clipboard_content["text"].
    Returns a tuple: (mock_copy_object, mock_paste_object, clipboard_content_dict).
    """
    mock_copy_object = mock.MagicMock()
    mock_paste_object = mock.MagicMock(return_value="")
    clipboard_content_dict = {"text": None}

    def custom_pyperclip_copy(text_to_copy):
        clipboard_content_dict["text"] = text_to_copy
        mock_copy_object(text_to_copy)

    def custom_pyperclip_paste():
        return mock_paste_object()

    monkeypatch.setattr("dirdigest.utils.clipboard.pyperclip.copy", custom_pyperclip_copy)
    monkeypatch.setattr("dirdigest.utils.clipboard.pyperclip.paste", custom_pyperclip_paste)
    
    try:
        import pyperclip 
        mock_copy_object.PyperclipException = pyperclip.PyperclipException
        mock_paste_object.PyperclipException = pyperclip.PyperclipException
    except ImportError:
        class DummyPyperclipException(Exception):
            pass
        mock_copy_object.PyperclipException = DummyPyperclipException
        mock_paste_object.PyperclipException = DummyPyperclipException

    return mock_copy_object, mock_paste_object, clipboard_content_dict