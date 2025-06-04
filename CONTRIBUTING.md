# Contributing to Terminal Tree

Thank you for your interest in contributing to Terminal Tree! 🌲

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git

### Setting Up Development Environment

1. **Fork and Clone**

   ```bash
   git clone https://github.com/yourusername/terminal-tree.git
   cd terminal-tree
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt

   # For development dependencies
   pip install -e ".[dev]"
   ```

3. **Run the Application**
   ```bash
   python run.py
   ```

## 🛠️ Development Guidelines

### Code Style

- Follow PEP 8 guidelines
- Use Black for code formatting: `black .`
- Use isort for import sorting: `isort .`
- Type hints are encouraged

### Testing

- Write tests for new features
- Run tests with: `pytest`
- Ensure all tests pass before submitting

### Commit Messages

Use clear, descriptive commit messages:

- `feat: add new feature`
- `fix: resolve bug in file preview`
- `docs: update README`
- `style: format code with black`

## 📝 How to Contribute

### Reporting Bugs

1. Check if the issue already exists
2. Create a new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version)

### Suggesting Features

1. Open an issue with the "enhancement" label
2. Describe the feature and its benefits
3. Provide examples if possible

### Submitting Pull Requests

1. **Create a Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**

   - Write clean, documented code
   - Add tests if applicable
   - Update documentation

3. **Test Your Changes**

   ```bash
   python run.py  # Test the main application
   pytest         # Run tests
   ```

4. **Submit PR**
   - Push your branch
   - Create a pull request
   - Describe your changes clearly

## 🏗️ Project Structure

```
terminal-tree/
├── terminal_tree_plugin/     # Core application
│   ├── app.py               # Main application
│   ├── main.py              # Entry point
│   ├── widgets/             # UI components
│   ├── utils/               # Utility functions
│   └── styles/              # CSS styles
├── examples/                # Example applications
├── scripts/                 # Installation scripts
└── tests/                   # Test files
```

## 🎯 Areas for Contribution

- **Features**: New functionality, UI improvements
- **Performance**: Optimization, caching
- **Documentation**: README, code comments, examples
- **Testing**: Unit tests, integration tests
- **Accessibility**: Keyboard navigation, screen readers
- **Internationalization**: Multi-language support

## 📋 Development Tasks

### Easy (Good First Issues)

- Fix typos in documentation
- Add new file type icons
- Improve error messages
- Add keyboard shortcuts

### Medium

- Add new preview formats
- Implement search functionality
- Add configuration options
- Performance optimizations

### Advanced

- Plugin system
- Remote file system support
- Advanced filtering
- Custom themes

## 🤝 Code of Conduct

- Be respectful and inclusive
- Help others learn and grow
- Focus on constructive feedback
- Celebrate diversity of ideas

## 📞 Getting Help

- **Issues**: For bugs and feature requests
- **Discussions**: For questions and ideas
- **Email**: For security issues

## 🙏 Recognition

Contributors will be:

- Listed in the README
- Mentioned in release notes
- Credited in the project

Thank you for making Terminal Tree better! 🌟
