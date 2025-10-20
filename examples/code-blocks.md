# Code Blocks Example

This example demonstrates syntax highlighting for various programming languages in txmd.

## Python

```python
def factorial(n: int) -> int:
    """Calculate the factorial of a number."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# Example usage
result = factorial(5)
print(f"5! = {result}")
```

## JavaScript

```javascript
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// Example usage
console.log(`Fibonacci(10) = ${fibonacci(10)}`);
```

## Bash

```bash
#!/bin/bash

# Example script to process markdown files
for file in *.md; do
    echo "Processing $file..."
    txmd "$file"
done
```

## Rust

```rust
fn main() {
    let numbers = vec![1, 2, 3, 4, 5];

    let sum: i32 = numbers.iter().sum();
    println!("Sum: {}", sum);

    let doubled: Vec<i32> = numbers.iter()
        .map(|x| x * 2)
        .collect();
    println!("Doubled: {:?}", doubled);
}
```

## JSON

```json
{
  "name": "txmd",
  "version": "0.2.0",
  "description": "Terminal markdown viewer",
  "features": [
    "Syntax highlighting",
    "Pipeline support",
    "Vim-style navigation"
  ]
}
```

## YAML

```yaml
name: txmd
version: 0.2.0
description: Terminal markdown viewer

features:
  - Syntax highlighting
  - Pipeline support
  - Vim-style navigation

dependencies:
  textual: ^0.86.3
  typer: ^0.13.1
  rich: ^13.9.4
```

## SQL

```sql
-- Create a users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO users (username, email) VALUES
    ('alice', 'alice@example.com'),
    ('bob', 'bob@example.com');

-- Query users
SELECT username, email FROM users WHERE created_at > '2024-01-01';
```

## CSS

```css
/* Styling for markdown viewer */
.markdown-container {
    width: 100%;
    height: 100%;
    background-color: #1e1e1e;
    color: #d4d4d4;
    font-family: 'Fira Code', monospace;
}

.code-block {
    padding: 1em;
    border-radius: 4px;
    background-color: #2d2d2d;
}
```

## Plain Text Code Block

```
This is a plain text code block without syntax highlighting.
It's useful for generic output or documentation.
```

## Inline Code

You can also use inline code like `print("Hello")` within paragraphs.
