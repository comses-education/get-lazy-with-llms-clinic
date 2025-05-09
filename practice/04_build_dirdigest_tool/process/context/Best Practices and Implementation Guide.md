# Building the `dirdigest` CLI Tool: Best Practices and Implementation Guide

## Table of Contents
- [Introduction](#introduction)
- [Best Practices for Python CLI Applications](#best-practices-for-python-cli-applications)
- [CLI Framework Selection](#cli-framework-selection)
- [Directory Traversal and File Handling](#directory-traversal-and-file-handling)
- [Pattern Matching and Filtering](#pattern-matching-and-filtering)
- [Output Formatting](#output-formatting)
- [Clipboard Integration](#clipboard-integration)
- [Testing CLI Applications](#testing-cli-applications)
- [Project Structure](#project-structure)
- [Implementation Recommendations](#implementation-recommendations)

## Introduction

This guide provides best practices and implementation advice for building `dirdigest`, a Python command-line tool that processes directories recursively to create structured digests in markdown or JSON format.

## Best Practices for Python CLI Applications

### 1. Framework Selection

Choose a robust CLI framework rather than manually parsing arguments. Popular options include:

- **Click**: Offers composable command interfaces, nested commands, and automatic help generation
- **argparse**: Standard library solution with extensive customization options
- **Typer**: Modern library built on top of Click with type annotations focus

Click is particularly well-suited for `dirdigest` due to its:
- Arbitrary nesting of commands
- Automatic help page generation
- Support for context passing between commands

### 2. Separation of Concerns

Modular design is crucial for maintainable CLI applications:

```
# BAD: Logic and interface mixed together
def main():
    args = parse_args()
    if args.command == 'process':
        # All processing logic directly here
    # ...

# GOOD: Separation of concerns
def main():
    args = parse_args()
    if args.command == 'process':
        process_command(args)
    # ...
```

Clearly separate your code into:
1. CLI interface layer (argument parsing)
2. Business logic (core functionality)
3. Presentation layer (output formatting)

This separation makes testing easier and enables multiple interface options (CLI, API, etc.).

### 3. Human-Friendly Output

Make your CLI output user-friendly:

- Use the `rich` library for beautiful terminal output with minimal effort
- Implement color-coding for different types of information
- Design a clear, consistent output format
- Include progress indicators for lengthy operations
- Provide different verbosity levels

Example using `rich`:

```python
from rich.console import Console
from rich.tree import Tree

console = Console()

def display_directory_tree(path):
    tree = Tree(f"[bold blue]{path}[/bold blue]")
    # Add items to tree
    console.print(tree)
```

### 4. Distribution and Packaging

- Package your CLI tool properly to make it easily installable:
  ```python
  # setup.py
  setup(
      name="dirdigest",
      version="0.1.0",
      py_modules=["dirdigest"],
      install_requires=["click", "rich", "pyperclip"],
      entry_points="""
          [console_scripts]
          dirdigest=dirdigest.cli:main
      """,
  )
  ```
- Consider distributing as a single file if possible to minimize dependencies
- Use proper versioning for your CLI tool

## CLI Framework Selection

For the `dirdigest` tool, Click is particularly well-suited:

```python
import click

@click.group()
@click.version_option()
def cli():
    """Directory digest tool for creating structured directory summaries."""
    pass

@cli.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False), default='.')
@click.option('--output', '-o', type=click.Path(), help='Output file path (default: stdout)')
@click.option('--format', '-f', type=click.Choice(['json', 'markdown']), default='markdown', 
              help='Output format')
def process(directory, output, format):
    """Process a directory and create a structured digest."""
    # Implementation here
    
if __name__ == '__main__':
    cli()
```

Benefits of Click for this project:
- Context passing between commands (useful for configuration passing)
- Nested commands for potential future extensions
- Type validation for arguments (path handling, format choices)

## Directory Traversal and File Handling

### Efficient Directory Traversal

Use `os.walk()` for recursive directory traversal with additional filtering:

```python
def traverse_directory(directory, max_depth=None, follow_symlinks=False):
    current_depth = 0
    for root, dirs, files in os.walk(directory, followlinks=follow_symlinks):
        # Calculate current depth
        rel_path = os.path.relpath(root, directory)
        if rel_path == '.':
            current_depth = 0
        else:
            current_depth = rel_path.count(os.sep) + 1
            
        # Skip if we've reached max depth
        if max_depth is not None and current_depth >= max_depth:
            del dirs[:]  # Prevent further recursion
            continue
            
        # Process files and directories
        yield root, dirs, files
```

The `scandir()` function provides better performance than older methods:

```python
import os

def fast_traverse(directory):
    with os.scandir(directory) as it:
        for entry in it:
            yield entry
```

This is 2-20 times faster than using `os.listdir()` and `os.path.isdir()` separately.

### Directory Tree Representation

For directory structures, create a nested dictionary representation:

```python
def path_to_dict(path, max_size, include_patterns, exclude_patterns):
    result = {'name': os.path.basename(path)}
    
    if os.path.isdir(path):
        result['type'] = "directory"
        children = []
        
        with os.scandir(path) as it:
            for entry in it:
                # Apply filtering logic here
                if should_include(entry.path, include_patterns, exclude_patterns):
                    children.append(path_to_dict(entry.path, max_size, include_patterns, exclude_patterns))
        
        result['children'] = children
    else:
        result['type'] = "file"
        result['size_kb'] = os.path.getsize(path) / 1024
        
        # Only include content if file is small enough
        if result['size_kb'] <= max_size:
            with open(path, 'r', errors='ignore') as f:
                result['content'] = f.read()
    
    return result
```

## Pattern Matching and Filtering

The `gitignorefile` library can be used for pattern matching, as it implements the `.gitignore` pattern matching rules:

```python
import gitignorefile

def create_matcher(include_patterns, exclude_patterns):
    # Create custom matcher from patterns
    
    def matcher(path):
        # First check excludes
        for pattern in exclude_patterns:
            if gitignorefile.fnmatch(path, pattern):
                return False
                
        # If includes are specified, at least one must match
        if include_patterns:
            for pattern in include_patterns:
                if gitignorefile.fnmatch(path, pattern):
                    return True
            return False
            
        # If no includes specified, include everything not excluded
        return True
        
    return matcher
```

## Output Formatting

### JSON Output

```python
import json

def format_as_json(directory_data, metadata):
    result = {
        "metadata": metadata,
        "root": directory_data
    }
    return json.dumps(result, indent=2)
```

### Markdown Output

```python
def format_as_markdown(directory_data, metadata):
    md_output = [
        f"# Directory Digest: {metadata['base_directory']}",
        "",
        f"*Generated by dirdigest v{metadata['tool_version']} on {metadata['created_at']}*",
        "",
        "## Directory Structure",
        "```
        format_directory_tree(directory_data),
        "```",
        "",
        "## Contents",
        ""
    ]
    
    # Add file contents
    file_contents = extract_file_contents(directory_data)
    for file_path, content in file_contents:
        md_output.extend([
            f"### {file_path}",
            "```
            content,
            "```",
            ""
        ])
    
    return "\n".join(md_output)
```

## Clipboard Integration

Use `pyperclip` for cross-platform clipboard interaction:

```python
import pyperclip

def copy_to_clipboard(content):
    try:
        pyperclip.copy(content)
        return True
    except Exception as e:
        # Handle clipboard errors
        return False
```

For a more robust clipboard management approach:

```python
class ClipboardManager:
    def __init__(self):
        self.history = []
        self.current_value = None

    def get_clipboard(self):
        value = pyperclip.paste()
        if value != self.current_value:
            self.history.append(value)
            self.current_value = value
        return value

    def set_clipboard(self, value):
        pyperclip.copy(value)
        self.current_value = value
        self.history.append(value)
        
    def clear_clipboard(self):
        pyperclip.copy('')
        self.current_value = ''
```

This gives you a history of clipboard operations and better error handling.

## Testing CLI Applications

Testing CLI applications requires special approaches. Here are the best practices:

### 1. Use Click's Built-in Testing Support

Click provides the `click.testing` module specifically for testing CLI applications:

```python
from click.testing import CliRunner
from dirdigest import cli

def test_help_output():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Directory digest tool' in result.output
```

This approach allows testing the command interface without actual execution.

### 2. Use Pytest Fixtures for Common Test Setups

```python
import pytest
import tempfile
import os

@pytest.fixture
def temp_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test files and directories
        os.makedirs(os.path.join(tmpdir, "subdir"))
        with open(os.path.join(tmpdir, "file1.txt"), "w") as f:
            f.write("Test content")
        # Return the temp directory path
        yield tmpdir
        
def test_directory_processing(temp_directory):
    runner = CliRunner()
    result = runner.invoke(cli, ['process', temp_directory])
    assert result.exit_code == 0
    assert "file1.txt" in result.output
```

### 3. Mock External Dependencies

Use `unittest.mock` to mock filesystem operations, clipboard interactions, etc.:

```python
from unittest.mock import patch

def test_clipboard_copy():
    with patch('dirdigest.utils.clipboard.pyperclip.copy') as mock_copy:
        runner = CliRunner()
        result = runner.invoke(cli, ['process', '.', '--clipboard'])
        assert result.exit_code == 0
        # Verify that copy was called
        mock_copy.assert_called_once()
```

### 4. Test for Different Input Scenarios

```python
@pytest.mark.parametrize("format_option", ["json", "markdown"])
def test_output_formats(format_option, temp_directory):
    runner = CliRunner()
    result = runner.invoke(cli, ['process', temp_directory, '--format', format_option])
    assert result.exit_code == 0
    # Verify correct format was generated
```

### 5. Functional Testing Approach

For testing the entire CLI application:

```python
import subprocess

def test_cli_executable():
    result = subprocess.run(
        ["python", "-m", "dirdigest", "--help"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Directory digest tool" in result.stdout
```

## Project Structure

A well-organized project structure for `dirdigest`:

```
dirdigest/
├── __init__.py
├── cli.py           # Command line interface using Click
├── core.py          # Core directory traversal and processing logic
├── formatters/      # Output formatters
│   ├── __init__.py
│   ├── json.py
│   └── markdown.py
├── utils/
│   ├── __init__.py
│   ├── clipboard.py # Clipboard handling
│   ├── config.py    # Configuration handling
│   └── patterns.py  # Pattern matching utilities
├── constants.py     # Default patterns and constants
└── tests/           # Test suite
    ├── __init__.py
    ├── test_cli.py
    ├── test_core.py
    ├── test_formatters.py
    └── fixtures/    # Test fixture files
```

This structure separates concerns and makes the codebase modular and testable.

## Implementation Recommendations

1. **Use dependency injection** for components like formatters, filesystem operations, and clipboard access to make testing easier.

2. **Create a class-based architecture** for the core components:
   ```python
   class DirectoryProcessor:
       def __init__(self, config, matcher, formatter):
           self.config = config
           self.matcher = matcher
           self.formatter = formatter
           
       def process(self, directory):
           # Directory traversal and processing logic
           
       def generate_output(self, data):
           # Use the formatter to generate output
           return self.formatter.format(data)
   ```

3. **Implement a plugin system** for formatters to allow for future expansion:
   ```python
   class FormatRegistry:
       _formatters = {}
       
       @classmethod
       def register(cls, name):
           def decorator(formatter_class):
               cls._formatters[name] = formatter_class
               return formatter_class
           return decorator
           
       @classmethod
       def get_formatter(cls, name):
           return cls._formatters.get(name)
   
   @FormatRegistry.register('json')
   class JsonFormatter:
       def format(self, data):
           # JSON formatting logic
   ```

4. **Use proper error handling and reporting** throughout the application:
   ```python
   class DirectoryProcessingError(Exception):
       """Base exception for directory processing errors."""
       pass
       
   class FileReadError(DirectoryProcessingError):
       """Exception raised when a file cannot be read."""
       pass
   ```

5. **Implement comprehensive logging** with different verbosity levels:
   ```python
   import logging
   from rich.logging import RichHandler
   
   def setup_logging(verbosity):
       level = {
           0: logging.WARNING,
           1: logging.INFO,
           2: logging.DEBUG
       }.get(verbosity, logging.DEBUG)
       
       logging.basicConfig(
           level=level,
           format="%(message)s",
           handlers=[RichHandler(rich_tracebacks=True)]
       )
   ```

By following these best practices and recommendations, you'll create a robust, maintainable `dirdigest` tool that meets all the specified requirements while being easy to extend and test.