"""Table of Contents parsing and tree building for txmd."""

import re
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class HeaderNode:
    """Represents a header node in the TOC tree.

    Attributes:
        level (int): Header level (1-6 for # through ######)
        text (str): The header text content
        line_number (int): Line number in the original markdown content
        children (List[HeaderNode]): Child headers nested under this header
    """

    level: int
    text: str
    line_number: int
    children: List["HeaderNode"] = field(default_factory=list)


def parse_markdown_headers(content: str) -> List[Tuple[int, str, int]]:
    """Parse markdown content and extract all headers.

    This function finds ATX-style headers (# through ######) in markdown
    content and returns their information. It skips headers inside code blocks.

    Args:
        content (str): The markdown content to parse

    Returns:
        List[Tuple[int, str, int]]: List of tuples containing:
            - level: Header level (1-6)
            - text: Header text content
            - line_number: Line number in content (1-indexed)

    Example:
        >>> content = "# Title\\n## Subtitle"
        >>> parse_markdown_headers(content)
        [(1, 'Title', 1), (2, 'Subtitle', 2)]
    """
    headers = []
    lines = content.split("\n")

    # Regex for ATX-style headers: # Header
    # Matches 1-6 # symbols followed by text
    header_pattern = re.compile(r"^(#{1,6})\s+(.+?)(?:\s*#*)?$")

    # Regex for code fence (``` or ~~~)
    code_fence_pattern = re.compile(r"^```|^~~~")

    in_code_block = False

    for line_num, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Check for code fence toggle
        if code_fence_pattern.match(stripped):
            in_code_block = not in_code_block
            continue

        # Skip lines inside code blocks
        if in_code_block:
            continue

        # Skip indented code blocks (4 spaces or tab)
        if line.startswith("    ") or line.startswith("\t"):
            continue

        # Check for header
        match = header_pattern.match(stripped)
        if match:
            level = len(match.group(1))  # Count the # symbols
            text = match.group(2).strip()
            headers.append((level, text, line_num))

    return headers


def build_toc_tree(headers: List[Tuple[int, str, int]]) -> List[HeaderNode]:
    """Build a hierarchical tree structure from flat header list.

    This function takes a flat list of headers and constructs a tree
    structure based on header levels, suitable for display in a Tree widget.

    Args:
        headers (List[Tuple[int, str, int]]): List of header tuples from
            parse_markdown_headers()

    Returns:
        List[HeaderNode]: List of root-level HeaderNode objects, each
            potentially containing children

    Example:
        >>> headers = [(1, 'Title', 1), (2, 'Subtitle', 2), (2, 'Another', 3)]
        >>> tree = build_toc_tree(headers)
        >>> len(tree)
        1
        >>> len(tree[0].children)
        2
    """
    if not headers:
        return []

    root_nodes = []
    stack = []  # Stack to track current path in tree

    for level, text, line_num in headers:
        node = HeaderNode(level, text, line_num)

        # Pop stack until we find a valid parent (level < current level)
        while stack and stack[-1].level >= level:
            stack.pop()

        if stack:
            # Add as child to the parent on top of stack
            stack[-1].children.append(node)
        else:
            # This is a root-level node
            root_nodes.append(node)

        # Push current node onto stack
        stack.append(node)

    return root_nodes
