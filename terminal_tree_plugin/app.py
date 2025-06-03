"""Main application class for the terminal tree plugin."""

from pathlib import Path
from typing import Optional

from textual import events
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header

from .widgets import FilePreview, PathInput, TreeView


class TerminalTreeApp(App):
    """Main application for the terminal tree plugin."""
    
    # Use relative path from the package
    CSS_PATH = Path(__file__).parent / "styles" / "app.tcss"
    
    TITLE = "Terminal Tree Plugin"
    SUB_TITLE = "Filesystem Navigator"
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("f1", "show_help", "Help"),
        ("f5", "refresh", "Refresh"),
        ("ctrl+h", "toggle_hidden", "Toggle Hidden"),
        ("g", "edit_path", "Edit Path"),
        ("backspace", "go_up", "Parent Dir"),
        ("tab", "focus_next", "Next Panel"),
        ("shift+tab", "focus_previous", "Previous Panel"),
    ]
    
    def __init__(
        self,
        start_path: Optional[Path] = None,
        debug: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.start_path = start_path or Path.cwd()
        self._debug = debug
        
        # Widget references
        self.tree_view: Optional[TreeView] = None
        self.file_preview: Optional[FilePreview] = None
        self.path_input: Optional[PathInput] = None
    
    def compose(self) -> ComposeResult:
        """Compose the application layout."""
        yield Header()
        
        # Path input at the top
        self.path_input = PathInput(start_path=self.start_path, id="path_input")
        yield self.path_input
        
        # Main content area with tree and preview
        with Horizontal(id="main_content"):
            # Left panel: Tree view
            self.tree_view = TreeView(
                start_path=self.start_path,
                id="tree_view"
            )
            yield self.tree_view
            
            # Right panel: File preview
            self.file_preview = FilePreview(id="file_preview")
            yield self.file_preview
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize the application when mounted."""
        # Set initial focus to tree view
        if self.tree_view:
            self.tree_view.focus()
    
    # Message handlers
    def on_tree_view_directory_changed(self, message: TreeView.DirectoryChanged) -> None:
        """Handle directory changes from tree view."""
        if self.path_input:
            self.path_input.current_path = message.path
        
        # Clear file preview when directory changes
        if self.file_preview:
            self.file_preview.clear()
    
    def on_tree_view_file_selected(self, message: TreeView.FileSelected) -> None:
        """Handle file selection from tree view."""
        if self.file_preview:
            self.file_preview.set_file(message.path)
    
    def on_path_input_path_changed(self, message: PathInput.PathChanged) -> None:
        """Handle path changes from path input."""
        if self.tree_view:
            self.tree_view.navigate_to(message.path)
    
    def on_path_input_path_edit_started(self, message: PathInput.PathEditStarted) -> None:
        """Handle path edit start."""
        # Focus the path input when editing starts
        if self.path_input:
            self.path_input.focus()
    
    def on_path_input_path_edit_cancelled(self, message: PathInput.PathEditCancelled) -> None:
        """Handle path edit cancellation."""
        # Return focus to tree view
        if self.tree_view:
            self.tree_view.focus()
    
    # Action handlers
    def action_quit(self) -> None:
        """Quit the application."""
        self.exit()
    
    def action_show_help(self) -> None:
        """Show help information."""
        # In a full implementation, this would show a help modal
        self.bell()
    
    def action_refresh(self) -> None:
        """Refresh the current view."""
        if self.tree_view:
            self.tree_view.refresh_tree()
        
        if self.file_preview:
            self.file_preview.refresh_preview()
    
    def action_toggle_hidden(self) -> None:
        """Toggle showing hidden files."""
        if self.tree_view:
            self.tree_view.toggle_hidden()
    
    def action_edit_path(self) -> None:
        """Start editing the current path."""
        if self.path_input and not self.path_input.is_editing:
            self.path_input.start_editing()
    
    def action_focus_next(self) -> None:
        """Focus the next widget."""
        self.focus_next()
    
    def action_focus_previous(self) -> None:
        """Focus the previous widget."""
        self.focus_previous()
    
    def action_go_up(self) -> None:
        """Navigate to parent directory."""
        if self.tree_view:
            self.tree_view.go_up()
    
    # Key event handlers
    def on_key(self, event: events.Key) -> None:
        """Handle global key events."""
        # Let individual widgets handle their own keys first
        if event.is_printable and not self.path_input.is_editing:
            # If a printable key is pressed and we're not editing path,
            # start path editing
            if event.key == "g":
                self.action_edit_path()
                event.prevent_default()
    
    # Error handling
    def on_exception(self, exception: Exception) -> None:
        """Handle exceptions."""
        if self._debug:
            # In debug mode, let the exception propagate
            raise exception
        else:
            # In normal mode, show a simple error message
            self.bell()
            # In a full implementation, you might want to show an error modal 