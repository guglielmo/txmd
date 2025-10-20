# Tables Example

This example demonstrates various table formats supported by txmd.

## Basic Table

| Feature | Description | Status |
|---------|-------------|--------|
| Vim navigation | j/k keys for scrolling | ✅ Implemented |
| Pipeline support | stdin integration | ✅ Implemented |
| Search | Find text in document | 🚧 Planned |
| Themes | Custom color schemes | 🚧 Planned |

## Alignment Examples

### Left, Center, and Right Alignment

| Left Aligned | Center Aligned | Right Aligned |
|:-------------|:--------------:|--------------:|
| Left | Center | Right |
| Text | Text | Text |
| 123 | 456 | 789 |

## Complex Table

### Comparison Table

| Language | Typing | Compiled | Use Case |
|----------|--------|----------|----------|
| Python | Dynamic | No | Scripting, Data Science, Web |
| Rust | Static | Yes | Systems, Performance |
| JavaScript | Dynamic | No | Web, Node.js |
| Go | Static | Yes | Backend, DevOps |
| TypeScript | Static | Yes (to JS) | Web, Enterprise |

## Package Information

| Package | Version | Description |
|---------|---------|-------------|
| textual | ^0.86.3 | TUI framework |
| typer | ^0.13.1 | CLI framework |
| rich | ^13.9.4 | Terminal formatting |
| markdown | ^3.7 | Markdown parsing |

## Key Bindings Reference

| Key | Action | Description |
|-----|--------|-------------|
| `j` / `↓` | Scroll Down | Move down one line |
| `k` / `↑` | Scroll Up | Move up one line |
| `Space` / `PgDn` | Page Down | Scroll down one page |
| `b` / `PgUp` | Page Up | Scroll up one page |
| `Home` | Top | Jump to document start |
| `End` | Bottom | Jump to document end |
| `q` / `Ctrl+C` | Quit | Exit the viewer |

## Emoji Support

| Category | Emoji | Description |
|----------|-------|-------------|
| Status | ✅ | Completed |
| Status | 🚧 | In Progress |
| Status | ❌ | Not Started |
| Actions | 📝 | Document |
| Actions | 🔍 | Search |
| Actions | ⚙️ | Settings |

## Markdown Elements Support

| Element | Supported | Notes |
|---------|-----------|-------|
| Headers (H1-H6) | ✅ | All levels supported |
| **Bold** | ✅ | Full support |
| *Italic* | ✅ | Full support |
| Lists | ✅ | Ordered and unordered |
| Code Blocks | ✅ | With syntax highlighting |
| Tables | ✅ | With alignment |
| Links | ✅ | Clickable in terminals that support it |
| Images | ⚠️ | ASCII representation |
| Blockquotes | ✅ | Full support |
