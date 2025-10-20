# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

txmd is a terminal-based Markdown viewer built with Textual. It provides a rich TUI interface for viewing Markdown files and supports Unix pipeline integration, allowing users to pipe markdown content directly to the viewer.

## Development Commands

### Environment Setup
```bash
poetry install
```

### Testing
```bash
# Run all tests
poetry run pytest

# Run with coverage report
poetry run pytest --cov=txmd --cov-report=term-missing

# Run specific test file
poetry run pytest tests/test_toc.py -v

# Run specific test class or method
poetry run pytest tests/test_ui.py::TestTOCToggle::test_toc_toggle_shows_and_hides -v
```

### Code Quality
```bash
# Format code
poetry run black txmd/ tests/

# Sort imports
poetry run isort txmd/ tests/

# Lint code
poetry run flake8 txmd/ tests/

# Run all quality checks
poetry run black txmd/ tests/ && poetry run isort txmd/ tests/ && poetry run flake8 txmd/ tests/ && poetry run pytest
```

### Running the Application
```bash
# Run from source during development
poetry run txmd README.md

# Or pipe content
echo "# Test" | poetry run txmd
```

### Building and Publishing
```bash
# Build the package
poetry build

# Version is managed in pyproject.toml (currently 0.4.0)
```

## Architecture

### Core Components

**txmd/cli.py** - Main application entry point
- `MarkdownViewerApp`: Textual application class that renders markdown content
- `main()`: Typer CLI command that handles file/stdin input
- `read_stdin()`: Handles stdin detection and terminal restoration

**txmd/toc.py** - Table of Contents module
- `parse_markdown_headers()`: Extracts headers from markdown content using regex
- `build_toc_tree()`: Builds hierarchical tree structure from flat header list
- `HeaderNode`: Data class representing nodes in the TOC tree

### Key Design Patterns

**Pipeline Support Implementation**
The application detects if it's receiving piped input via `sys.stdin.isatty()`. When reading from stdin, it must restore terminal control by reopening `/dev/tty` (see txmd/cli.py:102-107) to allow Textual to interact with the terminal for the TUI.

**Textual App Structure**
- Uses overlay approach with CSS layers for TOC display
- TOC `Tree` widget uses `layer: overlay` to appear on top of content
- Content `ScrollableContainer` shifts right when TOC is visible via `margin-left` and CSS class `toc-visible`
- `Markdown` widget (from Textual) handles rendering
- Action methods (e.g., `action_scroll_down()`) respond to key bindings
- Custom CSS defines the visual styling
- Focus management prevents TOC from stealing input when hidden (`can_focus` property)

**Table of Contents Implementation**
The TOC feature provides dynamic navigation through markdown documents:
- Hidden by default, toggled with 't' key
- Parses ATX-style headers (# through ######) on mount via `_populate_toc()`
- Filters out headers in code blocks (fenced ``` and ~~~ blocks, indented 4-space blocks)
- Builds hierarchical tree structure preserving header nesting
- Tree widget allows expand/collapse of nested sections
- Leaf nodes (no children) have `allow_expand = False` for cleaner UI
- Enhanced keyboard navigation:
  - Arrow keys: Navigate TOC entries
  - Enter: Expand/collapse branches (handled in `on_key()`)
  - Space: Jump to section positioned at top (handled in `action_page_down()`)
- Clicking a TOC entry scrolls to the corresponding header
- Scroll position calculated using `markdown_widget.virtual_size.height` for accuracy
- TOC visibility controlled via CSS classes (`.visible` on tree, `toc-visible` on content)
- TOC width: 40 columns, content margin-left: 40 when visible

### Key Dependencies
- **Textual (^0.86.3)**: TUI framework providing the Markdown widget and app infrastructure
- **Typer (^0.13.1)**: CLI framework for argument parsing
- **Markdown (^3.7)**: Used by Textual's Markdown widget for parsing
- **Rich (^13.9.4)**: Terminal formatting (used for console error messages)
- **pytest-asyncio (^1.2.0)**: Dev dependency for async UI testing (configured with `asyncio_mode = "auto"`)

## Testing Strategy

The project has three test suites:

**tests/test_cli.py** - CLI and application initialization tests
- Tests file and stdin input handling
- Verifies version flag functionality
- Tests error handling and edge cases

**tests/test_toc.py** - Table of Contents parsing and tree building (100% coverage)
- Comprehensive tests for `parse_markdown_headers()` including code block filtering
- Tests for `build_toc_tree()` with various nesting scenarios
- Tests for `HeaderNode` dataclass

**tests/test_ui.py** - UI interaction tests using Textual's `run_test()` framework
- TOC toggle and visibility tests
- Scroll keybinding tests (tests functionality, not exact scroll positions)
- TOC navigation and section jumping tests
- Code block filtering verification
- Focus management tests

When writing UI tests:
- Use `async with app.run_test(size=(80, 30)) as pilot:` for custom terminal sizes
- Call `await pilot.pause()` after actions to allow message processing
- Use `await pilot.press("key")` to simulate keypresses
- Avoid testing exact scroll positions (fragile in test mode); verify actions don't crash instead
- Check widget state via `app.query_one()` and CSS classes

## Navigation Keybindings

The app uses vim-style navigation defined in `BINDINGS`:
- `j`/`k`: Line scrolling
- `space`/`b`: Page scrolling
- Arrow keys, Home/End also supported
- `t`: Toggle Table of Contents visibility
- `q` or `Ctrl+C`: Quit

When modifying keybindings, update the `BINDINGS` list with `Binding()` objects in txmd/cli.py.

## Python Version Support

Supports Python 3.9-3.12 (see pyproject.toml classifiers). Minimum version is 3.9.

## Entry Point

The CLI is exposed via Poetry scripts configuration:
```toml
[tool.poetry.scripts]
txmd = "txmd.cli:app"
```

This means `txmd` command invokes the `app` Typer instance from `txmd.cli`.
