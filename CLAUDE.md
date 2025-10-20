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

# Version is managed in pyproject.toml (currently 0.1.3)
```

## Architecture

### Core Components

**txmd/cli.py** - Main application entry point
- `MarkdownViewerApp`: Textual application class that renders markdown content
- `main()`: Typer CLI command that handles file/stdin input
- `read_stdin()`: Handles stdin detection and terminal restoration

### Key Design Patterns

**Pipeline Support Implementation**
The application detects if it's receiving piped input via `sys.stdin.isatty()`. When reading from stdin, it must restore terminal control by reopening `/dev/tty` (see txmd/cli.py:102-107) to allow Textual to interact with the terminal for the TUI.

**Textual App Structure**
- Uses `ScrollableContainer` for viewport management
- `Markdown` widget (from Textual) handles rendering
- Action methods (e.g., `action_scroll_down()`) respond to key bindings
- Custom CSS defines the visual styling

### Key Dependencies
- **Textual (^0.86.3)**: TUI framework providing the Markdown widget and app infrastructure
- **Typer (^0.13.1)**: CLI framework for argument parsing
- **Markdown (^3.7)**: Used by Textual's Markdown widget for parsing
- **Rich (^13.9.4)**: Terminal formatting (used for console error messages)

## Navigation Keybindings

The app uses vim-style navigation defined in `BINDINGS` (txmd/cli.py:40-53):
- `j`/`k`: Line scrolling
- `space`/`b`: Page scrolling
- Arrow keys, Home/End also supported
- `q` or `Ctrl+C`: Quit

When modifying keybindings, update the `BINDINGS` list with `Binding()` objects.

## Python Version Support

Supports Python 3.9-3.12 (see pyproject.toml classifiers). Minimum version is 3.9.

## Entry Point

The CLI is exposed via Poetry scripts configuration:
```toml
[tool.poetry.scripts]
txmd = "txmd.cli:app"
```

This means `txmd` command invokes the `app` Typer instance from `txmd.cli`.
