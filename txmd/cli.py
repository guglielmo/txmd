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

app = typer.Typer(
    name="txmd",
    help="A terminal-based markdown viewer with pipeline support",
    add_completion=False,
)


class MarkdownViewerApp(App[None]):
    """A Textual app to display markdown content."""

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
        super().__init__()
        self.content = content

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        with ScrollableContainer():
            yield Markdown(self.content)

    def action_quit(self) -> None:
        """Quit the application."""
        self.exit()

    def action_scroll_down(self) -> None:
        """Scroll down."""
        self.query_one(ScrollableContainer).scroll_down(animate=False)

    def action_scroll_up(self) -> None:
        """Scroll up."""
        self.query_one(ScrollableContainer).scroll_up(animate=False)

    def action_page_down(self) -> None:
        """Scroll one page down."""
        self.query_one(ScrollableContainer).scroll_page_down(animate=False)

    def action_page_up(self) -> None:
        """Scroll one page up."""
        self.query_one(ScrollableContainer).scroll_page_up(animate=False)

    def action_scroll_home(self) -> None:
        """Scroll to the top."""
        self.query_one(ScrollableContainer).scroll_home(animate=False)

    def action_scroll_end(self) -> None:
        """Scroll to the bottom."""
        self.query_one(ScrollableContainer).scroll_end(animate=False)

    async def on_mount(self) -> None:
        """Handle app mount event."""
        self.title = "Markdown Viewer"


def read_stdin() -> str:
    """Read content from stdin if available."""
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


@app.command()
def main(
    file: Optional[Path] = typer.Argument(
        None,
        help="Markdown file to display. If not provided, reads from stdin.",
        exists=True,
        dir_okay=False,
        readable=True,
    )
) -> None:
    """
    Display markdown content in the terminal.

    If no file is provided, reads from stdin.
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
