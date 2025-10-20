# txmd/cli.py
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import ScrollableContainer
from textual.widgets import Markdown

from txmd import __version__

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
    ]

    def __init__(self, content: str):
        """Initialize the MarkdownViewerApp.

        Args:
            content (str): The markdown content to display in the viewer.
        """
        super().__init__()
        self.content = content

    def compose(self) -> ComposeResult:
        """Create child widgets for the app.

        This method is called by Textual to build the widget hierarchy.
        It creates a ScrollableContainer with a Markdown widget inside.

        Returns:
            ComposeResult: The composed widgets for the application.
        """
        with ScrollableContainer():
            yield Markdown(self.content)

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
        Scrolling is performed without animation for immediate response.
        """
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

    async def on_mount(self) -> None:
        """Handle app mount event.

        This lifecycle method is called when the app is first mounted.
        It sets the application title shown in the terminal title bar.
        """
        self.title = "Markdown Viewer"


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
        else:
            stdin_content = read_stdin()
            if not stdin_content:
                console.print(
                    "[red]Error:[/] No input provided. "
                    "Please provide a file or pipe content to txmd."
                )
                sys.exit(1)
            content = stdin_content

        app = MarkdownViewerApp(content)
        app.run()

    except Exception as e:
        console.print(f"[red]Error:[/] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    app()
