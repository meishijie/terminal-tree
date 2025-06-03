# 🌲 Terminal Tree

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Textual](https://img.shields.io/badge/Framework-Textual-green)](https://github.com/textualize/textual)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

A modern terminal file system navigator based on the [Textual](https://github.com/textualize/textual) framework, providing an interactive, colorful user experience as an alternative to the traditional `tree` command.

## ✨ Key Features

- 🌳 **Interactive Navigation** - Browse the file system with keyboard controls, support for expanding/collapsing directories
- 📄 **File Preview** - Syntax-highlighted code file preview supporting multiple file formats
- 🔍 **Smart Path** - Path editing and auto-completion functionality
- 🎨 **Modern Interface** - Beautiful terminal user interface based on Textual
- ⚡ **Multiple Versions** - Full version, simplified version, and compact version for different terminal sizes
- 🔧 **Easy Integration** - Can completely replace the system's tree command

## 🎬 Demo

```
📁 terminal-tree/
├── 📁 terminal_tree_plugin/
│   ├── 📄 app.py (5.7KB)
│   ├── 📁 widgets/
│   │   ├── 📄 tree_view.py (8.1KB)
│   │   ├── 📄 file_preview.py (4.2KB)
│   │   └── 📄 path_input.py (6.8KB)
│   └── 📁 utils/
├── 📄 run.py (1.2KB)
└── 📄 README.md (4.5KB)
```

### Keyboard Shortcuts

- **Navigation**: `↑↓` Move up/down, `←→` Expand/collapse directories
- **Actions**: `Enter` Enter directory, `Backspace` Go back to parent
- **Features**: `g` Edit path, `F5` Refresh, `Ctrl+H` Show/hide hidden files
- **Others**: `Tab` Switch panels, `q` Quit

## 🚀 Quick Start

### Installation

1. **Clone Repository**

   ```bash
   git clone https://github.com/yourusername/terminal-tree.git
   cd terminal-tree
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run Application**

   ```bash
   python run.py

   # Or specify a directory
   python run.py /path/to/directory
   ```

### System Integration (Optional)

To replace the system's `tree` command:

```bash
# Configure shell aliases
chmod +x scripts/setup_tree_aliases.sh
./scripts/setup_tree_aliases.sh

# Reload shell configuration
source ~/.zshrc  # or ~/.bashrc

# Now you can use directly
tree              # Launch Terminal Tree
tree /usr/local   # Launch in specified directory
```

## 📁 Project Structure

```
terminal-tree/
├── terminal_tree_plugin/     # Core application code
│   ├── app.py               # Main application class
│   ├── main.py              # Entry point
│   ├── widgets/             # UI components
│   │   ├── tree_view.py     # File tree component
│   │   ├── file_preview.py  # File preview component
│   │   └── path_input.py    # Path input component
│   ├── utils/               # Utility functions
│   │   ├── file_utils.py    # File operations
│   │   └── path_utils.py    # Path handling
│   └── styles/              # CSS styles
│       └── app.tcss         # Textual style file
├── examples/                # Different version examples
│   ├── simple_tree_app.py   # Simplified version
│   └── compact_tree.py      # Compact version
├── scripts/                 # Installation and configuration scripts
│   ├── setup_tree_aliases.sh
│   ├── install_simple_tree.sh
│   └── test_tree_setup.sh
├── run.py                   # Main startup script
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Project configuration
└── README.md               # Project documentation
```

## 🛠️ Version Descriptions

| Version     | File                          | Features                                              | Use Case                         |
| ----------- | ----------------------------- | ----------------------------------------------------- | -------------------------------- |
| **Full**    | `run.py`                      | Three-panel layout, file preview, syntax highlighting | Daily development, full-featured |
| **Simple**  | `examples/simple_tree_app.py` | Two-panel layout, basic functionality                 | Medium terminal windows          |
| **Compact** | `examples/compact_tree.py`    | Single-panel layout, minimal interface                | Small terminal windows           |

## 🔧 Development

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/terminal-tree.git
cd terminal-tree

# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/  # if tests exist

# Run application
python run.py
```

### Code Structure

- **`terminal_tree_plugin/app.py`** - Main application class, handles overall layout and events
- **`terminal_tree_plugin/widgets/`** - Custom UI components
- **`terminal_tree_plugin/utils/`** - Utility functions and helper classes
- **`terminal_tree_plugin/styles/`** - Textual CSS styles

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Contribution Guidelines

- Maintain consistent code style
- Add appropriate documentation and comments
- Ensure new features have corresponding tests
- Update README if necessary

## 📝 Changelog

### v1.0.0

- ✨ Initial release
- 🌳 Interactive file tree navigation
- 📄 File preview functionality
- 🎨 Modern interface design
- ⌨️ Complete keyboard shortcut support

## ❓ FAQ

**Q: How to exit the application?**
A: Press `q` key or `Ctrl+C`

**Q: Why can't I see hidden files?**
A: Press `Ctrl+H` to toggle hidden file visibility

**Q: How to quickly jump to a specific path?**
A: Press `g` to enter path editing mode

**Q: What file previews are supported?**
A: Supports text files and code files with syntax highlighting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Will McGugan](https://github.com/willmcgugan) - Creator of the excellent Textual framework
- [Textual](https://github.com/textualize/textual) - Modern Python TUI framework
- [Rich](https://github.com/textualize/rich) - Terminal text beautification library

---

⭐ If this project helps you, please give it a Star!

🐛 Found a problem? [Submit an Issue](https://github.com/yourusername/terminal-tree/issues)

🌲 Enjoy the modern terminal file browsing experience!
