# Architecture Documentation

This document describes the technical architecture of txmd, a terminal-based markdown viewer.

## Table of Contents

- [Overview](#overview)
- [High-Level Architecture](#high-level-architecture)
- [Component Details](#component-details)
- [Data Flow](#data-flow)
- [Design Decisions](#design-decisions)
- [Technologies](#technologies)
- [Extension Points](#extension-points)

## Overview

txmd is a minimal, focused application built on three main pillars:

1. **CLI Interface** - Typer-based command-line argument parsing
2. **TUI Application** - Textual-based terminal user interface
3. **Pipeline Support** - Unix-style stdin/stdout integration

The application consists of a single Python module (`txmd/cli.py`) containing ~200 lines of code, making it easy to understand and maintain.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     User Input                          │
│              (File path or stdin pipe)                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  CLI Layer (Typer)                      │
│  ┌───────────────────────────────────────────────────┐  │
│  │  main() - Entry point                             │  │
│  │  - Parse arguments                                │  │
│  │  - Detect input source (file vs stdin)            │  │
│  │  - Read content                                   │  │
│  └────────────────────┬──────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              TUI Layer (Textual)                        │
│  ┌───────────────────────────────────────────────────┐  │
│  │  MarkdownViewerApp                                │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │  ScrollableContainer                        │  │  │
│  │  │    └─ Markdown Widget                       │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  │                                                   │  │
│  │  Key Bindings → Actions                           │  │
│  │    j/k → scroll_up/down                           │  │
│  │    Space/b → page_down/up                         │  │
│  │    Home/End → scroll_home/end                     │  │
│  │    q/Ctrl+C → quit                                │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Rendering Layer                            │
│  - Textual renders Markdown widget                      │
│  - Markdown parsed by Python-Markdown                   │
│  - Rich provides terminal formatting                    │
│  - Syntax highlighting for code blocks                  │
└─────────────────────────────────────────────────────────┘
```

## Component Details

### 1. CLI Layer (`main()`)

**Location:** `txmd/cli.py:179-214`

**Responsibilities:**
- Parse command-line arguments using Typer
- Determine input source (file path or stdin)
- Read and validate content
- Initialize and run TUI application
- Handle errors and display user-friendly messages

**Key Functions:**

#### `main(file: Optional[Path]) -> None`
Entry point for the CLI. Handles two input modes:

1. **File Mode:**
   ```python
   if file:
       with open(file, "r", encoding="utf-8") as f:
           content = f.read()
   ```

2. **Pipe Mode:**
   ```python
   else:
       stdin_content = read_stdin()
       if not stdin_content:
           # Error: no input
       content = stdin_content
   ```

#### `read_stdin() -> str`
**Location:** `txmd/cli.py:151-176`

Critical function for pipeline support:

```python
def read_stdin() -> str:
    if not sys.stdin.isatty():
        content = sys.stdin.read()
        # Reopen stdin as terminal
        try:
            sys.stdin.close()
            sys.__stdin__ = sys.stdin = open("/dev/tty")
        except Exception:
            pass
        return content
    return ""
```

**Why this matters:**
- When reading from a pipe, stdin is consumed and unavailable
- TUI needs stdin for keyboard input
- Solution: Read piped content, then reopen `/dev/tty` to restore terminal control
- This is the key insight that makes pipeline support work!

### 2. TUI Layer (`MarkdownViewerApp`)

**Location:** `txmd/cli.py:20-148`

**Responsibilities:**
- Create and manage terminal UI
- Handle user input (key bindings)
- Render markdown content
- Manage scrolling and navigation

**Architecture:**

```
MarkdownViewerApp (App)
    │
    ├─ CSS Styling
    │   └─ Defines colors, padding, layout
    │
    ├─ BINDINGS
    │   └─ Maps keys to action methods
    │
    ├─ compose() → ComposeResult
    │   └─ Creates widget hierarchy
    │
    └─ Action Methods
        ├─ action_quit()
        ├─ action_scroll_down()
        ├─ action_scroll_up()
        ├─ action_page_down()
        ├─ action_page_up()
        ├─ action_scroll_home()
        └─ action_scroll_end()
```

#### Widget Hierarchy

```
MarkdownViewerApp
  └─ ScrollableContainer
      └─ Markdown (Textual widget)
```

**Why this structure:**
- `ScrollableContainer`: Provides viewport and scrolling mechanics
- `Markdown`: Built-in Textual widget that handles markdown parsing and rendering
- Simple hierarchy = easy to understand and maintain

#### CSS Styling

**Location:** `txmd/cli.py:35-49`

```css
ScrollableContainer {
    width: 100%;
    height: 100%;
    background: $surface;
}

Markdown {
    width: 100%;
    height: auto;
    padding: 1 2;
    background: $surface;
    color: $text;
}
```

Uses Textual's design tokens (`$surface`, `$text`) for theme compatibility.

#### Key Bindings

**Location:** `txmd/cli.py:51-64`

Bindings map keys → action names → action methods:

```python
Binding("j", "scroll_down", "Scroll Down")
         │        │              │
       Key    Action Name    Description
```

When user presses `j`:
1. Textual looks up binding
2. Finds action name `"scroll_down"`
3. Calls `action_scroll_down()` method
4. Method queries ScrollableContainer and scrolls it

### 3. Rendering Layer

**Dependencies:**
- **Textual**: Provides the TUI framework and Markdown widget
- **Python-Markdown**: Parses markdown syntax (used internally by Textual)
- **Rich**: Terminal formatting and text rendering (used by Textual)

**Rendering Pipeline:**

```
Markdown Text
    │
    ▼
Python-Markdown Parser
    │
    ▼
Textual Markdown Widget
    │
    ▼
Rich Text Rendering
    │
    ▼
Terminal Display
```

**Not implemented in txmd:** The rendering is entirely handled by Textual's `Markdown` widget. We just pass it the content.

## Data Flow

### File Input Flow

```
┌──────────┐
│  User    │
│  $ txmd  │
│  file.md │
└────┬─────┘
     │
     ▼
┌─────────────────┐
│ main()          │
│ - file param    │
│ - open & read   │
└────┬────────────┘
     │
     ▼
┌─────────────────────┐
│ MarkdownViewerApp   │
│ __init__(content)   │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ app.run()           │
│ - compose()         │
│ - render            │
│ - event loop        │
└─────────────────────┘
```

### Pipeline Input Flow

```
┌──────────────────┐
│  User            │
│  $ cat file.md   │
│    | txmd         │
└────┬─────────────┘
     │
     ▼
┌─────────────────┐
│ main()          │
│ - no file param │
└────┬────────────┘
     │
     ▼
┌─────────────────────┐
│ read_stdin()        │
│ - detect pipe       │
│ - read content      │
│ - reopen /dev/tty   │  ← Critical step!
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ MarkdownViewerApp   │
│ __init__(content)   │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ app.run()           │
│ - reads from stdin  │  ← Now works because we reopened /dev/tty
│ - user can navigate │
└─────────────────────┘
```

### Event Flow (User Navigation)

```
┌──────────────────┐
│  User presses 'j'│
└────┬─────────────┘
     │
     ▼
┌─────────────────────────┐
│ Textual Event System    │
│ - Captures key press    │
│ - Looks up binding      │
└────┬────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│ BINDINGS lookup             │
│ "j" → "scroll_down" action  │
└────┬────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│ action_scroll_down()            │
│ - query_one(ScrollableContainer)│
│ - .scroll_down(animate=False)   │
└────┬────────────────────────────┘
     │
     ▼
┌─────────────────────────┐
│ ScrollableContainer     │
│ - Updates scroll offset │
│ - Triggers re-render    │
└────┬────────────────────┘
     │
     ▼
┌─────────────────────┐
│ Display updates     │
│ - Content scrolls   │
└─────────────────────┘
```

## Design Decisions

### 1. Single Module Architecture

**Decision:** Keep everything in one file (`cli.py`)

**Rationale:**
- Simple application (~200 lines)
- Easy to understand and navigate
- No complex module dependencies
- Quick onboarding for contributors

**Trade-off:** If the app grows significantly, refactoring into modules may be needed.

### 2. No Configuration Files

**Decision:** No config file support in v0.2.0

**Rationale:**
- Simplicity first
- Reduces complexity
- Most users don't need customization initially

**Future:** Configuration support is on the roadmap for future versions.

### 3. Textual Over Custom TUI

**Decision:** Use Textual framework instead of building custom TUI

**Rationale:**
- Mature, well-tested framework
- Handles complex terminal details
- Built-in Markdown widget
- Active development and community
- Cross-platform support

**Alternative considered:** Using curses directly (rejected: too low-level, requires more code)

### 4. /dev/tty Restoration for Pipelines

**Decision:** Reopen `/dev/tty` after reading stdin

**Rationale:**
- Only way to support pipelines AND interactive TUI
- stdin consumed by piped content
- Need terminal device for keyboard input
- Proven pattern in Unix tools

**Platform limitation:** Windows doesn't have `/dev/tty` (requires WSL or Windows Terminal workarounds)

### 5. No Animation on Scrolling

**Decision:** `animate=False` on all scroll operations

**Rationale:**
- Faster, more responsive feel
- Vim users expect instant response
- Reduces CPU usage
- Simpler code

### 6. Vim-Style Keybindings

**Decision:** Primary keybindings follow vim conventions

**Rationale:**
- Target audience: developers
- Vim keybindings are familiar
- Efficient navigation
- Also provide arrow keys for non-vim users

### 7. Dependency Minimization

**Decision:** Keep dependencies minimal and stable

**Current dependencies:**
- Textual (TUI framework) - required
- Typer (CLI) - required
- Rich (terminal formatting) - dependency of Textual
- Markdown (parsing) - dependency of Textual

**Rationale:**
- Easier installation
- Fewer potential conflicts
- Smaller package size
- Faster startup

## Technologies

### Core Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.9+ | Programming language |
| Textual | ^0.86.3 | TUI framework |
| Typer | ^0.13.1 | CLI framework |
| Rich | ^13.9.4 | Terminal formatting |
| Python-Markdown | ^3.7 | Markdown parsing |

### Development Tools

| Tool | Purpose |
|------|---------|
| Poetry | Dependency management |
| pytest | Testing framework |
| black | Code formatting |
| isort | Import sorting |
| flake8 | Linting |

### Why These Choices?

**Textual:**
- Modern, actively maintained
- Excellent documentation
- Built-in widgets (including Markdown)
- Reactive programming model
- CSS-like styling

**Typer:**
- Simple CLI definition
- Type-safe argument parsing
- Built on Click (battle-tested)
- Automatic help generation

**Poetry:**
- Modern Python packaging
- Deterministic builds
- Easy dependency management
- Virtual environment handling

## Extension Points

### Adding New Features

#### 1. New Keybindings

Add to `BINDINGS` list:

```python
BINDINGS = [
    # ... existing bindings
    Binding("n", "my_action", "My Action"),
]
```

Add corresponding action method:

```python
def action_my_action(self) -> None:
    """Description of action."""
    # Implementation
```

#### 2. Custom Styling

Modify the `CSS` string:

```python
CSS = """
ScrollableContainer {
    # Add new styles
}
"""
```

#### 3. Additional Widgets

Add widgets in `compose()`:

```python
def compose(self) -> ComposeResult:
    with ScrollableContainer():
        yield Header()  # New widget
        yield Markdown(self.content)
        yield Footer()  # New widget
```

#### 4. Configuration Support

Future enhancement structure:

```python
# config.py (future)
class Config:
    theme: str
    keybindings: Dict[str, str]
    display_options: Dict[str, Any]

def load_config() -> Config:
    # Load from ~/.config/txmd/config.yaml
    pass
```

#### 5. Plugin System

Future plugin architecture:

```python
# plugins.py (future)
class Plugin(ABC):
    @abstractmethod
    def on_load(self, app: MarkdownViewerApp):
        pass

    @abstractmethod
    def on_render(self, content: str) -> str:
        pass
```

### Testing New Features

Framework for testing:

```python
# tests/test_feature.py
from textual.app import App
from txmd.cli import MarkdownViewerApp

def test_new_feature():
    """Test new feature."""
    content = "# Test"
    app = MarkdownViewerApp(content)

    # Test implementation
    assert app.content == content
```

## Performance Considerations

### Memory

- Entire document loaded into memory
- Textual renders visible portion only
- Large files (>10MB) may cause issues

### Rendering

- Initial render: O(n) where n = document size
- Scrolling: O(1) - only updates viewport
- Syntax highlighting: Depends on code block size

### Optimization Strategies

1. **Lazy loading** (future): Load document chunks on demand
2. **Virtualization** (future): Render only visible content
3. **Caching**: Textual caches rendered content automatically

## Security Considerations

### Input Validation

- File paths validated by Typer (`exists=True`)
- No shell command execution
- No network requests
- No code evaluation

### Potential Risks

- **Malicious markdown:** Could contain very large files → DoS
- **Terminal escape codes:** Markdown could contain ANSI escapes
  - Mitigated by Textual's rendering layer

### Best Practices

- Don't run txmd with elevated privileges
- Be cautious with untrusted markdown files
- Review content before viewing if from untrusted source

## Future Architecture Considerations

### Multi-File Support

Potential architecture:

```python
class MultiFileApp(App):
    files: List[Path]
    current_index: int

    def action_next_file(self):
        self.current_index += 1
        self.reload()

    def action_prev_file(self):
        self.current_index -= 1
        self.reload()
```

### Search Functionality

Potential architecture:

```python
class SearchableMarkdownViewerApp(MarkdownViewerApp):
    search_term: str
    matches: List[int]  # Line numbers

    def action_search(self):
        # Open search input
        pass

    def action_next_match(self):
        # Jump to next match
        pass
```

### Theme System

Potential architecture:

```python
class Theme:
    name: str
    colors: Dict[str, str]
    css: str

class ThemeManager:
    themes: Dict[str, Theme]

    def load_theme(self, name: str) -> Theme:
        pass

    def apply_theme(self, app: App, theme: Theme):
        app.CSS = theme.css
```

## Conclusion

txmd's architecture is intentionally simple and focused:

- **Single module** for easy understanding
- **Textual framework** for robust TUI
- **Pipeline support** through `/dev/tty` restoration
- **Minimal dependencies** for reliability
- **Vim-style bindings** for efficient navigation

This architecture makes txmd easy to:
- Understand (small codebase)
- Maintain (clear structure)
- Extend (well-defined extension points)
- Test (simple components)

As the project grows, the architecture can evolve while maintaining these core principles.
