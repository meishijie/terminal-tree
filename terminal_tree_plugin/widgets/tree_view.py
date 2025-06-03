"""Tree view widget for filesystem navigation."""

from pathlib import Path
from typing import Dict, List, Optional, Set

from rich.text import Text
from textual import events
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Tree

from ..utils.file_utils import get_file_info
from ..utils.path_utils import is_hidden


class TreeView(Widget):
    """A tree view widget for filesystem navigation."""
    
    DEFAULT_CSS = """
    TreeView {
        width: 1fr;
        height: 1fr;
        border: solid $primary;
        background: $surface;
    }
    
    TreeView Tree {
        background: $surface;
        color: $text;
    }
    
    TreeView Tree:focus {
        border: solid $accent;
    }
    """
    
    # Messages
    class DirectoryChanged(Message):
        """Posted when the current directory changes."""
        
        def __init__(self, path: Path) -> None:
            self.path = path
            super().__init__()
    
    class FileSelected(Message):
        """Posted when a file is selected."""
        
        def __init__(self, path: Path) -> None:
            self.path = path
            super().__init__()
    
    # Reactive attributes
    current_path: reactive[Path] = reactive(Path.cwd())
    show_hidden: reactive[bool] = reactive(False)
    
    def __init__(
        self,
        start_path: Optional[Path] = None,
        show_hidden: bool = False,
        **kwargs,
    ) -> None:
        self._expanded_dirs: Set[Path] = set()
        self._tree: Optional[Tree] = None
        super().__init__(**kwargs)
        self.show_hidden = show_hidden
        self.current_path = start_path or Path.cwd()
    
    def compose(self):
        """Compose the tree widget."""
        self._tree = Tree(str(self.current_path), id="file_tree")
        self._tree.show_root = True
        self._tree.show_guides = True
        yield self._tree
    
    def on_mount(self) -> None:
        """Initialize the tree when mounted."""
        if self._tree:
            self._populate_tree()
            self._tree.focus()
    
    def watch_current_path(self, new_path: Path) -> None:
        """React to current path changes."""
        if self._tree:
            self._populate_tree()
            self.post_message(self.DirectoryChanged(new_path))
    
    def watch_show_hidden(self, show_hidden: bool) -> None:
        """React to show_hidden changes."""
        if self._tree:
            self._populate_tree()
    
    def _populate_tree(self) -> None:
        """Populate the tree with filesystem data."""
        if not self._tree:
            return
        
        try:
            # Clear existing tree
            self._tree.clear()
            
            # Set root label
            root_label = self._get_path_label(self.current_path)
            self._tree.root.set_label(root_label)
            self._tree.root.data = self.current_path
            
            # Add children to root
            self._add_children(self._tree.root, self.current_path)
            
            # Expand root to show contents
            self._tree.root.expand()
            
        except Exception as e:
            # If there's an error, at least show the root
            self._tree.root.set_label(f"❌ Error: {e}")
            self._tree.root.data = self.current_path
    
    def _get_path_label(self, path: Path) -> Text:
        """Get a formatted label for a path."""
        text = Text()
        
        if path.is_dir():
            # Directory icon and name
            text.append("📁 ", style="bold blue")
            # Handle root directory case
            display_name = path.name if path.name else str(path)
            text.append(display_name, style="bold blue")
        else:
            # File icon and name
            if path.suffix.lower() in {".py", ".js", ".html", ".css", ".json"}:
                text.append("📄 ", style="green")
            elif path.suffix.lower() in {".txt", ".md", ".rst"}:
                text.append("📝 ", style="yellow")
            elif path.suffix.lower() in {".jpg", ".png", ".gif", ".svg"}:
                text.append("🖼️ ", style="magenta")
            else:
                text.append("📄 ", style="white")
            
            text.append(path.name, style="white")
            
            # Add file size (simplified to avoid errors)
            try:
                size = path.stat().st_size
                if size < 1024:
                    size_str = f"{size}B"
                elif size < 1024 * 1024:
                    size_str = f"{size // 1024}KB"
                else:
                    size_str = f"{size // (1024 * 1024)}MB"
                text.append(f" ({size_str})", style="dim")
            except Exception:
                pass
        
        return text
    
    def _add_children(self, node, path: Path) -> None:
        """Add child nodes to a tree node."""
        if not path.is_dir():
            return
        
        try:
            # Get directory contents
            items = list(path.iterdir())
            
            # Filter hidden files if needed
            if not self.show_hidden:
                items = [item for item in items if not is_hidden(item)]
            
            # Limit items to prevent overwhelming the display
            items = items[:50]  # Show max 50 items
            
            # Sort: directories first, then files, both alphabetically
            items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
            
            # Add items to tree
            for item in items:
                try:
                    label = self._get_path_label(item)
                    child_node = node.add(label, data=item)
                    
                    # If it's a directory, add a placeholder to make it expandable
                    if item.is_dir():
                        try:
                            # Quick check if directory has contents (avoid full iteration)
                            has_contents = any(x for x, _ in zip(item.iterdir(), range(1)))
                            if has_contents:
                                child_node.add("📂 Loading...", data=None)
                        except (PermissionError, OSError):
                            child_node.add("🔒 Protected", data=None)
                except Exception:
                    # Skip problematic items
                    continue
        
        except (PermissionError, OSError):
            # Add error node
            node.add("❌ Permission denied", data=None)
        except Exception as e:
            # Add generic error node
            node.add(f"❌ Error: {str(e)[:50]}", data=None)
    
    def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        """Handle tree node expansion."""
        node = event.node
        path = node.data
        
        if path and path.is_dir():
            # Check if this node has placeholder children (empty nodes)
            has_placeholder = False
            for child in node.children:
                if child.data is None and ("Loading..." in str(child.label) or "Protected" in str(child.label)):
                    has_placeholder = True
                    break
            
            # Only remove children if they are placeholders
            if has_placeholder:
                # Remove placeholder children safely
                try:
                    node.remove_children()
                except (KeyError, ValueError):
                    # If removal fails, clear the children list manually
                    node._children.clear()
                
                # Add actual children
                self._add_children(node, path)
            
            # Remember expanded state
            self._expanded_dirs.add(path)
    
    def on_tree_node_collapsed(self, event: Tree.NodeCollapsed) -> None:
        """Handle tree node collapse."""
        node = event.node
        path = node.data
        
        if path:
            # Remove from expanded set
            self._expanded_dirs.discard(path)
    
    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """Handle tree node selection."""
        node = event.node
        path = node.data
        
        if path:
            if path.is_dir():
                # Change current directory
                self.current_path = path
            else:
                # Select file for preview
                self.post_message(self.FileSelected(path))
    
    def navigate_to(self, path: Path) -> None:
        """Navigate to a specific path."""
        if path.is_dir():
            self.current_path = path
        else:
            # Navigate to parent directory and select file
            self.current_path = path.parent
            # TODO: Select the file in the tree
    
    def go_up(self) -> None:
        """Navigate to parent directory."""
        parent = self.current_path.parent
        if parent != self.current_path:  # Not at root
            self.current_path = parent
    
    def refresh_tree(self) -> None:
        """Refresh the tree view."""
        self._populate_tree()
    
    def toggle_hidden(self) -> None:
        """Toggle showing hidden files."""
        self.show_hidden = not self.show_hidden
    
    def on_key(self, event: events.Key) -> None:
        """Handle key events."""
        # Only handle keys that are specific to TreeView
        # Let application handle backspace, f5, ctrl+h via BINDINGS
        if event.key == "enter":
            # Handle enter key to navigate into directories
            if self._tree and self._tree.cursor_node:
                node = self._tree.cursor_node
                path = node.data
                if path and path.is_dir():
                    self.current_path = path
                    event.prevent_default()
        # Let the Tree widget handle arrow keys for navigation within the tree 