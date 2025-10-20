# STATUS.md

## Current State

**Version**: 0.4.0
**Status**: Alpha (Development Status :: 3 - Alpha)
**Last Updated**: 2025-01-20

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
- ✅ **Dynamic Table of Contents (TOC)**
  - Hierarchical tree structure showing document headers
  - Toggle with 't' key
  - Navigate with arrow keys, Enter to expand/collapse, Space to jump to section
  - Filters out headers in code blocks
  - Content shifts right when TOC is visible

### Known Limitations

- ❌ No multi-file support (cannot view multiple files simultaneously)
- ❌ No search functionality within documents
- ❌ No configuration file support
- ❌ No custom theme support
- ❌ No bookmark support for long documents
- ❌ No tab/window management for multiple documents

## Todo List

### High Priority Features

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

- [x] **Test Coverage** (84% overall coverage)
  - ✅ Unit tests for CLI argument parsing
  - ✅ Tests for stdin handling
  - ✅ UI interaction tests for Textual app
  - ✅ Comprehensive TOC parsing and tree building tests

- [x] **Documentation**
  - ✅ Comprehensive README with usage examples
  - ✅ CONTRIBUTING.md with contribution guidelines
  - ✅ ARCHITECTURE.md with technical details
  - ✅ Examples directory with sample markdown files
  - ✅ CLAUDE.md for AI assistant context

- [ ] **CI/CD Pipeline**
  - Automated testing on push
  - Automated publishing to PyPI
  - Version management automation

## Recent Changes

### 0.4.0 (2025-01-20)
- **Major Feature**: Dynamic Table of Contents (TOC)
  - Hierarchical tree view of document headers
  - Toggle TOC visibility with 't' key
  - Navigate to sections with Space key
  - Expand/collapse tree branches with Enter
  - Filters headers in code blocks
  - Content shifts when TOC is visible
- **Testing**: Added comprehensive UI interaction tests (84% coverage)
- Added pytest-asyncio for async testing support
- Updated documentation (CLAUDE.md, STATUS.md)

### 0.3.0 (2024-11-24)
- Added --version flag
- Improved documentation
- Fixed code quality issues

### 0.1.3 (2024-11-24)
- Initial published version on PyPI
- Basic markdown viewing functionality
- Pipeline support with stdin handling

## Notes

- Python support: 3.9 - 3.12
- Primary dependencies: Textual (^0.86.3), Typer (^0.13.1), Markdown (^3.7)
- Development tools: pytest, pytest-asyncio, pytest-cov, black, isort, flake8
