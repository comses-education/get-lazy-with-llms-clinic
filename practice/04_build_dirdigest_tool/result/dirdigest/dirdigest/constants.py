# dirdigest/dirdigest/constants.py
TOOL_NAME = "dirdigest"
TOOL_VERSION = "0.1.0"  # Corresponds to pyproject.toml version

# Using gitignore style patterns.
# Ensure patterns for directories end with a '/' if they are meant to only match directories.
# Otherwise, fnmatch might match 'node_modules.txt' with 'node_modules'.
# For simplicity here, we'll rely on os.path.isdir checks later for directory-specific patterns
# if not using a library that handles this distinction well (like gitignore_parser).
# For now, fnmatch will be used, and it doesn't distinguish files from dirs based on trailing slash.

DEFAULT_IGNORE_PATTERNS = [
    # Hidden files and directories
    ".*",  # Matches .git, .DS_Store, .env, etc.
    "**/.DS_Store",  # More specific for .DS_Store in any subdir
    "**/Thumbs.db",
    # Binary and media files (common examples)
    "*.jpg",
    "*.jpeg",
    "*.png",
    "*.gif",
    "*.bmp",
    "*.tiff",
    "*.webp",
    "*.mp4",
    "*.avi",
    "*.mov",
    "*.mkv",
    "*.wmv",
    "*.mp3",
    "*.wav",
    "*.flac",
    "*.aac",
    "*.ogg",
    "*.exe",
    "*.dll",
    "*.so",
    "*.dylib",
    "*.app",
    "*.msi",
    "*.com",
    "*.bat",
    "*.sh",
    "*.zip",
    "*.tar",
    "*.tar.gz",
    "*.tar.bz2",
    "*.rar",
    "*.7z",
    "*.gz",
    "*.bz2",
    "*.woff",
    "*.woff2",
    "*.ttf",
    "*.otf",
    "*.eot",
    "*.pdf",
    "*.doc",
    "*.docx",
    "*.ppt",
    "*.pptx",
    "*.xls",
    "*.xlsx",
    "*.odt",
    "*.ods",
    "*.odp",
    "*.iso",
    "*.img",
    "*.dmg",
    # Development artifacts
    "*.pyc",
    "*.pyo",
    "*.pyd",
    "*.class",
    "*.jar",
    "*.war",
    "*.ear",
    "*.o",
    "*.obj",
    "*.lib",
    "*.a",
    "*.o.*",  # *.o.* for object files from some compilers
    "__pycache__/",  # Matches the directory itself
    ".cache/",
    "dist/",
    "build/",
    "target/",  # Common for Java/Rust
    "out/",  # Common for some build systems
    "node_modules/",
    "bower_components/",
    ".venv/",
    "venv/",
    "ENV/",
    "env/",
    ".env/",  # Virtual environments
    ".git/",  # VCS directories
    ".svn/",
    ".hg/",
    "*.egg-info/",
    # Data and temporary files
    "*.db",
    "*.sqlite",
    "*.sqlite3",
    "*.mdb",
    "*.log",
    "*.tmp",
    "*.temp",
    "*.bak",
    "*.swp",
    "~*",  # ~* for Vim backup files
    "*.DS_Store",  # Already covered by .*, but explicit is fine
    "Thumbs.db",  # Already covered by .*, but explicit is fine
]
