# Best Practices Prompt for Testing the `dirdigest` Tool

**I need to create a comprehensive test suite for the `dirdigest` command line tool. Here's the relevant information about the tool:**

- **Tool Purpose**: `dirdigest` recursively processes directories and files, creating a structured digest in markdown or JSON format suitable for LLM context ingestion.
- **Key Requirements**: 
  - Process directories recursively with configurable depth and file size limits
  - Filter files/directories using include/exclude patterns
  - Generate formatted output in markdown or JSON
  - Support clipboard integration
  - Handle configuration from file and CLI arguments
  - Provide detailed logging and error handling
- **Technical Architecture**: Python-based CLI tool using modules for core functionality, formatting, clipboard handling, pattern matching, and configuration management
- **Code Structure**: Modular architecture with separate components for CLI, core processing, formatting, and utilities

## Test Suite Requirements

**Generate a detailed test suite plan that includes:**

1. **Test Categories**: Break down tests into logical categories:
   - CLI argument parsing and validation tests
   - File traversal and filtering tests
   - Content processing and size limit tests
   - Output format (markdown/JSON) tests
   - Configuration file parsing tests
   - Clipboard integration tests
   - Logging and error handling tests

2. **Priority Levels**: Assign priorities to different test areas based on criticality:
   - High: Core functionality (file traversal, content processing)
   - Medium: Output formatting and configuration handling
   - Low: Convenience features (clipboard integration)

3. **Test Case Structure**: For each test area, provide:
   - Test objectives
   - Input requirements (directory structures, file contents, CLI arguments)
   - Expected outcomes (output format, included/excluded files)
   - Edge cases (large files, special characters, symlinks)
   - Potential failure scenarios (permission errors, encoding issues)

## Guidance for Reasoning

**As you develop this test plan:**
- First analyze the code structure to identify key components requiring thorough testing
- Consider both happy paths (normal usage) and edge cases (unusual file structures, invalid inputs)
- Identify integration points between components (e.g., how core processing feeds into formatters)
- Pay special attention to pattern matching logic and directory traversal edge cases
- Consider performance implications with large directory structures
- Address security concerns with file access and content processing
- Test configuration merging logic thoroughly (CLI args overriding config files)

## Output Specifications

**Structure your test suite plan as follows:**
1. Executive summary of testing strategy (2-3 paragraphs)
2. Categorized test scenarios with specific test cases
3. Test prioritization and rationale
4. Implementation recommendations including:
   - Mock directory structures to use for testing
   - Required test fixtures
   - Recommended test isolation techniques

## Success Criteria Definition

**The test suite should validate that:**
- Files are correctly traversed and filtered according to specified patterns
- Content size limits are properly enforced
- Output is correctly formatted in the chosen format (JSON or markdown)
- Configuration options from both CLI and files are correctly merged
- Errors are properly handled and logged
- Performance remains acceptable with large directory structures

## Example Format

**Include 2-3 example test cases in this format:**
```
Test ID: CLI-001
Description: Verify basic directory processing with default options
Preconditions: Test directory with mixed file types (text, binary, hidden)
Test Steps:
  1. Run `dirdigest` with no arguments on the test directory
  2. Examine stdout output
  3. Verify clipboard contents
Expected Result: Markdown-formatted directory digest with default ignores applied
Edge Cases: Test with empty directory, directory containing only ignored files
```