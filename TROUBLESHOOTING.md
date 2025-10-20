# Troubleshooting Guide

This guide helps you resolve common issues when using txmd.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Runtime Errors](#runtime-errors)
- [Display Issues](#display-issues)
- [Pipeline Issues](#pipeline-issues)
- [Performance Issues](#performance-issues)
- [Platform-Specific Issues](#platform-specific-issues)
- [Getting Help](#getting-help)

## Installation Issues

### Poetry Installation Fails

**Problem:** `poetry install` fails with dependency resolution errors.

**Solutions:**

1. **Update Poetry:**
   ```bash
   poetry self update
   ```

2. **Clear Poetry cache:**
   ```bash
   poetry cache clear pypi --all
   ```

3. **Try with verbose output:**
   ```bash
   poetry install -vvv
   ```

4. **Check Python version:**
   ```bash
   python --version  # Should be 3.9 or higher
   ```

### pip Installation Fails

**Problem:** `pip install txmd` fails.

**Solutions:**

1. **Upgrade pip:**
   ```bash
   pip install --upgrade pip
   ```

2. **Try with user install:**
   ```bash
   pip install --user txmd
   ```

3. **Use virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install txmd
   ```

### Command Not Found After Installation

**Problem:** `txmd: command not found` after installation.

**Solutions:**

1. **Check if installed with pip --user:**
   - On Linux/macOS: Add `~/.local/bin` to PATH
   - On Windows: Add `%APPDATA%\Python\Scripts` to PATH

2. **Use Poetry:**
   ```bash
   poetry run txmd README.md
   ```

3. **Find installation location:**
   ```bash
   pip show txmd
   python -m txmd README.md  # Alternative way to run
   ```

## Runtime Errors

### "No module named 'txmd'"

**Problem:** Python can't find the txmd module.

**Solutions:**

1. **Verify installation:**
   ```bash
   pip list | grep txmd
   ```

2. **Reinstall:**
   ```bash
   pip uninstall txmd
   pip install txmd
   ```

3. **Check Python environment:**
   ```bash
   which python
   which txmd
   ```

### "Error: No input provided"

**Problem:** Running `txmd` without arguments shows this error.

**Solutions:**

This is expected behavior. txmd requires either a file argument or piped input:

```bash
# Correct usage:
txmd README.md           # With file
echo "# Test" | txmd     # With pipe
cat file.md | txmd       # With pipe

# Incorrect:
txmd                     # No input - causes error
```

### Permission Denied Errors

**Problem:** `Permission denied` when reading files.

**Solutions:**

1. **Check file permissions:**
   ```bash
   ls -l your-file.md
   chmod +r your-file.md  # Make file readable
   ```

2. **Check if file exists:**
   ```bash
   ls your-file.md
   ```

3. **Use absolute path:**
   ```bash
   txmd /full/path/to/file.md
   ```

### Unicode/Encoding Errors

**Problem:** `UnicodeDecodeError` when opening files.

**Solutions:**

1. **Check file encoding:**
   ```bash
   file -i your-file.md
   ```

2. **Convert to UTF-8:**
   ```bash
   iconv -f ISO-8859-1 -t UTF-8 input.md > output.md
   txmd output.md
   ```

## Display Issues

### Terminal Colors Not Working

**Problem:** No syntax highlighting or colors appear.

**Solutions:**

1. **Check terminal capabilities:**
   ```bash
   echo $TERM
   # Should be something like: xterm-256color, screen-256color
   ```

2. **Set TERM variable:**
   ```bash
   export TERM=xterm-256color
   ```

3. **Test with different terminal:**
   - Try iTerm2, Alacritty, or Windows Terminal
   - Avoid basic terminals that don't support colors

### Text Rendering Issues

**Problem:** Characters appear garbled or overlap.

**Solutions:**

1. **Use a terminal with good Unicode support:**
   - iTerm2 (macOS)
   - Alacritty (cross-platform)
   - Windows Terminal (Windows)
   - GNOME Terminal (Linux)

2. **Check font:**
   - Use a monospace font
   - Recommended: Fira Code, JetBrains Mono, Cascadia Code

3. **Set locale:**
   ```bash
   export LANG=en_US.UTF-8
   export LC_ALL=en_US.UTF-8
   ```

### Screen Size Issues

**Problem:** Content doesn't fit properly in terminal.

**Solutions:**

1. **Resize terminal:**
   - Make terminal window larger
   - txmd adapts to terminal size

2. **Check minimum size:**
   - Minimum recommended: 80x24 characters

### Markdown Not Rendering Correctly

**Problem:** Markdown elements don't display as expected.

**Solutions:**

1. **Check markdown syntax:**
   - Ensure proper spacing around headers (#)
   - Verify list formatting
   - Check code block fences (```)

2. **Test with example files:**
   ```bash
   txmd examples/basic.md
   ```

3. **Verify file content:**
   ```bash
   cat your-file.md  # Check if content is valid
   ```

## Pipeline Issues

### Pipeline Not Working

**Problem:** Piped input doesn't work or hangs.

**Solutions:**

1. **Verify pipeline:**
   ```bash
   # Test if pipe produces output
   echo "# Test" | cat

   # Then try with txmd
   echo "# Test" | txmd
   ```

2. **Check for interactive prompts:**
   - Ensure source command doesn't require input
   - Use non-interactive flags if available

3. **Try with explicit input:**
   ```bash
   cat file.md | txmd
   ```

### Terminal Control Issues After Piping

**Problem:** Terminal doesn't respond to keyboard after using pipeline.

**Solutions:**

1. **This should be automatic**, but if it fails:
   ```bash
   reset  # Reset terminal
   ```

2. **Check /dev/tty access:**
   ```bash
   ls -l /dev/tty
   # Should be readable and writable
   ```

3. **Platform-specific:**
   - Linux/macOS: Should work automatically
   - Windows: May require Windows Terminal or WSL

### stdin Detection Issues

**Problem:** txmd doesn't recognize piped input.

**Solutions:**

1. **Explicit file input:**
   ```bash
   # Instead of: cat file.md | txmd
   txmd file.md
   ```

2. **Check stdin:**
   ```bash
   # Verify stdin works
   echo "test" | cat
   ```

## Performance Issues

### Slow Loading on Large Files

**Problem:** txmd takes a long time to load large markdown files.

**Solutions:**

1. **View file sections:**
   ```bash
   head -n 500 large-file.md | txmd
   tail -n 500 large-file.md | txmd
   ```

2. **Split large files:**
   ```bash
   split -l 1000 large-file.md section-
   txmd section-aa
   ```

3. **Check file size:**
   ```bash
   ls -lh large-file.md
   # Files > 10MB may be slow
   ```

### High Memory Usage

**Problem:** txmd uses excessive memory.

**Solutions:**

1. **Process smaller chunks:**
   ```bash
   sed -n '1,1000p' file.md | txmd
   ```

2. **Monitor memory:**
   ```bash
   # On Linux
   ps aux | grep txmd

   # On macOS
   top -p $(pgrep txmd)
   ```

### Sluggish Scrolling

**Problem:** Scrolling feels slow or laggy.

**Solutions:**

1. **Check terminal performance:**
   - GPU acceleration: Enable in terminal settings
   - Try different terminal emulator

2. **Reduce document size:**
   - Split into smaller files
   - Remove unnecessary content

3. **Update Textual:**
   ```bash
   poetry update textual
   ```

## Platform-Specific Issues

### Windows Issues

#### Windows Terminal Required

**Problem:** txmd doesn't work well in Command Prompt.

**Solution:** Use Windows Terminal or PowerShell 7+:
```powershell
# Install Windows Terminal from Microsoft Store
# Or use PowerShell
pwsh -Command "txmd README.md"
```

#### Path Issues

**Problem:** Windows paths with spaces or backslashes cause errors.

**Solutions:**

1. **Use quotes:**
   ```powershell
   txmd "C:\Users\Name\Documents\file.md"
   ```

2. **Use forward slashes:**
   ```powershell
   txmd C:/Users/Name/Documents/file.md
   ```

#### /dev/tty Not Available

**Problem:** `/dev/tty` doesn't exist on Windows.

**Solution:** Use WSL (Windows Subsystem for Linux) for full pipeline support:
```bash
wsl -e txmd README.md
```

### macOS Issues

#### Permission Errors in Terminal

**Problem:** Terminal access denied errors.

**Solution:** Grant Terminal full disk access:
1. System Preferences → Security & Privacy → Privacy
2. Full Disk Access → Add Terminal app

#### Homebrew Python Issues

**Problem:** Multiple Python versions cause conflicts.

**Solution:**
```bash
# Use specific Python version
python3.11 -m pip install txmd

# Or use pyenv
pyenv install 3.11.0
pyenv local 3.11.0
pip install txmd
```

### Linux Issues

#### Missing /dev/tty

**Problem:** `/dev/tty` not accessible (rare).

**Solution:**
```bash
# Check permissions
ls -l /dev/tty

# Should show: crw-rw-rw- 1 root tty

# If not, this is a system configuration issue
```

#### Terminal Emulator Compatibility

**Problem:** Some terminal emulators don't work well.

**Recommended terminals:**
- GNOME Terminal
- Konsole
- Alacritty
- kitty

## Debug Mode

### Enable Verbose Output

Get more information about errors:

```bash
# Run with Python directly to see full traceback
python -m txmd README.md

# Check Poetry environment
poetry run python -c "import txmd; print(txmd.__file__)"
```

### Check Dependencies

Verify all dependencies are installed:

```bash
# List installed packages
poetry show

# Check specific package
poetry show textual
```

### Test Installation

Run tests to verify installation:

```bash
# Clone repository
git clone https://github.com/guglielmo/txmd.git
cd txmd

# Install dev dependencies
poetry install

# Run tests
poetry run pytest -v
```

## Common Error Messages

### "TextualError: Unable to retrieve dimensions"

**Cause:** Terminal size can't be determined.

**Solution:** Ensure you're running in a proper terminal (not as a background process).

### "OSError: [Errno 6] No such device or address"

**Cause:** Terminal device not available (often in CI/automated environments).

**Solution:** txmd requires an interactive terminal. Use file arguments instead of stdin in automated environments.

### "ModuleNotFoundError: No module named 'rich'"

**Cause:** Dependencies not fully installed.

**Solution:**
```bash
pip install --force-reinstall txmd
```

## Getting Help

If you still have issues:

1. **Check existing issues:**
   - Visit: https://github.com/guglielmo/txmd/issues
   - Search for your problem

2. **Create a new issue:**
   - Include: OS, Python version, txmd version
   - Provide: Full error message
   - Add: Steps to reproduce
   - Example template:

```markdown
## Environment
- OS: Ubuntu 22.04
- Python: 3.11.4
- txmd: 0.2.0
- Terminal: GNOME Terminal

## Problem
Description of the issue...

## Steps to Reproduce
1. Run command...
2. See error...

## Error Message
```
Full error output here
```

## Expected Behavior
What should happen...

## Actual Behavior
What actually happens...
```

3. **Community Help:**
   - GitHub Discussions
   - Stack Overflow (tag: `txmd`)

4. **Quick Diagnostics:**

```bash
# Gather diagnostic information
echo "=== System Info ==="
uname -a
echo "=== Python Version ==="
python --version
echo "=== txmd Version ==="
pip show txmd
echo "=== Terminal ==="
echo $TERM
echo "=== Locale ==="
locale
```

Save this output when reporting issues!
