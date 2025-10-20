# txmd Examples

This directory contains example markdown files demonstrating various features and use cases of txmd.

## Example Files

### 1. basic.md
Basic markdown features including:
- Headings (all levels)
- Text formatting (bold, italic, strikethrough)
- Lists (ordered and unordered)
- Links and blockquotes
- Horizontal rules
- Inline code

**Try it:**
```bash
txmd examples/basic.md
```

### 2. code-blocks.md
Syntax highlighting examples for various programming languages:
- Python, JavaScript, Rust, Bash
- JSON, YAML, SQL, CSS
- Plain text code blocks
- Inline code examples

**Try it:**
```bash
txmd examples/code-blocks.md
```

### 3. tables.md
Table formatting and alignment:
- Basic tables
- Column alignment (left, center, right)
- Complex data tables
- Reference tables for keybindings and features
- Tables with emoji

**Try it:**
```bash
txmd examples/tables.md
```

### 4. advanced.md
Advanced markdown features and real-world use cases:
- Nested structures (lists with code, nested blockquotes)
- Task lists
- Complex tutorial content
- Pipeline usage examples
- Integration with git and other tools
- Performance considerations

**Try it:**
```bash
txmd examples/advanced.md
```

## Testing Multiple Files

View all examples in sequence:

```bash
for file in examples/*.md; do
    echo "Viewing: $file"
    txmd "$file"
done
```

## Pipeline Examples

Test pipeline functionality with these examples:

```bash
# View basic example via pipeline
cat examples/basic.md | txmd

# View code examples
cat examples/code-blocks.md | txmd

# Combine multiple files
cat examples/basic.md examples/tables.md | txmd
```

## Creating Your Own Examples

Feel free to create your own markdown files to test txmd features:

```bash
# Create a new example
cat > my-example.md << 'EOF'
# My Example

This is my custom markdown file.

- Feature 1
- Feature 2
- Feature 3
EOF

# View it
txmd my-example.md
```

## Navigation Tips

When viewing these examples, remember the key bindings:

- `j` / `↓` - Scroll down
- `k` / `↑` - Scroll up
- `Space` / `PgDn` - Page down
- `b` / `PgUp` - Page up
- `Home` - Jump to top
- `End` - Jump to bottom
- `q` / `Ctrl+C` - Quit

## Contributing Examples

If you create interesting example files, consider contributing them:

1. Add your example file to this directory
2. Update this README with a description
3. Submit a pull request

Good examples demonstrate:
- Specific markdown features
- Real-world use cases
- Integration with other tools
- Edge cases or special formatting
