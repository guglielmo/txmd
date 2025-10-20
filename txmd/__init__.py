"""txmd - A terminal-based markdown viewer with pipeline support."""

try:
    from importlib.metadata import version

    __version__ = version("txmd")
except Exception:
    __version__ = "unknown"
