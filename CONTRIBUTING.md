# Contributing to txmd

Thank you for your interest in contributing to txmd! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Issue Guidelines](#issue-guidelines)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

Please be respectful and constructive in all interactions. We aim to foster an inclusive and welcoming community.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Poetry for dependency management
- Git for version control

### Finding Issues to Work On

- Check the [issue tracker](https://github.com/guglielmo/txmd/issues) for open issues
- Look for issues labeled `good first issue` for beginner-friendly tasks
- Issues labeled `help wanted` are specifically looking for contributors
- Check the project milestones to see upcoming features and priorities

## Development Setup

1. **Fork and Clone the Repository**

   ```bash
   # Fork the repository on GitHub first, then:
   git clone https://github.com/YOUR_USERNAME/txmd.git
   cd txmd
   ```

2. **Install Dependencies**

   ```bash
   # Install Poetry if you haven't already
   curl -sSL https://install.python-poetry.org | python3 -

   # Install project dependencies
   poetry install
   ```

3. **Verify Installation**

   ```bash
   # Run the application to ensure it works
   poetry run txmd README.md

   # Run tests to ensure everything is working
   poetry run pytest
   ```

## Development Workflow

### Branch Strategy

- `main` branch contains stable, released code
- Create feature branches from `main` for your work
- Use descriptive branch names: `feature/add-search`, `fix/stdin-handling`, `docs/improve-readme`

### Making Changes

1. **Create a Feature Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write clean, readable code
   - Follow the coding standards below
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Your Changes**

   ```bash
   # Run tests
   poetry run pytest

   # Run code formatting
   poetry run black txmd/

   # Sort imports
   poetry run isort txmd/

   # Run linter
   poetry run flake8 txmd/
   ```

4. **Commit Your Changes**

   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

   Use clear, descriptive commit messages:
   - Start with a verb: "Add", "Fix", "Update", "Remove"
   - Keep the first line under 50 characters
   - Add details in the body if needed

## Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use [Black](https://black.readthedocs.io/) for code formatting (line length: 88)
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Use type hints for function parameters and return values
- Maximum line length: 88 characters (Black default)

### Code Quality

- **Readability**: Write code that is easy to understand
- **Documentation**: Add docstrings to all public functions and classes
- **Type Hints**: Use type annotations for better code clarity
- **Error Handling**: Handle errors gracefully with appropriate error messages
- **No Dead Code**: Remove commented-out code and unused imports

### Documentation

- Add docstrings to all public functions, classes, and methods
- Use Google-style docstrings format:

  ```python
  def example_function(param1: str, param2: int) -> bool:
      """Brief description of function.

      More detailed description if needed. Explain what the function
      does, its purpose, and any important details.

      Args:
          param1 (str): Description of param1.
          param2 (int): Description of param2.

      Returns:
          bool: Description of return value.

      Raises:
          ValueError: When param2 is negative.

      Example:
          >>> example_function("test", 5)
          True
      """
  ```

### Textual-Specific Guidelines

- Use Textual's reactive attributes and message handlers appropriately
- Follow Textual's widget composition patterns
- Keep actions simple and focused (one action = one behavior)
- Use CSS for styling rather than inline styles
- Test TUI behavior manually in a real terminal

## Testing

### Writing Tests

- Write tests for all new features and bug fixes
- Use pytest for testing
- Place tests in the `tests/` directory
- Name test files with `test_` prefix (e.g., `test_cli.py`)
- Use descriptive test function names: `test_description_of_what_is_tested`

### Test Structure

```python
def test_feature_name():
    """Test that feature works as expected."""
    # Arrange: Set up test data
    content = "# Test Header"

    # Act: Execute the code being tested
    result = process_content(content)

    # Assert: Verify the results
    assert result is not None
    assert "Test Header" in result
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=txmd

# Run specific test file
poetry run pytest tests/test_cli.py

# Run specific test function
poetry run pytest tests/test_cli.py::test_function_name

# Run with verbose output
poetry run pytest -v
```

### Test Coverage

- Aim for high test coverage (>80%)
- Focus on testing critical paths and edge cases
- Don't sacrifice code quality for coverage numbers

## Submitting Changes

### Before Submitting

1. **Update from main**

   ```bash
   git checkout main
   git pull origin main
   git checkout your-feature-branch
   git rebase main
   ```

2. **Run all checks**

   ```bash
   # Format code
   poetry run black txmd/
   poetry run isort txmd/

   # Run linter
   poetry run flake8 txmd/

   # Run tests
   poetry run pytest
   ```

3. **Update documentation**
   - Update README.md if adding new features
   - Update CLAUDE.md if changing architecture
   - Add/update docstrings
   - Update examples if needed

### Pushing Changes

```bash
git push origin your-feature-branch
```

## Issue Guidelines

### Creating Issues

When creating an issue, please:

- **Use a clear, descriptive title**
- **Provide context**: What were you trying to do?
- **Describe the problem**: What happened vs. what you expected
- **Include steps to reproduce** (for bugs)
- **Provide environment details**: OS, Python version, txmd version
- **Add relevant labels**: bug, enhancement, documentation, etc.

### Issue Templates

**Bug Report:**
```markdown
## Description
Brief description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What you expected to happen

## Actual Behavior
What actually happened

## Environment
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.11]
- txmd version: [e.g., 0.2.0]

## Additional Context
Any other relevant information
```

**Feature Request:**
```markdown
## Description
Brief description of the feature

## Use Case
Why is this feature needed? What problem does it solve?

## Proposed Solution
How you think it should work

## Alternatives Considered
Other solutions you've thought about

## Additional Context
Any other relevant information
```

## Pull Request Process

### Creating a Pull Request

1. **Push your branch** to your fork
2. **Open a Pull Request** from your branch to `main`
3. **Fill out the PR template** with:
   - Clear description of changes
   - Reference to related issues
   - Testing performed
   - Screenshots (if UI changes)

### PR Title Format

Use conventional commit format:
- `feat: add search functionality`
- `fix: resolve stdin handling on Windows`
- `docs: update installation instructions`
- `test: add tests for markdown parsing`
- `refactor: simplify scrolling logic`

### PR Description Template

```markdown
## Summary
Brief description of what this PR does

## Related Issues
Fixes #123
Related to #456

## Changes
- Change 1
- Change 2
- Change 3

## Testing
- [ ] All existing tests pass
- [ ] Added new tests for this feature
- [ ] Manually tested on [OS/environment]
- [ ] Documentation updated

## Screenshots (if applicable)
[Add screenshots here]

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
- [ ] All tests passing
```

### Review Process

- A maintainer will review your PR
- Address any feedback or requested changes
- Once approved, a maintainer will merge your PR
- Your contribution will be included in the next release

### After Your PR is Merged

- Delete your feature branch
- Update your local repository:

  ```bash
  git checkout main
  git pull origin main
  ```

## Project Structure

Understanding the project structure helps with contributions:

```
txmd/
├── txmd/                    # Main package directory
│   ├── __init__.py         # Package initialization
│   └── cli.py              # CLI and TUI implementation
├── tests/                   # Test directory
│   ├── __init__.py
│   └── test_cli.py         # CLI tests
├── examples/                # Example markdown files
├── .github/                 # GitHub configuration
│   └── workflows/          # CI/CD workflows
├── pyproject.toml          # Poetry configuration and dependencies
├── README.md               # Project readme
├── CONTRIBUTING.md         # This file
├── CLAUDE.md               # AI assistant context
├── LICENSE                 # MIT License
└── .gitignore              # Git ignore rules
```

## Key Files

- **txmd/cli.py**: Main application code (MarkdownViewerApp, CLI entry point)
- **pyproject.toml**: Dependencies, project metadata, tool configuration
- **tests/test_cli.py**: Test suite for CLI functionality

## Architecture Notes

### Pipeline Support

The application uses a special pattern to support Unix pipelines:

1. Detects piped input with `sys.stdin.isatty()`
2. Reads stdin content
3. Reopens `/dev/tty` to restore terminal control for the TUI
4. Displays content in Textual app

### Textual App Structure

- `MarkdownViewerApp`: Main application class
- `ScrollableContainer`: Provides viewport scrolling
- `Markdown` widget: Handles markdown rendering
- Action methods: Respond to keybindings (e.g., `action_scroll_down`)
- CSS: Defines visual styling

## Getting Help

- **Questions**: Open a discussion on GitHub
- **Bugs**: Create an issue with the bug template
- **Features**: Create an issue with the feature request template
- **Chat**: Join project discussions on GitHub

## Recognition

Contributors will be:
- Listed in release notes
- Acknowledged in the project
- Helping build a better tool for the community

Thank you for contributing to txmd!
