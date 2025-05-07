# src/dirdigest/models.py (Corrected)

import dataclasses
from enum import Enum
from pathlib import Path
from typing import List, Optional, Union


class ItemType(Enum):
    """Type of filesystem item."""
    FOLDER = "folder"
    FILE = "file"


class FileStatus(Enum):
    """Status of a file regarding inclusion in the digest."""
    INCLUDED = "included"
    SKIPPED_SIZE = "skipped_size"
    SKIPPED_ENCODING = "skipped_encoding"
    SKIPPED_PERMISSION = "skipped_permission"
    SKIPPED_BINARY = "skipped_binary" # Explicit status for non-text files


@dataclasses.dataclass
class FileInfo:
    """Represents information about a file."""
    # --- Non-default arguments first ---
    relative_path: str
    absolute_path: Path
    # --- Default arguments follow ---
    type: ItemType = ItemType.FILE
    content: Optional[str] = None
    status: FileStatus = FileStatus.INCLUDED
    size_kb: float = 0.0


@dataclasses.dataclass
class DirectoryInfo:
    """Represents information about a directory."""
    # --- Non-default arguments first ---
    relative_path: str
    absolute_path: Path
    # --- Default arguments follow ---
    type: ItemType = ItemType.FOLDER
    children: List[Union["DirectoryInfo", FileInfo]] = dataclasses.field(default_factory=list)

    def sort_children(self):
        """Sorts children alphabetically by relative path."""
        self.children.sort(key=lambda item: item.relative_path)

# Define a type alias for convenience
FileSystemItem = Union[DirectoryInfo, FileInfo]