# Advanced Markdown Features

This example showcases more advanced markdown features and use cases for txmd.

## Nested Structures

### Complex Lists with Code

1. **Setup Development Environment**
   - Install Python 3.9+
   - Install Poetry:
     ```bash
     curl -sSL https://install.python-poetry.org | python3 -
     ```
   - Clone the repository:
     ```bash
     git clone https://github.com/guglielmo/txmd.git
     cd txmd
     ```

2. **Install Dependencies**
   - Production dependencies:
     ```bash
     poetry install --no-dev
     ```
   - Development dependencies:
     ```bash
     poetry install
     ```

3. **Run Tests**
   - All tests:
     ```bash
     poetry run pytest
     ```
   - Specific test:
     ```bash
     poetry run pytest tests/test_cli.py::test_function_name
     ```

## Nested Blockquotes

> ### Main Quote
>
> This is the main blockquote.
>
> > #### Nested Quote
> >
> > This quote is nested inside the main quote.
> >
> > > ##### Deeply Nested
> > >
> > > This is even more deeply nested.
>
> Back to the main quote level.

## Mixed Content

### Tutorial: Using txmd in Pipelines

You can pipe content directly to txmd from various sources:

**From a file:**
```bash
cat README.md | txmd
```

**From curl:**
```bash
curl -s https://raw.githubusercontent.com/user/repo/main/README.md | txmd
```

**From git:**
```bash
git show HEAD:README.md | txmd
```

**From echo:**
```bash
echo "# Quick Note\n\nThis is a quick markdown note." | txmd
```

> **Tip**: txmd automatically handles terminal restoration after reading from stdin,
> so you can use navigation keys normally even when piping content.

### Configuration Example

Here's an example of how you might configure txmd (when configuration support is added):

```yaml
# ~/.config/txmd/config.yaml
theme: dracula

keybindings:
  scroll_down:
    - j
    - down
  scroll_up:
    - k
    - up
  quit:
    - q
    - ctrl+c

display:
  line_numbers: false
  wrap_text: true
  max_width: 100
```

## Task Lists

- [x] Basic markdown rendering
- [x] Vim-style navigation
- [x] Pipeline support
- [x] Syntax highlighting
- [ ] Search functionality
- [ ] Bookmark support
- [ ] Custom themes
- [ ] Multi-file support

## Definition Lists (if supported)

Term 1
: Definition of term 1
: Another definition for term 1

Term 2
: Definition of term 2

## Footnotes (if supported)

Here's a sentence with a footnote.[^1]

Another sentence with a different footnote.[^2]

[^1]: This is the first footnote.
[^2]: This is the second footnote.

## Abbreviations

The HTML specification is maintained by the W3C.

*[HTML]: Hyper Text Markup Language
*[W3C]: World Wide Web Consortium

## Code with Line Numbers

Here's a complete Python script:

```python
#!/usr/bin/env python3
"""Example script demonstrating txmd usage."""

import subprocess
import sys
from pathlib import Path


def view_markdown(file_path: Path) -> None:
    """View a markdown file using txmd.

    Args:
        file_path: Path to the markdown file.
    """
    if not file_path.exists():
        print(f"Error: {file_path} not found", file=sys.stderr)
        sys.exit(1)

    subprocess.run(["txmd", str(file_path)])


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python script.py <markdown_file>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    view_markdown(file_path)


if __name__ == "__main__":
    main()
```

## Mathematical Expressions (if supported)

Inline math: $E = mc^2$

Block math:

$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$

## Real-World Use Case

### Viewing Git Commit Messages

You can use txmd to view formatted git commit messages:

```bash
git log --pretty=format:"# Commit: %h%n**Author:** %an <%ae>%n**Date:** %ad%n%n## Message%n%n%s%n%n%b" -1 | txmd
```

This creates a nicely formatted view of your latest commit.

### Documentation Preview

When writing documentation, preview your changes before committing:

```bash
# Watch and preview changes
while true; do
    clear
    cat docs/api.md | txmd
    sleep 2
done
```

### Clipboard Integration

On macOS, you can view clipboard content as markdown:

```bash
pbpaste | txmd
```

On Linux with xclip:

```bash
xclip -selection clipboard -o | txmd
```

## Performance Considerations

When viewing very large documents:

1. **Memory**: txmd loads the entire document into memory
2. **Rendering**: Initial render time depends on document size
3. **Scrolling**: Scrolling is optimized for smooth performance
4. **Syntax Highlighting**: Complex code blocks may take longer to render

**Tip**: For very large files (>10MB), consider viewing sections:

```bash
head -n 1000 large-file.md | txmd
```
