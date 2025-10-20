"""Tests for txmd CLI functionality."""

from unittest.mock import Mock, patch

import pytest
import typer
from typer.testing import CliRunner

from txmd import __version__
from txmd.cli import MarkdownViewerApp, app, read_stdin, version_callback


class TestMarkdownViewerApp:
    """Tests for the MarkdownViewerApp class."""

    def test_app_initialization(self):
        """Test that the app initializes with content."""
        content = "# Test Heading\n\nThis is a test."
        app = MarkdownViewerApp(content)
        assert app.content == content

    def test_app_title_on_mount(self):
        """Test that the app sets its title on mount."""
        app = MarkdownViewerApp("# Test")
        assert hasattr(app, "title")

    def test_compose_method_exists(self):
        """Test that compose method exists and is callable."""
        content = "# Test Content"
        app = MarkdownViewerApp(content)

        # Verify compose method exists
        assert hasattr(app, "compose")
        assert callable(app.compose)

    def test_bindings_defined(self):
        """Test that key bindings are properly defined."""
        app = MarkdownViewerApp("test")

        # Check that bindings exist
        assert hasattr(app, "BINDINGS")
        assert len(app.BINDINGS) > 0

        # Check for key bindings
        binding_keys = [b.key for b in app.BINDINGS]
        assert "q" in binding_keys
        assert "j" in binding_keys
        assert "k" in binding_keys
        assert "space" in binding_keys
        assert "t" in binding_keys  # TOC toggle binding

    def test_css_defined(self):
        """Test that CSS is defined."""
        app = MarkdownViewerApp("test")
        assert hasattr(app, "CSS")
        assert isinstance(app.CSS, str)
        assert len(app.CSS) > 0

    def test_toc_state_initialization(self):
        """Test that TOC state is properly initialized."""
        content = "# Test Content"
        app = MarkdownViewerApp(content)

        assert hasattr(app, "toc_visible")
        assert app.toc_visible is False  # Hidden by default
        assert hasattr(app, "header_positions")
        assert isinstance(app.header_positions, dict)
        assert hasattr(app, "toc_nodes")
        assert isinstance(app.toc_nodes, dict)

    def test_toggle_toc_action_exists(self):
        """Test that toggle_toc action method exists."""
        app = MarkdownViewerApp("# Test")

        assert hasattr(app, "action_toggle_toc")
        assert callable(app.action_toggle_toc)

    def test_populate_toc_method_exists(self):
        """Test that _populate_toc helper method exists."""
        app = MarkdownViewerApp("# Test")

        assert hasattr(app, "_populate_toc")
        assert callable(app._populate_toc)

    def test_scroll_to_line_method_exists(self):
        """Test that _scroll_to_line helper method exists."""
        app = MarkdownViewerApp("# Test")

        assert hasattr(app, "_scroll_to_line")
        assert callable(app._scroll_to_line)

    def test_tree_node_selection_handler_exists(self):
        """Test that tree node selection handler exists."""
        app = MarkdownViewerApp("# Test")

        assert hasattr(app, "on_tree_node_selected")
        assert callable(app.on_tree_node_selected)


class TestReadStdin:
    """Tests for the read_stdin function."""

    @patch("sys.stdin")
    def test_read_stdin_with_piped_input(self, mock_stdin):
        """Test reading from stdin when input is piped."""
        mock_stdin.isatty.return_value = False
        mock_stdin.read.return_value = "# Piped Content\n\nTest"

        result = read_stdin()

        assert result == "# Piped Content\n\nTest"
        mock_stdin.read.assert_called_once()

    @patch("sys.stdin")
    def test_read_stdin_with_terminal(self, mock_stdin):
        """Test reading from stdin when running in terminal."""
        mock_stdin.isatty.return_value = True

        result = read_stdin()

        assert result == ""
        mock_stdin.read.assert_not_called()

    @patch("sys.stdin")
    @patch("builtins.open")
    def test_read_stdin_reopens_terminal(self, mock_open_fn, mock_stdin):
        """Test that stdin is reopened to /dev/tty after reading."""
        mock_stdin.isatty.return_value = False
        mock_stdin.read.return_value = "content"
        mock_tty = Mock()
        mock_open_fn.return_value = mock_tty

        result = read_stdin()

        # Should attempt to reopen /dev/tty
        assert result == "content"

    @patch("sys.stdin")
    @patch("builtins.open", side_effect=Exception("No TTY"))
    def test_read_stdin_handles_tty_reopen_failure(
        self, mock_open_fn, mock_stdin
    ):
        """Test that function handles TTY reopen failure gracefully."""
        mock_stdin.isatty.return_value = False
        mock_stdin.read.return_value = "content"

        # Should not raise exception even if TTY reopen fails
        result = read_stdin()
        assert result == "content"


class TestMainCommand:
    """Tests for the main command function."""

    @patch("txmd.cli.MarkdownViewerApp")
    def test_main_with_file(self, mock_app_class, tmp_path):
        """Test main command with a file argument."""
        # Create a temporary markdown file
        test_file = tmp_path / "test.md"
        test_content = "# Test File\n\nContent here"
        test_file.write_text(test_content)

        mock_app_instance = Mock()
        mock_app_class.return_value = mock_app_instance

        from txmd.cli import main

        # Call main with the file
        with patch("sys.exit"):
            main(test_file)

        # Verify app was created with file content and filename
        mock_app_class.assert_called_once_with(test_content, "test.md")
        mock_app_instance.run.assert_called_once()

    @patch("txmd.cli.MarkdownViewerApp")
    @patch("txmd.cli.read_stdin")
    def test_main_with_stdin(self, mock_read_stdin, mock_app_class):
        """Test main command with stdin input."""
        stdin_content = "# Piped Markdown\n\nFrom stdin"
        mock_read_stdin.return_value = stdin_content

        mock_app_instance = Mock()
        mock_app_class.return_value = mock_app_instance

        from txmd.cli import main

        with patch("sys.exit"):
            main(None)

        # Verify app was created with stdin content and None filename
        mock_app_class.assert_called_once_with(stdin_content, None)
        mock_app_instance.run.assert_called_once()

    @patch("txmd.cli.read_stdin")
    @patch("rich.console.Console.print")
    def test_main_no_input_exits(self, mock_print, mock_read_stdin):
        """Test that main exits when no input is provided."""
        mock_read_stdin.return_value = ""

        from txmd.cli import main

        with pytest.raises(SystemExit) as exc_info:
            main(None)

        assert exc_info.value.code == 1
        mock_print.assert_called()

    @patch("txmd.cli.MarkdownViewerApp")
    def test_main_handles_exceptions(self, mock_app_class, tmp_path):
        """Test that main handles exceptions gracefully."""
        test_file = tmp_path / "test.md"
        test_file.write_text("content")

        mock_app_class.side_effect = Exception("Test error")

        from txmd.cli import main

        with pytest.raises(SystemExit) as exc_info:
            main(test_file)

        assert exc_info.value.code == 1


class TestVersionOption:
    """Tests for version option functionality."""

    def test_version_callback_with_true(self):
        """Test that version_callback displays version and exits."""
        with pytest.raises(typer.Exit):
            version_callback(True)

    def test_version_callback_with_false(self):
        """Test that version_callback does nothing when False."""
        # Should not raise an exception
        version_callback(False)

    def test_version_flag_long(self, tmp_path):
        """Test --version flag displays version and exits."""
        runner = CliRunner()
        result = runner.invoke(app, ["--version"])

        assert result.exit_code == 0
        assert "txmd version" in result.output
        assert __version__ in result.output

    def test_version_flag_short(self, tmp_path):
        """Test -v flag displays version and exits."""
        runner = CliRunner()
        result = runner.invoke(app, ["-v"])

        assert result.exit_code == 0
        assert "txmd version" in result.output
        assert __version__ in result.output

    def test_version_format(self):
        """Test that __version__ is a valid string."""
        assert isinstance(__version__, str)
        assert len(__version__) > 0
        assert __version__ != "unknown"


class TestIntegration:
    """Integration tests."""

    def test_app_can_be_instantiated_and_composed(self):
        """Test that the app can be fully instantiated."""
        content = """
# Main Title

This is a paragraph with **bold** and *italic* text.

## Subsection

- List item 1
- List item 2
- List item 3

```python
def hello():
    print("Hello, world!")
```
        """

        app = MarkdownViewerApp(content)

        # Verify content is stored
        assert app.content == content

        # Verify app has required attributes
        assert hasattr(app, "CSS")
        assert hasattr(app, "BINDINGS")
        assert hasattr(app, "compose")

        # Verify bindings are callable
        assert callable(app.action_quit)
        assert callable(app.action_scroll_down)
        assert callable(app.action_scroll_up)
        assert callable(app.action_page_down)
        assert callable(app.action_page_up)
