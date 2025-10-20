# STATUS.md

## Current State

**Version**: 0.1.3
**Status**: Alpha (Development Status :: 3 - Alpha)
**Last Updated**: 2024-11-24

### Working Features

- ✅ Single markdown file viewing
- ✅ Pipeline/stdin support for piped content
- ✅ Vim-style navigation (j/k scrolling)
- ✅ Page navigation (space, b, PageUp/PageDown)
- ✅ Jump to top/bottom (Home/End)
- ✅ Standard markdown rendering via Textual's Markdown widget
- ✅ Syntax highlighting for code blocks
- ✅ Table support
- ✅ Terminal restoration after reading from stdin

### Known Limitations

- ❌ No multi-file support (cannot view multiple files simultaneously)
- ❌ No table of contents (TOC) generation or navigation
- ❌ No search functionality within documents
- ❌ No configuration file support
- ❌ No custom theme support
- ❌ No bookmark support for long documents
- ❌ No tab/window management for multiple documents

## Todo List

### High Priority Features

- [ ] **Dynamic Table of Contents (TOC)**
  - Parse markdown headers to generate TOC
  - Add sidebar/panel to display TOC structure
  - Implement navigation to jump to sections
  - Add keybinding to toggle TOC visibility (e.g., `t`)

- [ ] **Multi-file Support**
  - Accept multiple file arguments: `txmd file1.md file2.md file3.md`
  - Implement tab bar or file switcher UI
  - Add keybindings for tab navigation (e.g., `1-9` for tabs, `n`/`p` for next/prev)
  - Handle mixed stdin + file inputs

- [ ] **Search Functionality**
  - Add incremental search within current document
  - Keybinding to open search (e.g., `/` like vim)
  - Highlight search matches
  - Navigate between matches (n/N)

### Medium Priority Features

- [ ] **Bookmark Support**
  - Allow marking positions in long documents
  - Keybindings to set/jump to bookmarks
  - Persist bookmarks across sessions (optional)

- [ ] **Configuration File Support**
  - Support `~/.config/txmd/config.toml` or similar
  - Configurable keybindings
  - Default theme selection
  - UI preferences (show line numbers, TOC width, etc.)

- [ ] **Custom Theme Support**
  - Allow custom CSS themes
  - Built-in theme gallery (dark, light, solarized, etc.)
  - Theme hot-swapping during runtime

### Lower Priority Enhancements

- [ ] **GitHub Flavored Markdown (GFM) Extensions**
  - Task lists (- [ ] / - [x])
  - Strikethrough
  - Tables with alignment
  - Autolinks

- [ ] **Image Preview Support**
  - Terminal graphics protocol support (iTerm2, Kitty, Sixel)
  - Fallback to ASCII art or placeholder text
  - Image caching for performance

- [ ] **Line Numbers**
  - Optional line number display
  - Toggle with keybinding

- [ ] **Copy/Export Functionality**
  - Copy selected text to clipboard
  - Export rendered view to HTML or PDF

- [ ] **Follow Links**
  - Open external links in browser
  - Navigate to other markdown files (local links)

### Code Quality & Developer Experience

- [ ] **Test Coverage**
  - Add unit tests for CLI argument parsing
  - Add tests for stdin handling
  - Add integration tests for Textual app

- [ ] **Documentation**
  - Add API documentation
  - Create contribution guidelines
  - Add examples directory

- [ ] **CI/CD Pipeline**
  - Automated testing on push
  - Automated publishing to PyPI
  - Version management automation

## Recent Changes

### 0.1.3 (2024-11-24)
- Current published version on PyPI
- Basic markdown viewing functionality
- Pipeline support with stdin handling

## Notes

- Python support: 3.9 - 3.12
- Primary dependencies: Textual (^0.86.3), Typer (^0.13.1), Markdown (^3.7)
- Development tools: pytest, black, isort, flake8
