"""Tests for the Table of Contents module."""

from txmd.toc import HeaderNode, build_toc_tree, parse_markdown_headers


class TestParseMarkdownHeaders:
    """Tests for parse_markdown_headers function."""

    def test_parse_single_header(self):
        """Test parsing a single header."""
        content = "# Main Title"
        headers = parse_markdown_headers(content)

        assert len(headers) == 1
        assert headers[0] == (1, "Main Title", 1)

    def test_parse_multiple_headers(self):
        """Test parsing multiple headers at different levels."""
        content = """# Title
## Subtitle
### Section
## Another Subtitle"""

        headers = parse_markdown_headers(content)

        assert len(headers) == 4
        assert headers[0] == (1, "Title", 1)
        assert headers[1] == (2, "Subtitle", 2)
        assert headers[2] == (3, "Section", 3)
        assert headers[3] == (2, "Another Subtitle", 4)

    def test_parse_headers_with_content(self):
        """Test parsing headers mixed with regular content."""
        content = """# Introduction

This is some content.

## Section 1

More content here.

### Subsection 1.1

Even more content.

## Section 2

Final content."""

        headers = parse_markdown_headers(content)

        assert len(headers) == 4
        assert headers[0] == (1, "Introduction", 1)
        assert headers[1] == (2, "Section 1", 5)
        assert headers[2] == (3, "Subsection 1.1", 9)
        assert headers[3] == (2, "Section 2", 13)

    def test_parse_headers_with_trailing_hashes(self):
        """Test parsing headers with trailing # symbols."""
        content = """# Title #
## Subtitle ##
### Section ###"""

        headers = parse_markdown_headers(content)

        assert len(headers) == 3
        assert headers[0] == (1, "Title", 1)
        assert headers[1] == (2, "Subtitle", 2)
        assert headers[2] == (3, "Section", 3)

    def test_parse_headers_all_levels(self):
        """Test parsing all six levels of headers."""
        content = """# Level 1
## Level 2
### Level 3
#### Level 4
##### Level 5
###### Level 6"""

        headers = parse_markdown_headers(content)

        assert len(headers) == 6
        for i, (level, text, line_num) in enumerate(headers, start=1):
            assert level == i
            assert text == f"Level {i}"
            assert line_num == i

    def test_parse_no_headers(self):
        """Test parsing content with no headers."""
        content = """This is just regular text.
No headers here.
Just paragraphs."""

        headers = parse_markdown_headers(content)

        assert len(headers) == 0
        assert headers == []

    def test_parse_empty_content(self):
        """Test parsing empty content."""
        content = ""
        headers = parse_markdown_headers(content)

        assert len(headers) == 0
        assert headers == []

    def test_parse_headers_with_special_characters(self):
        """Test parsing headers containing special characters."""
        content = """# Title with **bold** text
## Section with `code`
### Item with [link](url)"""

        headers = parse_markdown_headers(content)

        assert len(headers) == 3
        assert headers[0] == (1, "Title with **bold** text", 1)
        assert headers[1] == (2, "Section with `code`", 2)
        assert headers[2] == (3, "Item with [link](url)", 3)

    def test_parse_headers_with_extra_whitespace(self):
        """Test parsing headers with extra whitespace."""
        content = """#   Title with spaces
##     Subtitle   """

        headers = parse_markdown_headers(content)

        assert len(headers) == 2
        assert headers[0] == (1, "Title with spaces", 1)
        assert headers[1] == (2, "Subtitle", 2)

    def test_parse_ignores_inline_hashes(self):
        """Test that inline # symbols are not treated as headers."""
        content = """Regular text with # symbol

# Real Header

Text with #hashtag"""

        headers = parse_markdown_headers(content)

        assert len(headers) == 1
        assert headers[0] == (1, "Real Header", 3)

    def test_parse_headers_in_code_blocks_ignored(self):
        """Test that headers in code blocks are not parsed."""
        content = """# Real Header

```python
# Not a header (Python comment)
def foo():
    # Another comment
    pass
```

## Another Real Header"""

        headers = parse_markdown_headers(content)

        # Should only find the real headers, not the comments in code
        assert len(headers) == 2
        assert headers[0] == (1, "Real Header", 1)
        assert headers[1] == (2, "Another Real Header", 10)

    def test_parse_headers_in_indented_code_ignored(self):
        """Test that headers in indented code blocks are ignored."""
        content = """# Real Header

    # This is indented code (4 spaces)
    # Not a header

## Another Real Header"""

        headers = parse_markdown_headers(content)

        assert len(headers) == 2
        assert headers[0] == (1, "Real Header", 1)
        assert headers[1] == (2, "Another Real Header", 6)

    def test_parse_headers_with_tilde_code_fence(self):
        """Test that headers in ~~~ code fences are ignored."""
        content = """# Real Header

~~~
# Not a header
~~~

## Another Real Header"""

        headers = parse_markdown_headers(content)

        assert len(headers) == 2
        assert headers[0] == (1, "Real Header", 1)
        assert headers[1] == (2, "Another Real Header", 7)


class TestBuildTocTree:
    """Tests for build_toc_tree function."""

    def test_build_tree_single_node(self):
        """Test building tree with a single root node."""
        headers = [(1, "Title", 1)]
        tree = build_toc_tree(headers)

        assert len(tree) == 1
        assert tree[0].level == 1
        assert tree[0].text == "Title"
        assert tree[0].line_number == 1
        assert len(tree[0].children) == 0

    def test_build_tree_flat_structure(self):
        """Test building tree with all same-level headers."""
        headers = [
            (1, "Section 1", 1),
            (1, "Section 2", 2),
            (1, "Section 3", 3),
        ]
        tree = build_toc_tree(headers)

        assert len(tree) == 3
        assert all(node.level == 1 for node in tree)
        assert tree[0].text == "Section 1"
        assert tree[1].text == "Section 2"
        assert tree[2].text == "Section 3"
        assert all(len(node.children) == 0 for node in tree)

    def test_build_tree_nested_structure(self):
        """Test building tree with nested headers."""
        headers = [
            (1, "Title", 1),
            (2, "Subtitle 1", 2),
            (2, "Subtitle 2", 3),
        ]
        tree = build_toc_tree(headers)

        assert len(tree) == 1
        assert tree[0].text == "Title"
        assert len(tree[0].children) == 2
        assert tree[0].children[0].text == "Subtitle 1"
        assert tree[0].children[1].text == "Subtitle 2"

    def test_build_tree_deep_nesting(self):
        """Test building tree with deeply nested structure."""
        headers = [
            (1, "Level 1", 1),
            (2, "Level 2", 2),
            (3, "Level 3", 3),
            (4, "Level 4", 4),
        ]
        tree = build_toc_tree(headers)

        assert len(tree) == 1
        assert tree[0].text == "Level 1"
        assert len(tree[0].children) == 1
        assert tree[0].children[0].text == "Level 2"
        assert len(tree[0].children[0].children) == 1
        assert tree[0].children[0].children[0].text == "Level 3"
        assert len(tree[0].children[0].children[0].children) == 1
        assert tree[0].children[0].children[0].children[0].text == "Level 4"

    def test_build_tree_skipped_levels(self):
        """Test building tree when header levels are skipped."""
        headers = [
            (1, "Title", 1),
            (3, "Skipped to Level 3", 2),
            (2, "Back to Level 2", 3),
        ]
        tree = build_toc_tree(headers)

        assert len(tree) == 1
        assert tree[0].text == "Title"
        assert len(tree[0].children) == 2
        # Level 3 becomes child of level 1
        assert tree[0].children[0].text == "Skipped to Level 3"
        assert tree[0].children[0].level == 3
        # Level 2 also becomes child of level 1
        assert tree[0].children[1].text == "Back to Level 2"
        assert tree[0].children[1].level == 2

    def test_build_tree_complex_structure(self):
        """Test building tree with complex realistic structure."""
        headers = [
            (1, "Introduction", 1),
            (2, "Background", 2),
            (2, "Motivation", 3),
            (1, "Methods", 4),
            (2, "Approach 1", 5),
            (3, "Step 1", 6),
            (3, "Step 2", 7),
            (2, "Approach 2", 8),
            (1, "Conclusion", 9),
        ]
        tree = build_toc_tree(headers)

        # Should have 3 root nodes
        assert len(tree) == 3
        assert tree[0].text == "Introduction"
        assert tree[1].text == "Methods"
        assert tree[2].text == "Conclusion"

        # Introduction has 2 children
        assert len(tree[0].children) == 2
        assert tree[0].children[0].text == "Background"
        assert tree[0].children[1].text == "Motivation"

        # Methods has 2 children
        assert len(tree[1].children) == 2
        assert tree[1].children[0].text == "Approach 1"
        assert tree[1].children[1].text == "Approach 2"

        # Approach 1 has 2 children
        assert len(tree[1].children[0].children) == 2
        assert tree[1].children[0].children[0].text == "Step 1"
        assert tree[1].children[0].children[1].text == "Step 2"

    def test_build_tree_empty_headers(self):
        """Test building tree with empty header list."""
        headers = []
        tree = build_toc_tree(headers)

        assert len(tree) == 0
        assert tree == []

    def test_build_tree_preserves_line_numbers(self):
        """Test that line numbers are preserved in tree structure."""
        headers = [
            (1, "Title", 5),
            (2, "Section", 10),
            (3, "Subsection", 15),
        ]
        tree = build_toc_tree(headers)

        assert tree[0].line_number == 5
        assert tree[0].children[0].line_number == 10
        assert tree[0].children[0].children[0].line_number == 15


class TestHeaderNode:
    """Tests for HeaderNode dataclass."""

    def test_header_node_creation(self):
        """Test creating a HeaderNode instance."""
        node = HeaderNode(level=1, text="Title", line_number=1)

        assert node.level == 1
        assert node.text == "Title"
        assert node.line_number == 1
        assert isinstance(node.children, list)
        assert len(node.children) == 0

    def test_header_node_with_children(self):
        """Test HeaderNode with children."""
        child1 = HeaderNode(level=2, text="Child 1", line_number=2)
        child2 = HeaderNode(level=2, text="Child 2", line_number=3)
        parent = HeaderNode(
            level=1,
            text="Parent",
            line_number=1,
            children=[child1, child2],
        )

        assert len(parent.children) == 2
        assert parent.children[0] == child1
        assert parent.children[1] == child2

    def test_header_node_nested_children(self):
        """Test HeaderNode with nested children."""
        grandchild = HeaderNode(level=3, text="Grandchild", line_number=3)
        child = HeaderNode(
            level=2, text="Child", line_number=2, children=[grandchild]
        )
        parent = HeaderNode(
            level=1, text="Parent", line_number=1, children=[child]
        )

        assert len(parent.children) == 1
        assert len(parent.children[0].children) == 1
        assert parent.children[0].children[0].text == "Grandchild"
