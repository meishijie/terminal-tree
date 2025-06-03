#!/usr/bin/env python3
"""Main entry point for the terminal tree plugin."""

import sys
from pathlib import Path
from .app import TerminalTreeApp


def main():
    """Main entry point for the terminal tree plugin."""
    # Parse command line arguments
    start_path = Path.cwd()
    if len(sys.argv) > 1:
        provided_path = Path(sys.argv[1])
        if provided_path.exists() and provided_path.is_dir():
            start_path = provided_path
        else:
            print(f"Warning: '{provided_path}' is not a valid directory, using current directory.")
    
    # Create and run the app
    app = TerminalTreeApp(start_path=start_path)
    app.run()


if __name__ == "__main__":
    main() 