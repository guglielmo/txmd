# txmd

A modern, feature-rich terminal-based Markdown viewer with pipeline support,
built with [Textual](https://github.com/Textualize/textual).

![PyPI version](https://img.shields.io/pypi/v/txmd)
![Python versions](https://img.shields.io/pypi/pyversions/txmd)
![License](https://img.shields.io/pypi/l/txmd)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Pipeline Usage](#pipeline-usage)
  - [Navigation](#navigation)
  - [Keybindings Reference](#keybindings-reference)
- [Examples](#examples)
- [Supported Markdown Features](#supported-markdown-features)
- [Documentation](#documentation)
- [Development](#development)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [License](#license)

## Features

- 📝 Render Markdown files directly in your terminal
- 🔄 Pipeline support - pipe markdown content directly to txmd
- 🎨 Syntax highlighting for code blocks
- 📊 Table support
- 🖼️ Beautiful TUI interface powered by Textual
- ⌨️ Vim-style navigation (j/k for scrolling)
- 🚀 Fast and lightweight

## Installation

You can install txmd using pip:

```bash
pip install txmd
```

Or using Poetry:

```bash
poetry add txmd
```

## Usage

### Basic Usage

View a Markdown file:

```bash
txmd README.md
```

### Pipeline Usage

Pipe content to txmd:

```bash
echo "# Hello World" | txmd
cat document.md | txmd
curl https://raw.githubusercontent.com/user/repo/main/README.md | txmd
```

### Navigation

Inside the viewer, you can navigate using vim-style keys or traditional navigation keys:

**Basic Scrolling:**
- `j` or `↓` - Scroll down one line
- `k` or `↑` - Scroll up one line

**Page Scrolling:**
- `Space` or `Page Down` - Scroll down one page
- `b` or `Page Up` - Scroll up one page

**Jump to Position:**
- `Home` - Jump to the top of the document
- `End` - Jump to the bottom of the document

**Exit:**
- `q` or `Ctrl+C` - Quit the viewer

### Keybindings Reference

Complete list of all keybindings:

| Key(s) | Action | Description |
|--------|--------|-------------|
| `j`, `↓` | Scroll Down | Move down one line |
| `k`, `↑` | Scroll Up | Move up one line |
| `Space`, `Page Down` | Page Down | Scroll down by viewport height |
| `b`, `Page Up` | Page Up | Scroll up by viewport height |
| `Home` | Jump to Top | Scroll to the beginning of the document |
| `End` | Jump to Bottom | Scroll to the end of the document |
| `q`, `Ctrl+C` | Quit | Exit the application |

> **Note:** All scrolling operations happen instantly without animation for a responsive feel.

## Examples

txmd includes a collection of example markdown files demonstrating various features:

```bash
# View basic markdown features
txmd examples/basic.md

# See syntax highlighting for various languages
txmd examples/code-blocks.md

# Explore table formatting
txmd examples/tables.md

# Check out advanced features
txmd examples/advanced.md
```

See the [examples directory](examples/) for more information and sample files.

## Supported Markdown Features

txmd supports all standard Markdown elements through Textual's Markdown widget:

| Feature | Support | Notes |
|---------|---------|-------|
| **Headers** | ✅ Full | All levels (H1-H6) |
| **Text Formatting** | ✅ Full | Bold, italic, strikethrough |
| **Lists** | ✅ Full | Ordered, unordered, nested |
| **Code Blocks** | ✅ Full | Syntax highlighting for 100+ languages |
| **Inline Code** | ✅ Full | Monospace formatting |
| **Tables** | ✅ Full | With column alignment |
| **Blockquotes** | ✅ Full | Including nested quotes |
| **Horizontal Rules** | ✅ Full | Visual separators |
| **Links** | ✅ Full | Displayed with formatting |
| **Images** | ⚠️ Partial | Text representation in terminal |

### Code Syntax Highlighting

Syntax highlighting is supported for many languages including:
- Python, JavaScript, TypeScript, Rust, Go
- Java, C, C++, C#, Ruby, PHP
- Bash, Shell, PowerShell
- HTML, CSS, SCSS, JSON, YAML, TOML, XML
- SQL, Markdown, and many more

### Pipeline Integration

txmd is designed to work seamlessly in Unix pipelines. This means you can:

```bash
# Preview markdown before committing
git show HEAD:README.md | txmd

# View remote markdown files
curl -s https://raw.githubusercontent.com/user/repo/main/README.md | txmd

# View markdown from any command output
echo "# Dynamic Content\n\nGenerated at $(date)" | txmd

# Process and view markdown
grep -A 10 "## Section" document.md | txmd
```

**How it works:** txmd detects piped input, reads the content, and then restores terminal control by reopening `/dev/tty`. This allows the TUI to function normally even when receiving piped input.

> **Platform Note:** Full pipeline support works on Linux and macOS. On Windows, use WSL or Windows Terminal for best results.

## Documentation

Comprehensive documentation is available:

- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Detailed contribution guidelines, development setup, coding standards, and PR process
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical architecture, design decisions, and component details
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Solutions for common issues and debugging help
- **[CLAUDE.md](CLAUDE.md)** - AI assistant context and project overview
- **[examples/](examples/)** - Sample markdown files demonstrating features

## Development

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/guglielmo/txmd
   cd txmd
   ```

2. **Install Poetry** (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install dependencies:**
   ```bash
   poetry install
   ```

4. **Run from source:**
   ```bash
   poetry run txmd README.md
   ```

5. **Run tests:**
   ```bash
   poetry run pytest
   ```

### Code Quality

```bash
# Format code
poetry run black txmd/

# Sort imports
poetry run isort txmd/

# Lint code
poetry run flake8 txmd/

# Run all checks
poetry run black txmd/ && poetry run isort txmd/ && poetry run flake8 txmd/ && poetry run pytest
```

### Project Structure

```
txmd/
├── txmd/
│   ├── __init__.py      # Package initialization
│   └── cli.py           # Main application (CLI + TUI)
├── tests/
│   ├── __init__.py
│   └── test_cli.py      # Test suite
├── examples/            # Example markdown files
│   ├── basic.md
│   ├── code-blocks.md
│   ├── tables.md
│   ├── advanced.md
│   └── README.md
├── CONTRIBUTING.md      # Contribution guidelines
├── ARCHITECTURE.md      # Technical documentation
├── TROUBLESHOOTING.md   # Common issues and solutions
├── CLAUDE.md            # AI assistant context
├── pyproject.toml       # Poetry configuration
└── README.md            # This file
```

For detailed development information, see [CONTRIBUTING.md](CONTRIBUTING.md) and [ARCHITECTURE.md](ARCHITECTURE.md).

## Contributing

Contributions are welcome and appreciated! We'd love your help making txmd better.

### Quick Contribution Guide

1. **Fork and clone** the repository
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Run quality checks**:
   ```bash
   poetry run black txmd/
   poetry run isort txmd/
   poetry run flake8 txmd/
   poetry run pytest
   ```
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to your fork**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### What to Contribute

- 🐛 **Bug fixes** - Help us squash bugs
- ✨ **New features** - Add capabilities from the roadmap
- 📝 **Documentation** - Improve or add documentation
- ✅ **Tests** - Increase test coverage
- 🎨 **Examples** - Create new example markdown files

### Before Contributing

Please read our comprehensive [CONTRIBUTING.md](CONTRIBUTING.md) guide which covers:
- Development setup and workflow
- Coding standards and style guide
- Testing guidelines
- PR process and review guidelines
- Project architecture and structure

### Getting Help

- Check [existing issues](https://github.com/guglielmo/txmd/issues)
- Read the [TROUBLESHOOTING.md](TROUBLESHOOTING.md) guide
- Open a new issue for bugs or feature requests
- Join discussions on GitHub

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Textual](https://github.com/Textualize/textual)
- Markdown parsing by [Python-Markdown](https://python-markdown.github.io/)
- Command-line interface by [Typer](https://typer.tiangolo.com/)

## Troubleshooting

Having issues? Check our [TROUBLESHOOTING.md](TROUBLESHOOTING.md) guide for solutions to common problems:

- Installation issues
- Pipeline/stdin problems
- Display and rendering issues
- Platform-specific issues (Windows, macOS, Linux)
- Performance problems

### Quick Fixes

**Command not found after install:**
```bash
# Try running with python -m
python -m txmd README.md

# Or ensure ~/.local/bin is in PATH
export PATH="$HOME/.local/bin:$PATH"
```

**No colors/syntax highlighting:**
```bash
# Check terminal type
echo $TERM  # Should be something like xterm-256color

# Set if needed
export TERM=xterm-256color
```

**Pipeline not working on Windows:**
```bash
# Use WSL for full pipeline support
wsl -e txmd README.md
```

For more help, see the [full troubleshooting guide](TROUBLESHOOTING.md).

## FAQ

**Q: Why use txmd instead of other markdown viewers?**
A: txmd is designed to be lightweight, fast, and integrate seamlessly
with Unix pipelines while providing a beautiful TUI interface. It's perfect for developers who live in the terminal.

**Q: Does txmd support custom themes?**
A: Not yet, but it's on our roadmap! Custom theme support is planned for v0.2.0 or later.

**Q: Can I use txmd to preview markdown before committing to git?**
A: Absolutely! `git show HEAD:README.md | txmd` or `git diff main...HEAD | txmd`

**Q: Does txmd work on Windows?**
A: Yes, but for best results use Windows Terminal or WSL. Pipeline support works best on Linux/macOS or WSL.

**Q: Can I view multiple files at once?**
A: Not yet, but multi-file support with tabs is on the roadmap!

**Q: How do I report a bug or request a feature?**
A: Open an issue on [GitHub](https://github.com/guglielmo/txmd/issues) with details about the bug or feature request.

## Roadmap

### v0.2.0 - Enhanced Features (In Progress)

Priority features currently being developed:

- [ ] **Multi-file support** - View multiple markdown files with tab navigation
- [ ] **Search functionality** - Find text within documents with incremental search
- [ ] **Bookmark support** - Mark and jump to important sections
- [ ] **Custom themes** - Support for custom color schemes and styling

### Future Versions

Additional features planned for future releases:

- [ ] **Configuration file** - User preferences and custom keybindings
- [ ] **GitHub Flavored Markdown** - Extended markdown syntax support
- [ ] **Image preview** - Terminal graphics protocol support (Kitty, iTerm2)
- [ ] **TOC navigation** - Quick jump to headers
- [ ] **Export functionality** - Convert to HTML, PDF
- [ ] **Watch mode** - Auto-reload on file changes
- [ ] **Split view** - View two documents side by side

See the [GitHub issues](https://github.com/guglielmo/txmd/issues) and [project milestones](https://github.com/guglielmo/txmd/milestones) for more details.

## Support

### Getting Help

- 📖 **Documentation**: Check the [docs](#documentation) section above
- 🐛 **Bug Reports**: [Open an issue](https://github.com/guglielmo/txmd/issues/new) with details
- 💡 **Feature Requests**: [Request features](https://github.com/guglielmo/txmd/issues/new) through GitHub issues
- 💬 **Discussions**: Join [GitHub Discussions](https://github.com/guglielmo/txmd/discussions) for questions and ideas
- 🔧 **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Project Links

- **Repository**: https://github.com/guglielmo/txmd
- **Issue Tracker**: https://github.com/guglielmo/txmd/issues
- **PyPI Package**: https://pypi.org/project/txmd/
- **Changelog**: See [GitHub Releases](https://github.com/guglielmo/txmd/releases)