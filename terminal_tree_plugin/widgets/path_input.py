"""Path input widget with autocompletion."""

from pathlib import Path
from typing import List, Optional

from rich.text import Text
from textual import events
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Input, Static

from ..utils.path_utils import autocomplete_path, get_path_components, normalize_path, validate_path


class PathInput(Widget):
    """A path input widget with autocompletion and validation."""
    
    DEFAULT_CSS = """
    PathInput {
        height: 3;
        width: 1fr;
        border: solid $primary;
        background: $surface;
    }
    
    PathInput Input {
        background: $surface;
        color: $text;
        border: none;
    }
    
    PathInput Input:focus {
        background: $surface;
        border: solid $accent;
    }
    
    PathInput Static {
        background: $surface;
        color: $text;
        height: 1;
        padding: 0 1;
    }
    
    PathInput .path-valid {
        color: $success;
    }
    
    PathInput .path-invalid {
        color: $error;
    }
    
    PathInput .path-components {
        color: $text-muted;
    }
    """
    
    # Messages
    class PathChanged(Message):
        """Posted when a valid path is entered."""
        
        def __init__(self, path: Path) -> None:
            self.path = path
            super().__init__()
    
    class PathEditStarted(Message):
        """Posted when path editing starts."""
        pass
    
    class PathEditCancelled(Message):
        """Posted when path editing is cancelled."""
        pass
    
    # Reactive attributes
    current_path: reactive[Path] = reactive(Path.cwd())
    is_editing: reactive[bool] = reactive(False)
    
    def __init__(self, start_path: Optional[Path] = None, **kwargs) -> None:
        self._input: Optional[Input] = None
        self._status: Optional[Static] = None
        self._suggestions: List[str] = []
        super().__init__(**kwargs)
        self.current_path = start_path or Path.cwd()
    
    def compose(self):
        """Compose the path input widget."""
        self._input = Input(
            placeholder="Enter path...",
            id="path_input"
        )
        self._status = Static(
            self._get_path_display(),
            id="path_status"
        )
        
        yield self._input
        yield self._status
    
    def on_mount(self) -> None:
        """Initialize the widget when mounted."""
        self._update_display()
    
    def watch_current_path(self, new_path: Path) -> None:
        """React to current path changes."""
        self._update_display()
    
    def watch_is_editing(self, is_editing: bool) -> None:
        """React to editing state changes."""
        if self._input:
            if is_editing:
                self._input.value = str(self.current_path)
                self._input.focus()
                self.post_message(self.PathEditStarted())
            else:
                self._input.value = ""
                self._input.blur()
        
        self._update_display()
    
    def _get_path_display(self) -> Text:
        """Get the path display text."""
        if self.is_editing:
            return Text("Editing path... (Press Enter to confirm, Esc to cancel)", style="yellow")
        
        # Show path components as clickable breadcrumbs
        components = get_path_components(self.current_path)
        text = Text()
        
        for i, (name, path) in enumerate(components):
            if i > 0:
                text.append(" / ", style="dim")
            
            # Make each component clickable (in a real implementation)
            text.append(name, style="bold blue")
        
        return text
    
    def _update_display(self) -> None:
        """Update the display."""
        if self._status:
            self._status.update(self._get_path_display())
    
    def _validate_input(self, value: str) -> bool:
        """Validate the input path."""
        if not value.strip():
            return False
        
        try:
            path = normalize_path(value)
            is_valid, _ = validate_path(path)
            return is_valid
        except Exception:
            return False
    
    def _get_autocompletion(self, value: str) -> List[str]:
        """Get autocompletion suggestions."""
        if not value.strip():
            return []
        
        try:
            return autocomplete_path(value, self.current_path)
        except Exception:
            return []
    
    def start_editing(self) -> None:
        """Start editing the path."""
        self.is_editing = True
    
    def cancel_editing(self) -> None:
        """Cancel path editing."""
        self.is_editing = False
        self.post_message(self.PathEditCancelled())
    
    def confirm_path(self, path_str: str) -> None:
        """Confirm and set a new path."""
        try:
            path = normalize_path(path_str)
            is_valid, error = validate_path(path)
            
            if is_valid:
                self.current_path = path
                self.is_editing = False
                self.post_message(self.PathChanged(path))
            else:
                # Show error (in a real implementation, you might want to show this in the UI)
                pass
        except Exception:
            # Invalid path format
            pass
    
    def navigate_to_component(self, component_path: Path) -> None:
        """Navigate to a specific path component."""
        self.current_path = component_path
        self.post_message(self.PathChanged(component_path))
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes."""
        if not self.is_editing:
            return
        
        value = event.value
        
        # Update status based on validation
        if self._status:
            if self._validate_input(value):
                self._status.add_class("path-valid")
                self._status.remove_class("path-invalid")
                status_text = Text("✓ Valid path", style="green")
            else:
                self._status.add_class("path-invalid")
                self._status.remove_class("path-valid")
                status_text = Text("✗ Invalid path", style="red")
            
            self._status.update(status_text)
        
        # Get autocompletion suggestions
        self._suggestions = self._get_autocompletion(value)
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission."""
        if self.is_editing:
            self.confirm_path(event.value)
    
    def on_key(self, event: events.Key) -> None:
        """Handle key events."""
        if event.key == "escape" and self.is_editing:
            self.cancel_editing()
            event.prevent_default()
        elif event.key == "tab" and self.is_editing and self._suggestions:
            # Auto-complete with first suggestion
            if self._input and self._suggestions:
                self._input.value = self._suggestions[0]
            event.prevent_default()
        elif event.key == "g" and not self.is_editing:
            # Start editing
            self.start_editing()
            event.prevent_default()
        # Don't handle backspace here - let it bubble up to the app level 