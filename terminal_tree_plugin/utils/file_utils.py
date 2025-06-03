"""File operation utilities."""

import mimetypes
import os
import stat
from pathlib import Path
from typing import Dict, Optional, Tuple

from rich.syntax import Syntax


def get_file_info(path: Path) -> Dict[str, str]:
    """Get file information including size, permissions, and modification time."""
    try:
        stat_info = path.stat()
        
        # File size
        size = stat_info.st_size
        if size < 1024:
            size_str = f"{size} B"
        elif size < 1024 * 1024:
            size_str = f"{size / 1024:.1f} KB"
        elif size < 1024 * 1024 * 1024:
            size_str = f"{size / (1024 * 1024):.1f} MB"
        else:
            size_str = f"{size / (1024 * 1024 * 1024):.1f} GB"
        
        # Permissions
        mode = stat_info.st_mode
        permissions = stat.filemode(mode)
        
        # Modification time
        import datetime
        mtime = datetime.datetime.fromtimestamp(stat_info.st_mtime)
        mtime_str = mtime.strftime("%Y-%m-%d %H:%M:%S")
        
        return {
            "size": size_str,
            "permissions": permissions,
            "modified": mtime_str,
            "type": "directory" if path.is_dir() else "file",
        }
    except (OSError, ValueError):
        return {
            "size": "Unknown",
            "permissions": "Unknown",
            "modified": "Unknown",
            "type": "unknown",
        }


def is_text_file(path: Path, max_size: int = 1024 * 1024) -> bool:
    """Check if a file is likely to be a text file."""
    if not path.is_file():
        return False
    
    # Check file size (skip very large files)
    try:
        if path.stat().st_size > max_size:
            return False
    except OSError:
        return False
    
    # Check MIME type
    mime_type, _ = mimetypes.guess_type(str(path))
    if mime_type and mime_type.startswith("text/"):
        return True
    
    # Check common text file extensions
    text_extensions = {
        ".txt", ".md", ".py", ".js", ".html", ".css", ".json", ".xml",
        ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".log",
        ".sh", ".bash", ".zsh", ".fish", ".ps1", ".bat", ".cmd",
        ".c", ".cpp", ".h", ".hpp", ".java", ".go", ".rs", ".php",
        ".rb", ".pl", ".lua", ".r", ".sql", ".csv", ".tsv",
        ".dockerfile", ".gitignore", ".gitattributes", ".editorconfig",
    }
    
    if path.suffix.lower() in text_extensions:
        return True
    
    # Check if file has no extension but common text file names
    text_names = {
        "readme", "license", "changelog", "makefile", "dockerfile",
        "requirements", "pipfile", "poetry", "setup", "manifest",
    }
    
    if path.name.lower() in text_names:
        return True
    
    # Try to read a small portion and check for binary content
    try:
        with open(path, "rb") as f:
            chunk = f.read(1024)
            if b"\x00" in chunk:  # Null bytes indicate binary
                return False
            # Check if most characters are printable
            try:
                chunk.decode("utf-8")
                return True
            except UnicodeDecodeError:
                return False
    except (OSError, PermissionError):
        return False


def read_file_content(path: Path, max_lines: int = 1000) -> Optional[str]:
    """Read file content with encoding detection and line limit."""
    if not is_text_file(path):
        return None
    
    encodings = ["utf-8", "utf-16", "latin-1", "cp1252"]
    
    for encoding in encodings:
        try:
            with open(path, "r", encoding=encoding) as f:
                lines = []
                for i, line in enumerate(f):
                    if i >= max_lines:
                        lines.append(f"\n... (truncated after {max_lines} lines)")
                        break
                    lines.append(line.rstrip("\n\r"))
                return "\n".join(lines)
        except (UnicodeDecodeError, OSError):
            continue
    
    return None


def get_syntax_for_file(path: Path, content: str) -> Optional[Syntax]:
    """Get Rich Syntax object for file content with appropriate highlighting."""
    if not content:
        return None
    
    # Map file extensions to lexer names
    extension_map = {
        ".py": "python",
        ".js": "javascript", 
        ".ts": "typescript",
        ".html": "html",
        ".css": "css",
        ".json": "json",
        ".xml": "xml",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".toml": "toml",
        ".ini": "ini",
        ".cfg": "ini",
        ".conf": "ini",
        ".sh": "bash",
        ".bash": "bash",
        ".zsh": "bash",
        ".fish": "fish",
        ".ps1": "powershell",
        ".bat": "batch",
        ".cmd": "batch",
        ".c": "c",
        ".cpp": "cpp",
        ".h": "c",
        ".hpp": "cpp",
        ".java": "java",
        ".go": "go",
        ".rs": "rust",
        ".php": "php",
        ".rb": "ruby",
        ".pl": "perl",
        ".lua": "lua",
        ".r": "r",
        ".sql": "sql",
        ".md": "markdown",
        ".dockerfile": "dockerfile",
    }
    
    # Get lexer from extension
    lexer = extension_map.get(path.suffix.lower())
    
    # Special cases for files without extensions
    if not lexer:
        name_lower = path.name.lower()
        if name_lower in ["dockerfile", "makefile"]:
            lexer = name_lower
        elif name_lower in ["readme", "changelog"]:
            lexer = "markdown"
    
    # Default to text if no specific lexer found
    if not lexer:
        lexer = "text"
    
    try:
        return Syntax(
            content,
            lexer,
            theme="monokai",
            line_numbers=True,
            word_wrap=False,
            background_color="default",
        )
    except Exception:
        # Fallback to plain text if syntax highlighting fails
        return Syntax(
            content,
            "text",
            theme="monokai",
            line_numbers=True,
            word_wrap=False,
            background_color="default",
        ) 