"""Path handling utilities."""

import os
from pathlib import Path
from typing import List, Optional, Tuple


def normalize_path(path_str: str) -> Path:
    """Normalize a path string to a Path object."""
    # Expand user home directory
    path_str = os.path.expanduser(path_str)
    
    # Convert to Path and resolve
    path = Path(path_str)
    
    try:
        # Try to resolve the path (follow symlinks, make absolute)
        return path.resolve()
    except (OSError, ValueError):
        # If resolution fails, return the path as-is
        return path.absolute()


def validate_path(path: Path) -> Tuple[bool, str]:
    """Validate a path and return (is_valid, error_message)."""
    try:
        if not path.exists():
            return False, f"Path does not exist: {path}"
        
        if not path.is_dir():
            return False, f"Path is not a directory: {path}"
        
        # Check if we can read the directory
        try:
            list(path.iterdir())
        except PermissionError:
            return False, f"Permission denied: {path}"
        except OSError as e:
            return False, f"Cannot access directory: {e}"
        
        return True, ""
    
    except (OSError, ValueError) as e:
        return False, f"Invalid path: {e}"


def get_path_components(path: Path) -> List[Tuple[str, Path]]:
    """Get path components as (name, path) tuples for breadcrumb navigation."""
    components = []
    current = path.resolve()
    
    # Add the current directory
    components.append((current.name or str(current), current))
    
    # Add parent directories
    for parent in current.parents:
        name = parent.name or str(parent)
        components.append((name, parent))
    
    # Reverse to get root -> current order
    components.reverse()
    
    return components


def get_parent_directory(path: Path) -> Optional[Path]:
    """Get the parent directory of a path, or None if at root."""
    try:
        parent = path.parent
        if parent == path:  # We're at the root
            return None
        return parent
    except (OSError, ValueError):
        return None


def find_common_prefix(paths: List[Path]) -> Optional[Path]:
    """Find the common prefix path among a list of paths."""
    if not paths:
        return None
    
    if len(paths) == 1:
        return paths[0].parent if paths[0].is_file() else paths[0]
    
    # Convert all paths to their parts
    path_parts = [list(path.resolve().parts) for path in paths]
    
    # Find the common prefix
    common_parts = []
    min_length = min(len(parts) for parts in path_parts)
    
    for i in range(min_length):
        part = path_parts[0][i]
        if all(parts[i] == part for parts in path_parts):
            common_parts.append(part)
        else:
            break
    
    if common_parts:
        return Path(*common_parts)
    
    return None


def is_hidden(path: Path) -> bool:
    """Check if a file or directory is hidden."""
    # On Unix-like systems, files starting with '.' are hidden
    if path.name.startswith('.'):
        return True
    
    # On Windows, check the hidden attribute
    try:
        import stat
        if os.name == 'nt':  # Windows
            attrs = os.stat(path).st_file_attributes
            return bool(attrs & stat.FILE_ATTRIBUTE_HIDDEN)
    except (AttributeError, OSError):
        pass
    
    return False


def get_relative_path(path: Path, base: Path) -> str:
    """Get a relative path string from base to path."""
    try:
        return str(path.relative_to(base))
    except ValueError:
        # If path is not relative to base, return absolute path
        return str(path)


def autocomplete_path(partial_path: str, base_dir: Path) -> List[str]:
    """Get autocomplete suggestions for a partial path."""
    suggestions = []
    
    try:
        # Normalize the partial path
        if partial_path.startswith('/'):
            # Absolute path
            search_path = Path(partial_path)
        else:
            # Relative path
            search_path = base_dir / partial_path
        
        # If the path ends with a separator, list contents of that directory
        if partial_path.endswith(os.sep):
            if search_path.is_dir():
                try:
                    for item in sorted(search_path.iterdir()):
                        if item.is_dir():
                            suggestions.append(str(item) + os.sep)
                        else:
                            suggestions.append(str(item))
                except PermissionError:
                    pass
        else:
            # Find parent directory and filter by prefix
            parent = search_path.parent
            prefix = search_path.name
            
            if parent.is_dir():
                try:
                    for item in sorted(parent.iterdir()):
                        if item.name.startswith(prefix):
                            if item.is_dir():
                                suggestions.append(str(item) + os.sep)
                            else:
                                suggestions.append(str(item))
                except PermissionError:
                    pass
    
    except (OSError, ValueError):
        pass
    
    return suggestions[:20]  # Limit to 20 suggestions 