
# Perplexity Generated Requirements

## Enhanced Requirements for PromptBuilder CLI Tool

This document outlines comprehensive requirements for the PromptBuilder CLI tool, addressing usability, reliability, and maintainability aspects to create a robust and user-friendly experience.

### Core Functionality

The PromptBuilder tool assists users in creating META_PROMPTs that generate task-specific prompts (TASK_PERFORMING_PROMPTs) when fed to an LLM. These requirements build upon the initial specification to create a more complete solution.

### Command-Line Interface Requirements

#### Basic Command Structure
```
promptbuilder [command] [options]
```

#### Primary Commands
- `create`: Create a new META_PROMPT (default if no command specified)
- `templates`: List/use available META_PROMPT templates
- `validate`: Check a META_PROMPT for completeness and proper formatting
- `history`: Show recently generated META_PROMPTs

#### Core Options
- `--task`: Short task description (required)
- `--context`: List of local files or entire folders to parse recursively
- `--instructions`: String or local instructions file
- `--input`: String or local file describing the input to the PERFORMING_PROMPT
- `--output`: String or local file describing the output to the PERFORMING_PROMPT
- `--input_instructions`: String or local file with input instructions
- `--output_instructions`: String or local file with output instructions
- `--save`: Path where the META_PROMPT should be stored
- `--format`: Output format (plain, markdown, json) (default: plain)
- `--no-clipboard`: Disable automatic clipboard copy
- `--config`: Specify a custom config file (default: .promptbuilder)
- `--profile`: Use a specific configuration profile
- `--template`: Use a specific META_PROMPT template
- `--verbose`: Enable detailed output for debugging

### Functional Requirements

#### Core Functionality
- Generate META_PROMPTs based on provided parameters
- Output META_PROMPT to stdout or to disk if --save is specified
- Automatically copy prompt to clipboard after execution (with option to disable)
- Clearly mark input/output or input_instructions/output_instructions as placeholders in the META_PROMPT
- Support recursive folder parsing for context with appropriate file filtering

#### Configuration Management
- Use a hierarchical configuration system (.promptbuilder file)
- Support user, project, and command-specific configurations
- Allow multiple named profiles for different use cases
- Store reasonable defaults for all parameters
- Support environment variable overrides for all options

#### Template System
- Include built-in templates for common META_PROMPT patterns
- Allow users to create and save custom templates
- Support template variables and conditional sections
- Provide template inheritance for building complex prompts

#### Interactive Mode
- Offer an interactive prompt-building wizard (`promptbuilder interactive`)
- Guide users through each component with helpful examples
- Provide real-time feedback and suggestions
- Allow users to preview and refine the META_PROMPT before finalizing

#### Input Processing
- Support multiple input formats (text, markdown, JSON)
- Intelligently handle large context files by summarizing or chunking
- Process and sanitize inputs to prevent common LLM issues
- Validate files exist before attempting to process them

#### Output Handling
- Provide formatted output options (plain text, markdown, JSON)
- Create a summary view of the META_PROMPT components
- Generate preview of how placeholder substitution might look
- Support output to multiple destinations (stdout, file, clipboard)

### Non-Functional Requirements

#### Usability
- Provide comprehensive help with examples for each command and option
- Include progress indicators for lengthy operations
- Offer clear error messages with suggested solutions
- Support tab completion for commands and options
- Maintain consistent option naming across commands

#### Reliability
- Implement proper error handling for all operations
- Validate all user inputs before processing
- Include timeout handling for long-running operations
- Provide graceful degradation when optional features are unavailable
- Support operation history with ability to revert to previous prompts

#### Maintainability
- Use a modular, extensible architecture
- Implement comprehensive logging with configurable levels
- Follow consistent coding standards and documentation practices
- Include unit and integration tests for all components
- Provide plugin system for extending functionality

#### Performance
- Optimize for fast startup time
- Efficiently handle large context directories
- Use lazy loading for optional components
- Implement caching for frequently accessed resources

### Implementation Guidelines

#### File Structure
- Use a modular package structure separating concerns:
  - CLI interface
  - Configuration management
  - Template handling
  - Context processing
  - Output formatting
  - Clipboard operations

#### Error Handling
- Provide specific error codes for different failure modes
- Include verbose logging option for troubleshooting
- Exit with appropriate status codes for automation workflows

#### Documentation
- Generate clear man pages for Unix-like systems
- Include comprehensive --help text for all commands
- Provide usage examples for common scenarios
- Create a user guide with best practices

#### Testing
- Include a test suite with unit and integration tests
- Support a dry-run mode for validating configurations
- Implement META_PROMPT validation against best practices

### Conclusion

These enhanced requirements address the three key areas requested:

1. **Usability**: Improved through templates, interactive mode, better help, and configuration profiles
2. **Reliability**: Enhanced with input validation, error handling, and proper testing
3. **Maintainability**: Supported via modular architecture, documentation, and consistent practices

Following these requirements will result in a robust, user-friendly tool that efficiently helps users create effective META_PROMPTs for their specific tasks.

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/21296096/f32a6462-fb9d-4eec-b08c-64ce0fb87fa1/paste.txt
[2] https://simonwillison.net/2023/Sep/30/cli-tools-python/
[3] https://www.assemblyai.com/blog/the-definitive-guide-to-python-click/
[4] https://dev.to/usooldatascience/mastering-command-line-interfaces-cli-in-python-a-comprehensive-guide-10bc
[5] https://www.thoughtworks.com/en-us/insights/blog/engineering-effectiveness/elevate-developer-experiences-cli-design-guidelines
[6] https://stackoverflow.com/questions/11063458/python-script-to-copy-text-to-clipboard
[7] http://witkowskibartosz.com/blog/how-to-use-pyperclip.html
[8] https://dash.plotly.com/dash-core-components/clipboard
[9] https://pypi.org/project/click-config-file/
[10] https://signoz.io/guides/python-logging-best-practices/
[11] https://click.palletsprojects.com/en/stable/testing/
[12] https://realpython.com/get-all-files-in-directory-python/
[13] https://stackoverflow.com/questions/69411257/best-architecture-for-a-python-command-line-tool-with-multiple-subcommands
[14] https://discuss.python.org/t/copy-to-system-clipboard/16198
[15] https://pypi.org/project/pytest-click/
[16] https://packaging.python.org/en/latest/guides/creating-command-line-tools/
[17] https://www.reddit.com/r/vim/comments/9jz194/how_to_copy_the_output_from_a_python_script_to/
[18] https://www.reddit.com/r/Python/comments/a7atsr/how_to_write_perfect_python_commandline_interfaces/
[19] https://dev.to/audreyk/manage-your-clipboard-in-the-cli-with-python-5f0d
[20] https://www.reddit.com/r/commandline/comments/m62cjq/recommended_architecture_for_cli_applications/
[21] https://note.nkmk.me/en/python-pyperclip-usage/
[22] https://labs.appligent.com/appligent-labs/the-advantages-of-command-line-interfaces-over-sdks-and-dlls
[23] https://realpython.com/python-click/
[24] https://click.palletsprojects.com
[25] https://www.honeybadger.io/blog/building-command-line-applications-in-python-a-comprehensive-guide/
[26] https://www.infoq.com/news/2020/12/cli-guidelines-qa/
[27] https://github.com/qltysh/qlty
[28] https://softwareengineering.stackexchange.com/questions/307467/what-are-good-habits-for-designing-command-line-arguments
[29] https://www.mndwrk.com/blog/python-click-or-how-to-write-professional-cli-applications
[30] https://www.abiquo.com/blog/building-a-pluggable-command-line-tool-in-python/
[31] https://lucasfcosta.com/2022/06/01/ux-patterns-cli-tools.html
[32] https://www.reddit.com/r/codereview/comments/1jxd2ly/cli_tool_which_can_estimate_maintainability_of/
[33] https://www.reddit.com/r/learnpython/comments/1ei7z4j/how_do_you_optimise_a_click_cli_application_to/
[34] https://pyperclip.readthedocs.io/en/latest/
[35] https://cmd2.readthedocs.io/en/2.5.9/features/clipboard/
[36] https://python-forum.io/thread-24784.html
[37] https://www.youtube.com/watch?v=L6MeJKrgnl0
[38] https://www.reddit.com/r/learnpython/comments/1g0j4r1/need_a_more_reliable_method_for_programmatic/
[39] https://community.fly.io/t/how-to-implement-copying-to-the-clipboard-in-python/23817
[40] https://pybit.es/articles/pyperclip/
[41] https://dash.plotly.com/dash-ag-grid/clipboard
[42] https://stackoverflow.com/questions/51662213/cant-get-pyperclip-to-use-copy-and-paste-modules-on-python3
[43] https://pypi.org/project/pyperclip/
[44] https://stackoverflow.com/questions/62680915/how-to-use-python-to-click-a-button-also-how-to-paste-clipboard-content-into-a
[45] https://pypi.org/project/pytest-click/
[46] https://news.ycombinator.com/item?id=22964910
[47] https://jwodder.github.io/kbits/posts/click-config/
[48] https://stackoverflow.com/questions/2212643/python-recursive-folder-read
[49] https://www.reddit.com/r/Python/comments/lkj52j/opinions_on_best_way_to_manage_logging_in_python/
[50] https://wangonya.com/blog/testing-click-with-pytest/
[51] https://docs.python.org/3/library/configparser.html
[52] https://pocoo-libs.narkive.com/ZbPbFEe6/click-using-default-values-from-configuration-files
[53] https://realpython.com/get-all-files-in-directory-python/
[54] https://stackoverflow.com/questions/22807972/python-best-practice-in-terms-of-logging
[55] https://click.palletsprojects.com/en/stable/testing/
[56] https://discuss.python.org/t/configuration-best-practices/26157
[57] https://github.com/pallets/click/blob/main/tests/test_testing.py
[58] https://github.com/erezsh/plyplus/issues/46
[59] https://til.simonwillison.net/pytest/test-click-app-with-streaming-input
[60] https://dev.to/bowmanjd/build-a-command-line-interface-with-python-poetry-and-click-1f5k
[61] https://tomassetti.me/parsing-in-python/
[62] https://www.youtube.com/watch?v=8xNUk1kqi2A
[63] https://www.reddit.com/r/Python/comments/q2al2v/i_made_a_recursive_descent_parser_with_a_clever/
[64] https://www.tech-artists.org/t/python-fastest-way-to-recursively-list-files-of-specific-type/3081
[65] https://blog.red-dove.com/posts/parsing-in-python/
[66] https://www.datacamp.com/tutorial/recursion-in-python
[67] https://www.youtube.com/watch?v=hrcQZ9NVO_U
[68] https://www.reddit.com/r/Python/comments/w1utza/how_are_you_all_handling_config_files/
[69] https://stackoverflow.com/questions/5055042/whats-the-best-practice-using-a-settingsconfig-file-in-python
[70] https://configu.com/blog/working-with-python-configuration-files-tutorial-best-practices/
[71] https://tech.preferred.jp/en/blog/working-with-configuration-in-python/
[72] https://www.lambdatest.com/blog/python-configuration-file/
[73] https://www.youtube.com/watch?v=5oe823-U-6I
[74] https://gist.github.com/6412cdc19f9a44901b03841e0443fbf7
[75] https://jcharistech.wordpress.com/2019/09/24/unit-testing-cli-applications-built-with-python-click/
[76] https://stackoverflow.com/questions/69977461/proper-way-to-test-clickexception-was-raised-with-pytest

---
Answer from Perplexity: pplx.ai/share

