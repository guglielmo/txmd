# txmd

A modern, feature-rich terminal-based Markdown viewer with pipeline support, 
built with [Textual](https://github.com/Textualize/textual).

![PyPI version](https://img.shields.io/pypi/v/txmd)
![Python versions](https://img.shields.io/pypi/pyversions/txmd)
![License](https://img.shields.io/pypi/l/txmd)

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

Inside the viewer:
- `↑`/`k`: Scroll up
- `↓`/`j`: Scroll down
- `Page Up`/`Page Down`: Scroll by page
- `Home`/`End`: Jump to top/bottom
- `q`: Quit the viewer

## Features in Detail

### Supported Markdown Elements

txmd supports all standard Markdown features:

- Headers (all levels)
- Bold and italic text
- Lists (ordered and unordered)
- Code blocks with syntax highlighting
- Tables
- Blockquotes
- Horizontal rules
- Links
- Images (ASCII art representation in terminal)

### Pipeline Integration

txmd is designed to work seamlessly in Unix pipelines. This means you can:

```bash
# View git diff in markdown
git diff | txmd

# View formatted man pages
man git | txmd

# Preview markdown before committing
git show HEAD:README.md | txmd
```

## Development

### Setting Up Development Environment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/txmd
cd txmd
```

2. Install development dependencies using Poetry:
```bash
poetry install
```

3. Run tests:
```bash
poetry run pytest
```

### Project Structure

```
txmd/
├── txmd/
│   ├── __init__.py
│   ├── cli.py          # CLI implementation
│   └── markdown_parser.py    # Markdown parsing logic
├── tests/
│   └── ...
├── pyproject.toml
└── README.md
```

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please make sure to update tests as appropriate and follow the existing code style.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Textual](https://github.com/Textualize/textual)
- Markdown parsing by [Python-Markdown](https://python-markdown.github.io/)
- Command-line interface by [Typer](https://typer.tiangolo.com/)

## FAQ

**Q: Why use txmd instead of other markdown viewers?**
A: txmd is designed to be lightweight, fast, and integrate seamlessly 
with Unix pipelines while providing a beautiful TUI interface.

**Q: Does txmd support custom themes?**
A: Not yet, but it's on our roadmap! Stay tuned for updates.

**Q: Can I use txmd to preview markdown before committing to git?**
A: Yes! Just pipe the content to txmd: `git show HEAD:README.md | txmd`

## Roadmap

- [ ] Custom theme support
- [ ] GitHub Flavored Markdown extensions
- [ ] Image preview support via terminal graphics protocols
- [ ] Configuration file support
- [ ] Search functionality
- [ ] Bookmark support for long documents

## Support

If you encounter any issues or have questions, 
please file an issue on the [GitHub repository](https://github.com/yourusername/txmd/issues).