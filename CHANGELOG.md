# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-06-03

### Added

- 🌳 Interactive file system navigation with tree view
- 📄 File preview with syntax highlighting
- 🔍 Path editing with auto-completion
- ⌨️ Comprehensive keyboard shortcuts
- 🎨 Modern terminal UI using Textual framework
- 📋 Multiple app versions (full, simple, compact)
- 🔧 System integration scripts
- 📚 Complete documentation

### Features

- **Tree Navigation**: Expand/collapse directories, file icons
- **File Preview**: Code syntax highlighting, multiple file format support
- **Path Input**: Edit paths directly, breadcrumb navigation
- **Keyboard Shortcuts**:
  - `↑↓←→` for navigation
  - `Enter` to enter directories
  - `Backspace` to go up one level
  - `g` to edit path
  - `F5` to refresh
  - `Ctrl+H` to toggle hidden files
  - `Tab` to switch panels
  - `q` to quit

### Technical

- Built with Python 3.8+ and Textual framework
- Modular architecture with reusable components
- CSS-based styling system
- Cross-platform compatibility
- Minimal dependencies (textual, rich)

### Documentation

- Comprehensive README with installation instructions
- Examples directory with different app versions
- Scripts directory with installation and setup tools
- Inline code documentation

### Fixed

- ✅ Backspace key functionality for returning to parent directory
- ✅ Event handling conflicts between components
- ✅ Tree node expansion and collapse reliability
- ✅ Path validation and error handling

## [Unreleased]

### Planned

- 🔍 File search functionality
- 📊 Directory size visualization
- 🎨 Customizable themes
- 🔌 Plugin system
- 📱 Mobile terminal optimization
- 🌐 Remote file system support
