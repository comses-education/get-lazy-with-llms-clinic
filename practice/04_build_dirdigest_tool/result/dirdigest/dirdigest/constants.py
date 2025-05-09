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
    # --- Hidden files and directories ---
    ".*",  # General catch-all for hidden items like .git, .DS_Store, .vscode, etc.
            # This will catch top-level .env, .venv, etc.
    "**/.DS_Store",
    "**/Thumbs.db",
    "**/.classpath",
    "**/.project",
    "**/.settings/", # Common for Eclipse IDE
    "**/.idea/",    # Common for IntelliJ IDEs
    "**/.vscode/",  # Common for VS Code IDE

    # --- VCS specific (already covered by .*, but more explicit) ---
    "**/.git/",
    "**/.svn/",
    "**/.hg/",
    "**/.bzr/",

    # --- Common Build/Output/Artifact Directories (using globstar) ---
    "**/__pycache__/",
    "**/build/",
    "**/dist/",
    "**/target/",       # Common for Java (Maven/Gradle), Rust
    "**/out/",          # Common for some build systems, e.g., IntelliJ
    "**/bin/",          # Often contains compiled binaries or scripts not part of source
    "**/*.egg-info/",
    "**/.cache/",
    "**/.pytest_cache/",
    "**/.mypy_cache/",
    "**/.ruff_cache/",

    # --- Dependency/Package Management Directories (using globstar) ---
    "**/node_modules/",
    "**/bower_components/",
    "**/vendor/",       # Common in PHP (Composer), Go

    # --- Virtual Environment Directories (using globstar) ---
    # These ensure they are caught even if nested or named slightly differently
    "**/.venv/",
    "**/venv/",
    "**/ENV/",
    "**/env/",
    "**/.env/",         # Note: .env is often a file, but if it's a dir, this catches it.
                        # If specifically for .env *files*, see file patterns below.

    # --- Log files (using globstar) ---
    "**/*.log",
    "**/*.logs", # If a directory named e.g. app.logs

    # --- Temporary & Backup Files (using globstar) ---
    "**/*.tmp",
    "**/*.temp",
    "**/*.bak",
    "**/*.swp",
    "**/*~",            # Common for editor backup files (like Vim's value for 'backupcopy')

    # --- Compiled Code & Intermediates (specific extensions, often with globstar) ---
    "**/*.pyc",
    "**/*.pyo",
    "**/*.pyd",
    "**/*.class",       # Java
    "**/*.jar",
    "**/*.war",
    "**/*.ear",
    "**/*.o",           # C/C++ object files
    "**/*.obj",
    "**/*.so",          # Shared objects (Linux)
    "**/*.dylib",       # Dynamic libraries (macOS)
    "**/*.dll",         # Dynamic Link Libraries (Windows)
    "**/*.lib",
    "**/*.a",           # Static libraries
    "**/*.exe",         # Executables (Windows)
    "**/*.com",
    "**/*.bat",
    "**/*.sh",          # Shell scripts might be executables not source, user can include if needed

    # --- Common Binary, Media, and Large Data Files (extensions) ---
    # These are less likely to need globstar unless they are organized in specific ways
    # For these, simple extension matching is usually sufficient.
    # If you have, e.g., all images in '**/assets/images/', you'd exclude '**/assets/images/' above.
    "*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.tiff", "*.webp",
    "*.mp4", "*.avi", "*.mov", "*.mkv", "*.wmv",
    "*.mp3", "*.wav", "*.flac", "*.aac", "*.ogg",
    "*.zip", "*.tar", "*.tar.gz", "*.tar.bz2", "*.rar", "*.7z", "*.gz", "*.bz2",
    "*.woff", "*.woff2", "*.ttf", "*.otf", "*.eot",
    "*.pdf",
    "*.doc", "*.docx", "*.ppt", "*.pptx", "*.xls", "*.xlsx",
    "*.odt", "*.ods", "*.odp",
    "*.iso", "*.img", "*.dmg", "*.app", "*.msi",
    "*.db", "*.sqlite", "*.sqlite3", "*.mdb", # Database files

    # --- Specific files like .env (using globstar to catch at any depth) ---
    "**/.env",          # For .env *files* at any depth
    "**/.env.*",        # For files like .env.local, .env.development
    "**/poetry.lock",
    "**/Pipfile.lock",
    "**/yarn.lock",
    "**/package-lock.json",
    "**/composer.lock",
    "**/Gemfile.lock",
    "**/MANIFEST.MF", # Java manifest files often in target/ or build/

    # Add any other project-specific or generally unwanted patterns here
]