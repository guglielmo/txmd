"""UI interaction tests for the Textual markdown viewer app."""

from textual.containers import ScrollableContainer
from textual.widgets import Tree

from txmd.cli import MarkdownViewerApp


class TestTOCToggle:
    """Tests for Table of Contents toggle functionality."""

    async def test_toc_initially_hidden(self):
        """Test that TOC is hidden by default."""
        content = "# Title\n## Section 1\n## Section 2"
        app = MarkdownViewerApp(content, "test.md")

        async with app.run_test() as pilot:
            await pilot.pause()
            assert app.toc_visible is False

            # Check TOC tree doesn't have visible class
            tree = app.query_one("#toc-tree", Tree)
            assert "visible" not in tree.classes

    async def test_toc_toggle_shows_and_hides(self):
        """Test that pressing 't' toggles TOC visibility."""
        content = "# Title\n## Section 1\n## Section 2"
        app = MarkdownViewerApp(content, "test.md")

        async with app.run_test() as pilot:
            await pilot.pause()

            # Press 't' to show TOC
            await pilot.press("t")
            await pilot.pause()
            assert app.toc_visible is True

            tree = app.query_one("#toc-tree", Tree)
            assert "visible" in tree.classes

            # Press 't' again to hide TOC
            await pilot.press("t")
            await pilot.pause()
            assert app.toc_visible is False
            assert "visible" not in tree.classes

    async def test_toc_shows_filename_as_root(self):
        """Test that TOC uses filename as root label."""
        content = "# Title"
        filename = "README.md"
        app = MarkdownViewerApp(content, filename)

        async with app.run_test() as pilot:
            await pilot.pause()

            tree = app.query_one("#toc-tree", Tree)
            assert str(tree.root.label) == filename

    async def test_toc_shows_stdin_for_piped_content(self):
        """Test that TOC shows (stdin) when no filename provided."""
        content = "# Title"
        app = MarkdownViewerApp(content)

        async with app.run_test() as pilot:
            await pilot.pause()

            tree = app.query_one("#toc-tree", Tree)
            assert str(tree.root.label) == "(stdin)"

    async def test_toc_focus_management(self):
        """Test that TOC can only be focused when visible."""
        content = "# Title\n## Section"
        app = MarkdownViewerApp(content)

        async with app.run_test() as pilot:
            await pilot.pause()

            tree = app.query_one("#toc-tree", Tree)

            # Initially hidden, can't focus
            assert tree.can_focus is False
            assert not tree.has_focus

            # Show TOC
            await pilot.press("t")
            await pilot.pause()

            # Now can focus and should have focus
            assert tree.can_focus is True
            assert tree.has_focus

            # Hide TOC
            await pilot.press("t")
            await pilot.pause()

            # Can't focus again
            assert tree.can_focus is False


class TestScrollActions:
    """Tests for scrolling actions.

    Note: These tests verify that scroll keybindings execute without errors.
    Exact scroll position testing is challenging in test mode due to
    rendering constraints.
    """

    async def test_scroll_keybindings_work(self):
        """Test that all scroll keybindings execute without errors."""
        content = "# Title\n\n" + "\n\n".join(
            [f"## Section {i}\n\nContent for section {i}." for i in range(50)]
        )
        app = MarkdownViewerApp(content)

        async with app.run_test(size=(80, 30)) as pilot:
            await pilot.pause()

            # Test all scroll keybindings - they should not crash
            await pilot.press("j")  # Scroll down
            await pilot.pause()

            await pilot.press("k")  # Scroll up
            await pilot.pause()

            await pilot.press("down")  # Scroll down (arrow)
            await pilot.pause()

            await pilot.press("up")  # Scroll up (arrow)
            await pilot.pause()

            await pilot.press("space")  # Page down
            await pilot.pause()

            await pilot.press("b")  # Page up
            await pilot.pause()

            await pilot.press("pagedown")  # Page down (key)
            await pilot.pause()

            await pilot.press("pageup")  # Page up (key)
            await pilot.pause()

            await pilot.press("home")  # Top
            await pilot.pause()

            await pilot.press("end")  # Bottom
            await pilot.pause()

            # If we get here, all keybindings work
            assert True

    async def test_scroll_end(self):
        """Test that end key scrolls to bottom."""
        content = "# Title\n" + "\n".join([f"Line {i}" for i in range(100)])
        app = MarkdownViewerApp(content)

        async with app.run_test() as pilot:
            await pilot.pause()

            container = app.query_one("#content", ScrollableContainer)

            # Press end to go to bottom
            await pilot.press("end")
            await pilot.pause()

            # Should be at or near the maximum scroll position
            assert container.scroll_y >= container.max_scroll_y - 1


class TestTOCNavigation:
    """Tests for TOC navigation and section jumping."""

    async def test_toc_parses_headers(self):
        """Test that TOC correctly parses markdown headers."""
        content = """# Main Title
## Section 1
### Subsection 1.1
## Section 2"""
        app = MarkdownViewerApp(content, "test.md")

        async with app.run_test() as pilot:
            await pilot.pause()

            # Should have parsed headers into toc_nodes
            assert len(app.toc_nodes) == 4
            assert any("Main Title" in key for key in app.toc_nodes.keys())
            assert any("Section 1" in key for key in app.toc_nodes.keys())
            assert any("Subsection 1.1" in key for key in app.toc_nodes.keys())
            assert any("Section 2" in key for key in app.toc_nodes.keys())

    async def test_toc_hierarchical_structure(self):
        """Test that TOC builds hierarchical tree structure."""
        content = """# Title
## Section 1
### Subsection 1.1
## Section 2"""
        app = MarkdownViewerApp(content)

        async with app.run_test() as pilot:
            await pilot.pause()

            tree = app.query_one("#toc-tree", Tree)

            # Root should have 1 child (Title)
            assert len(tree.root.children) == 1
            title_node = tree.root.children[0]

            # Title should have 2 children (Section 1, Section 2)
            assert len(title_node.children) == 2

            # Section 1 should have 1 child (Subsection 1.1)
            section1_node = title_node.children[0]
            assert len(section1_node.children) == 1

    async def test_toc_leaf_nodes_cannot_expand(self):
        """Test that leaf nodes have allow_expand=False."""
        content = """# Title
## Section 1
## Section 2"""
        app = MarkdownViewerApp(content)

        async with app.run_test() as pilot:
            await pilot.pause()

            tree = app.query_one("#toc-tree", Tree)
            title_node = tree.root.children[0]

            # Section 1 and Section 2 are leaf nodes
            section1_node = title_node.children[0]
            section2_node = title_node.children[1]

            assert section1_node.allow_expand is False
            assert section2_node.allow_expand is False

    async def test_toc_branch_nodes_can_expand(self):
        """Test that branch nodes can be expanded."""
        content = """# Title
## Section 1
### Subsection 1.1"""
        app = MarkdownViewerApp(content)

        async with app.run_test() as pilot:
            await pilot.pause()

            tree = app.query_one("#toc-tree", Tree)
            title_node = tree.root.children[0]
            section1_node = title_node.children[0]

            # Section 1 has children, so it should be expandable
            assert section1_node.allow_expand is True

    async def test_toc_navigation_with_space(self):
        """Test that pressing space in TOC triggers navigation."""
        content = """# Title

""" + "\n".join([f"Line {i}" for i in range(50)]) + """

## Section Below

Content here."""
        app = MarkdownViewerApp(content)

        async with app.run_test(size=(80, 40)) as pilot:
            await pilot.pause()

            # Show TOC
            await pilot.press("t")
            await pilot.pause()

            # Navigate to second section
            await pilot.press("down")
            await pilot.pause()

            # Jump to section with space (should not crash)
            await pilot.press("space")
            await pilot.pause()

            # Test passes if no exception was raised
            assert True

    async def test_toc_enter_key_handling(self):
        """Test that pressing enter in TOC is handled."""
        content = """# Title
## Section 1
### Subsection 1.1"""
        app = MarkdownViewerApp(content)

        async with app.run_test() as pilot:
            await pilot.pause()

            # Show TOC
            await pilot.press("t")
            await pilot.pause()

            # Press enter (should toggle expansion without crashing)
            await pilot.press("enter")
            await pilot.pause()

            # Test passes if no exception was raised
            assert True


class TestTOCCodeBlockFiltering:
    """Tests for filtering out headers in code blocks."""

    async def test_toc_ignores_headers_in_fenced_code(self):
        """Test that headers in fenced code blocks are ignored."""
        content = """# Real Header

```python
# Not a header (Python comment)
def foo():
    pass
```

## Another Real Header"""
        app = MarkdownViewerApp(content)

        async with app.run_test() as pilot:
            await pilot.pause()

            # Should only have 2 headers, not 3
            assert len(app.toc_nodes) == 2
            toc_keys = app.toc_nodes.keys()
            assert any("Real Header" in key for key in toc_keys)
            assert any("Another Real Header" in key for key in toc_keys)
            assert not any("Not a header" in key for key in toc_keys)

    async def test_toc_ignores_headers_in_indented_code(self):
        """Test that headers in indented code blocks are ignored."""
        content = """# Real Header

    # This is indented code
    # Not a header

## Another Real Header"""
        app = MarkdownViewerApp(content)

        async with app.run_test() as pilot:
            await pilot.pause()

            # Should only have 2 headers
            assert len(app.toc_nodes) == 2
            toc_keys = app.toc_nodes.keys()
            assert any("Real Header" in key for key in toc_keys)
            assert any("Another Real Header" in key for key in toc_keys)


class TestContentShifting:
    """Tests for content shifting when TOC is visible."""

    async def test_content_shifts_when_toc_visible(self):
        """Test that content adds toc-visible class when TOC is shown."""
        content = "# Title\n## Section"
        app = MarkdownViewerApp(content)

        async with app.run_test() as pilot:
            await pilot.pause()

            container = app.query_one("#content", ScrollableContainer)

            # Initially no toc-visible class
            assert "toc-visible" not in container.classes

            # Show TOC
            await pilot.press("t")
            await pilot.pause()

            # Should have toc-visible class
            assert "toc-visible" in container.classes

            # Hide TOC
            await pilot.press("t")
            await pilot.pause()

            # Should remove toc-visible class
            assert "toc-visible" not in container.classes


class TestQuitAction:
    """Tests for quit functionality."""

    async def test_quit_with_q(self):
        """Test that 'q' key quits the app."""
        content = "# Title"
        app = MarkdownViewerApp(content)

        async with app.run_test() as pilot:
            await pilot.pause()

            # App should be running
            assert app.is_running

            # Press 'q' to quit
            await pilot.press("q")
            await pilot.pause()

            # App should have exited
            assert not app.is_running

    async def test_quit_with_ctrl_c(self):
        """Test that Ctrl+C quits the app."""
        content = "# Title"
        app = MarkdownViewerApp(content)

        async with app.run_test() as pilot:
            await pilot.pause()

            # App should be running
            assert app.is_running

            # Press Ctrl+C to quit
            await pilot.press("ctrl+c")
            await pilot.pause()

            # App should have exited
            assert not app.is_running
