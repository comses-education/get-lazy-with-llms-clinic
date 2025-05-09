# Cursor with Claude 3.7 Sonnet

## Improved Requirements for Promptbuilder CLI Tool

### Core Functionality
- Create a META_PROMPT generator that outputs a TASK_PERFORMING_PROMPT template
- Process various input types (direct strings, file contents, directory contents)
- Generate well-structured prompts following best practices from the provided context

### Command Line Interface
- Support all current arguments with consistent formatting:
  - `--task`: Task description (required)
  - `--context`: Files/directories to incorporate (supports glob patterns)
  - `--instructions`: Custom instructions (string or file path)
  - `--input`, `--output`: Input/output specifications
  - `--input_instructions`, `--output_instructions`: Format guidelines
  - `--save_on_disk`: Output file path
- Add new arguments:
  - `--format`: Output format (text, markdown, json)
  - `--version`: Show version information
  - `--verbose`: Enable detailed logging
  - `--config`: Specify custom config file location

### Architecture Requirements
- Implement modular design with clear separation of concerns:
  - CLI argument parsing
  - Configuration management
  - File/directory handling
  - Prompt generation
  - Output handling
- Use dependency injection for better testability
- Implement interface-based design for components
- Follow SOLID principles

### Testing Requirements
- Achieve minimum 80% test coverage
- Implement unit tests for all modules
- Add integration tests for command line functionality
- Create mock objects for file system operations
- Use fixtures for test data
- Implement property-based testing for input variations
- Support test parameterization for various scenarios

### Error Handling
- Provide clear error messages with suggested solutions
- Validate all inputs with specific error codes
- Implement graceful failure modes
- Add retry mechanisms for clipboard operations
- Log errors with appropriate detail levels

### Configuration Management
- Support hierarchical configuration:
  - Default built-in configuration
  - Global user configuration (~/.promptbuilder)
  - Project-specific configuration (./.promptbuilder)
  - Command-line arguments (highest priority)
- Allow configuration in YAML, JSON, or TOML formats
- Support environment variables for CI/CD integration

### Documentation
- Generate comprehensive API documentation
- Include usage examples and recipes
- Document configuration options
- Add developer documentation for extending functionality

### Extensibility
- Support plugin architecture for custom prompt templates
- Allow custom processors for different file types
- Enable hooks for pre/post-processing operations

### Performance Requirements
- Process large context directories efficiently
- Implement lazy loading for file contents
- Add caching mechanism for repeated operations
- Optimize for memory usage with large files

### Security
- Sanitize all file inputs
- Implement path traversal protection
- Validate file permissions before operations
- Support secrets management for sensitive content

### Code Quality
- Follow PEP 8 and PEP 257 standards
- Use type annotations throughout
- Implement static type checking
- Add linting to CI pipeline

### Deployment
- Package as PyPI module for easy installation
- Support containerized deployment
- Provide platform-specific binaries
- Support Python 3.8+ versions