## Updated Requirements for `dirdigest`

**The following enhancements are added to the previous requirements:**

### Inclusion/Exclusion Pattern Flexibility

- Users can specify multiple `--include` or `--exclude` patterns either:
  - As a comma-separated list in a single flag, e.g.:
    ```
    dirdigest . --exclude '*.log,*.tmp' --include '*.py'
    ```
  - By repeating the flag multiple times, e.g.:
    ```
    dirdigest . --exclude '*.log' --exclude '*.tmp'
    ```
- The tool must correctly parse and combine patterns from both methods, supporting both approaches simultaneously.

### User-Friendly CLI and Help

- The CLI must provide concise, informative, and well-formatted help text.
- Help text should include:
  - Clear descriptions for all arguments and options
  - Usage examples, including both comma-separated and repeated flag syntax for pattern arguments
  - Explanation of default behaviors and how to override them
- The CLI should guide users to common usage patterns and troubleshooting tips.
- Use `rich` to format help output for readability (e.g., bold headings, color highlights).

### Logging of Included and Excluded Files

- All included files must be logged in green for clear visibility.
- All excluded files and folders must be logged in red.
- For every excluded file or folder, display the specific reason for exclusion, such as:
  - "Matches default ignore pattern"
  - "Matches user-specified exclude pattern '*.log'"
  - "Exceeds max size (512 KB > 300 KB)"
  - "Is a hidden file"
  - "Is a symlink (symlink following disabled)"
- The log should summarize total included and excluded counts, using color for emphasis.

### Example Logging Output

```plaintext
[green]Included:[/green] src/main.py
[red]Excluded:[/red] logs/app.log (Matches user-specified exclude pattern '*.log')
[red]Excluded:[/red] .env (Matches default ignore pattern)
[red]Excluded:[/red] data/large.csv (Exceeds max size: 1024 KB > 300 KB)
[green]Included:[/green] README.md
...
[bold green]Total included:[/bold green] 15
[bold red]Total excluded:[/bold red] 42
```
