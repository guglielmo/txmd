# txmd/cli.py
import sys
from pathlib import Path
from typing import Dict, Optional

import typer
from rich.console import Console
from textual import events
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import ScrollableContainer
from textual.widgets import Markdown, Tree
from textual.widgets.tree import TreeNode

from txmd import __version__
from txmd.toc import HeaderNode, build_toc_tree, parse_markdown_headers

app = typer.Typer(
    name="txmd",
    help="A terminal-based markdown viewer with pipeline support",
    add_completion=False,
)


class MarkdownViewerApp(App[None]):
    """A Textual app to display markdown content.

    This class provides a terminal user interface for viewing Markdown files
    with vim-style navigation keybindings. It extends Textual's App class to
    create a scrollable container with a Markdown widget.

    Attributes:
        content (str): The markdown content to display in the viewer.

    Example:
        >>> app = MarkdownViewerApp("# Hello\\nThis is markdown content")
        >>> app.run()
    """

    CSS = """
    #toc-tree {
        display: none;
        layer: overlay;
        offset: 0 0;
        width: 40;
        height: 100%;
        padding: 1;
        background: $panel;
        border-right: solid $primary;
    }

    #toc-tree.visible {
        display: block;
    }

    #content {
        width: 100%;
        height: 100%;
        background: $surface;
        margin-left: 0;
    }

    #content.toc-visible {
        margin-left: 40;
    }

    Markdown {
        width: 100%;
        height: auto;
        padding: 1 2;
        background: $surface;
        color: $text;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("j", "scroll_down", "Scroll Down"),
        Binding("k", "scroll_up", "Scroll Up"),
        Binding("up", "scroll_up", "Up"),
        Binding("down", "scroll_down", "Down"),
        Binding("pageup", "page_up", "Page Up"),
        Binding("pagedown", "page_down", "Page Down"),
        Binding("home", "scroll_home", "Top"),
        Binding("end", "scroll_end", "Bottom"),
        Binding("ctrl+c", "quit", "Quit"),
        Binding("space", "page_down", "Page Down"),
        Binding("b", "page_up", "Page Up"),
        Binding("t", "toggle_toc", "Toggle TOC"),
    ]

    def __init__(self, content: str, filename: Optional[str] = None):
        """Initialize the MarkdownViewerApp.

        Args:
            content (str): The markdown content to display in the viewer.
            filename (Optional[str]): The name of the file being viewed.
        """
        super().__init__()
        self.content = content
        self.filename = filename or "(stdin)"
        self.toc_visible = False
        self.header_positions: Dict[str, int] = {}
        self.toc_nodes: Dict[str, HeaderNode] = {}

    def compose(self) -> ComposeResult:
        """Create child widgets for the app.

        This method is called by Textual to build the widget hierarchy.
        It creates a ScrollableContainer with a Markdown widget, and
        optionally overlays a TOC tree.

        Returns:
            ComposeResult: The composed widgets for the application.
        """
        # Main content - scrollable container (yield first for focus)
        with ScrollableContainer(id="content"):
            yield Markdown(self.content)

        # TOC tree (hidden by default, will overlay when visible)
        tree = Tree(self.filename, id="toc-tree")
        tree.can_focus = False  # Don't steal focus when hidden
        yield tree

    def action_quit(self) -> None:
        """Quit the application.

        This action is bound to 'q' and Ctrl+C keys by default.
        """
        self.exit()

    def action_scroll_down(self) -> None:
        """Scroll down by one line.

        This action is bound to 'j' and down arrow keys.
        Scrolling is performed without animation for immediate response.
        """
        self.query_one(ScrollableContainer).scroll_down(animate=False)

    def action_scroll_up(self) -> None:
        """Scroll up by one line.

        This action is bound to 'k' and up arrow keys.
        Scrolling is performed without animation for immediate response.
        """
        self.query_one(ScrollableContainer).scroll_up(animate=False)

    def action_page_down(self) -> None:
        """Scroll down by one page (viewport height).

        This action is bound to PageDown, Space, and 'b' keys.
        If the TOC tree is focused, Space navigates to the selected section.
        Otherwise, scrolling is performed without animation for immediate
        response.
        """
        # Check if TOC tree is focused - if so, navigate to section
        tree = self.query_one("#toc-tree", Tree)
        if tree.has_focus and tree.cursor_node is not None:
            if tree.cursor_node.data:
                node_key = tree.cursor_node.data
                if node_key in self.toc_nodes:
                    header_node = self.toc_nodes[node_key]
                    self._scroll_to_line(
                        header_node.line_number, position_at_top=True
                    )
                    return

        # Normal page down behavior
        self.query_one(ScrollableContainer).scroll_page_down(animate=False)

    def action_page_up(self) -> None:
        """Scroll up by one page (viewport height).

        This action is bound to PageUp key.
        Scrolling is performed without animation for immediate response.
        """
        self.query_one(ScrollableContainer).scroll_page_up(animate=False)

    def action_scroll_home(self) -> None:
        """Scroll to the top of the document.

        This action is bound to the Home key.
        Scrolling is performed without animation for immediate response.
        """
        self.query_one(ScrollableContainer).scroll_home(animate=False)

    def action_scroll_end(self) -> None:
        """Scroll to the bottom of the document.

        This action is bound to the End key.
        Scrolling is performed without animation for immediate response.
        """
        self.query_one(ScrollableContainer).scroll_end(animate=False)

    def action_toggle_toc(self) -> None:
        """Toggle the visibility of the Table of Contents tree.

        This action is bound to the 't' key. It shows or hides the TOC
        sidebar by adding/removing the 'visible' CSS class and shifts
        the content to the right when TOC is visible.
        """
        toc_tree = self.query_one("#toc-tree", Tree)
        content = self.query_one("#content", ScrollableContainer)
        self.toc_visible = not self.toc_visible

        if self.toc_visible:
            toc_tree.add_class("visible")
            content.add_class("toc-visible")
            toc_tree.can_focus = True  # Allow focus when visible
            toc_tree.focus()
        else:
            toc_tree.remove_class("visible")
            content.remove_class("toc-visible")
            toc_tree.can_focus = False  # Prevent focus when hidden
            # Return focus to the scrollable container
            content.focus()

    async def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """Handle tree node selection to navigate to headers.

        When a user selects a TOC entry, this method scrolls the markdown
        view to the corresponding header.

        Args:
            event: The tree node selection event containing the selected node
        """
        if event.node.data is None:
            return

        # Get the header node from our mapping
        node_key = event.node.data
        if node_key not in self.toc_nodes:
            return

        header_node = self.toc_nodes[node_key]
        self._scroll_to_line(header_node.line_number)

    async def on_key(self, event: events.Key) -> None:
        """Handle key events for enhanced tree navigation.

        Args:
            event: The key event
        """
        # Check if the tree is focused
        tree = self.query_one("#toc-tree", Tree)
        if not tree.has_focus:
            return

        # Handle Enter key - toggle expansion
        if event.key == "enter":
            if tree.cursor_node is not None:
                # Toggle expansion if the node has children
                if tree.cursor_node.allow_expand:
                    tree.cursor_node.toggle()
                    event.prevent_default()
                    event.stop()

    def _scroll_to_line(
        self, line_number: int, position_at_top: bool = False
    ) -> None:
        """Scroll the markdown view to a specific line number.

        Args:
            line_number: The line number to scroll to (1-indexed)
            position_at_top: If True, position the line near the top of the
                viewport (2 rows down). If False, use proportional scrolling.
        """
        lines = self.content.split("\n")
        total_lines = len(lines)

        if total_lines == 0 or line_number < 1:
            return

        # Get the scrollable container and markdown widget
        container = self.query_one(ScrollableContainer)
        markdown_widget = self.query_one(Markdown)

        # Get the virtual (rendered) size of the markdown widget
        virtual_size = markdown_widget.virtual_size

        if virtual_size.height == 0:
            return

        # Calculate scroll position based on line proportion
        # This is an approximation since markdown lines don't map 1:1
        scroll_proportion = (line_number - 1) / max(total_lines - 1, 1)

        # Calculate target Y position in the virtual space
        target_y = int(virtual_size.height * scroll_proportion)

        if position_at_top:
            # Position ~2 rows below the top for visibility
            # Subtract a small offset so the header is visible below top edge
            target_y = max(0, target_y - 2)

        # Scroll to the calculated position with faster animation
        container.scroll_to(y=target_y, animate=True, speed=100)

    async def on_mount(self) -> None:
        """Handle app mount event.

        This lifecycle method is called when the app is first mounted.
        It sets the application title, populates the TOC, and sets
        initial focus.
        """
        self.title = "Markdown Viewer"
        self._populate_toc()
        # Ensure content container has focus for scrolling
        self.query_one("#content", ScrollableContainer).focus()

    def _populate_toc(self) -> None:
        """Parse markdown headers and populate the TOC tree widget."""
        # Parse headers from content
        headers = parse_markdown_headers(self.content)

        if not headers:
            # No headers found, nothing to populate
            return

        # Build hierarchical tree structure
        root_nodes = build_toc_tree(headers)

        # Get the tree widget
        tree = self.query_one("#toc-tree", Tree)
        tree.clear()

        # Populate the tree widget
        def add_nodes_to_tree(
            parent: TreeNode,
            nodes: list[HeaderNode],
            node_map: Dict[str, HeaderNode],
        ) -> None:
            """Recursively add nodes to the tree widget."""
            for node in nodes:
                # Create a unique key for this node
                node_key = f"{node.text}:{node.line_number}"
                node_map[node_key] = node

                # Add to tree
                tree_node = parent.add(node.text, data=node_key)

                # Add children recursively
                if node.children:
                    add_nodes_to_tree(tree_node, node.children, node_map)
                else:
                    # Leaf nodes should not show expand/collapse controls
                    tree_node.allow_expand = False

        # Add all root nodes
        add_nodes_to_tree(tree.root, root_nodes, self.toc_nodes)


def read_stdin() -> str:
    """Read content from stdin if available.

    This function checks if stdin is being piped (not a TTY) and reads
    the piped content. After reading, it attempts to reopen /dev/tty
    to restore terminal control, which is necessary for the Textual TUI
    to function properly.

    Returns:
        str: The content read from stdin, or empty string if stdin is a TTY.

    Note:
        This function modifies sys.stdin to reopen the terminal device,
        allowing the TUI to accept keyboard input after reading piped content.
    """
    if not sys.stdin.isatty():
        content = sys.stdin.read()
        # Reopen stdin as terminal
        try:
            sys.stdin.close()
            sys.__stdin__ = sys.stdin = open("/dev/tty")
        except Exception:
            # If we can't reopen the terminal, continue anyway
            pass
        return content
    return ""


def version_callback(value: bool) -> None:
    """Display version information and exit.

    Args:
        value (bool): True if --version flag was provided.

    Raises:
        typer.Exit: Always exits after displaying version.
    """
    if value:
        typer.echo(f"txmd version {__version__}")
        raise typer.Exit()


@app.command()
def main(
    file: Optional[Path] = typer.Argument(
        None,
        help="Markdown file to display. If not provided, reads from stdin.",
        exists=True,
        dir_okay=False,
        readable=True,
    ),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """Display markdown content in the terminal.

    This is the main entry point for the txmd CLI application. It accepts
    either a file path or piped content from stdin and displays it in a
    terminal-based markdown viewer with vim-style navigation.

    Args:
        file (Optional[Path]): Path to a markdown file to display.
            If None, the application will attempt to read from stdin.

    Raises:
        SystemExit: Exits with code 1 if no input is provided or if
            an error occurs.

    Examples:
        View a markdown file:
            $ txmd README.md

        Pipe content to txmd:
            $ echo "# Hello World" | txmd
            $ cat document.md | txmd
            $ curl https://example.com/doc.md | txmd
    """
    console = Console()

    try:
        if file:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
            filename = file.name
        else:
            stdin_content = read_stdin()
            if not stdin_content:
                console.print(
                    "[red]Error:[/] No input provided. "
                    "Please provide a file or pipe content to txmd."
                )
                sys.exit(1)
            content = stdin_content
            filename = None

        app = MarkdownViewerApp(content, filename)
        app.run()

    except Exception as e:
        console.print(f"[red]Error:[/] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    app()
