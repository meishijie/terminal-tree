"""File preview widget with syntax highlighting."""

from pathlib import Path
from typing import Optional

from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static

from ..utils.file_utils import get_file_info, get_syntax_for_file, is_text_file, read_file_content


class FilePreview(Widget):
    """A widget for previewing file contents with syntax highlighting."""
    
    DEFAULT_CSS = """
    FilePreview {
        width: 1fr;
        height: 1fr;
        border: solid $primary;
        background: $surface;
    }
    
    FilePreview Static {
        background: $surface;
        color: $text;
        padding: 1;
    }
    
    FilePreview:focus {
        border: solid $accent;
    }
    """
    
    # Reactive attributes
    current_file: reactive[Optional[Path]] = reactive(None)
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._content_widget: Optional[Static] = None
    
    def compose(self):
        """Compose the preview widget."""
        self._content_widget = Static(
            self._get_welcome_content(),
            id="preview_content"
        )
        yield self._content_widget
    
    def watch_current_file(self, new_file: Optional[Path]) -> None:
        """React to current file changes."""
        if self._content_widget:
            if new_file:
                content = self._get_file_content(new_file)
            else:
                content = self._get_welcome_content()
            
            self._content_widget.update(content)
    
    def _get_welcome_content(self) -> RenderableType:
        """Get welcome content when no file is selected."""
        welcome_text = Text()
        welcome_text.append("📁 Terminal Tree Plugin\n\n", style="bold blue")
        welcome_text.append("Select a file from the tree to preview its contents.\n\n", style="dim")
        welcome_text.append("Supported features:\n", style="bold")
        welcome_text.append("• Syntax highlighting for code files\n", style="green")
        welcome_text.append("• File information display\n", style="green")
        welcome_text.append("• Text file content preview\n", style="green")
        welcome_text.append("• Binary file detection\n", style="green")
        welcome_text.append("\nKeyboard shortcuts:\n", style="bold")
        welcome_text.append("• ↑/↓ - Navigate within tree\n", style="yellow")
        welcome_text.append("• ←/→ - Expand/collapse directories\n", style="yellow")
        welcome_text.append("• Enter - Open directory/file\n", style="yellow")
        welcome_text.append("• Backspace - Go to parent directory\n", style="yellow")
        welcome_text.append("• g - Edit path\n", style="yellow")
        welcome_text.append("• F5 - Refresh\n", style="yellow")
        welcome_text.append("• Ctrl+H - Toggle hidden files\n", style="yellow")
        welcome_text.append("• Tab - Switch panels\n", style="yellow")
        welcome_text.append("• q - Quit\n", style="yellow")
        
        return Panel(
            welcome_text,
            title="Welcome",
            border_style="blue",
            padding=(1, 2),
        )
    
    def _get_file_content(self, file_path: Path) -> RenderableType:
        """Get content for a specific file."""
        if not file_path.exists():
            return Panel(
                Text("❌ File not found", style="red"),
                title=f"Error: {file_path.name}",
                border_style="red",
            )
        
        # Get file information
        file_info = get_file_info(file_path)
        
        # Create header with file info
        header = Text()
        header.append(f"📄 {file_path.name}\n", style="bold white")
        header.append(f"Path: {file_path}\n", style="dim")
        header.append(f"Size: {file_info['size']}\n", style="dim")
        header.append(f"Modified: {file_info['modified']}\n", style="dim")
        header.append(f"Permissions: {file_info['permissions']}\n", style="dim")
        header.append("\n")
        
        # Check if it's a text file
        if not is_text_file(file_path):
            # Binary file
            content = Text()
            content.append(header)
            content.append("🔒 Binary file - preview not available\n", style="yellow")
            
            # Try to show file type info
            import mimetypes
            mime_type, _ = mimetypes.guess_type(str(file_path))
            if mime_type:
                content.append(f"MIME type: {mime_type}\n", style="dim")
            
            return Panel(
                content,
                title=f"Binary File: {file_path.name}",
                border_style="yellow",
                padding=(1, 2),
            )
        
        # Read text file content
        file_content = read_file_content(file_path)
        
        if file_content is None:
            return Panel(
                Text("❌ Unable to read file content", style="red"),
                title=f"Error: {file_path.name}",
                border_style="red",
            )
        
        # Get syntax highlighting
        syntax = get_syntax_for_file(file_path, file_content)
        
        if syntax:
            # Use syntax highlighting
            content_panel = Panel(
                syntax,
                title=f"📄 {file_path.name}",
                border_style="green",
                padding=(0, 1),
            )
        else:
            # Plain text fallback
            content = Text()
            content.append(header)
            content.append(file_content)
            
            content_panel = Panel(
                content,
                title=f"📄 {file_path.name}",
                border_style="blue",
                padding=(1, 2),
            )
        
        return content_panel
    
    def set_file(self, file_path: Optional[Path]) -> None:
        """Set the current file to preview."""
        self.current_file = file_path
    
    def clear(self) -> None:
        """Clear the preview and show welcome content."""
        self.current_file = None
    
    def refresh_preview(self) -> None:
        """Refresh the current file preview."""
        if self.current_file:
            # Force refresh by setting to None then back
            current = self.current_file
            self.current_file = None
            self.current_file = current 