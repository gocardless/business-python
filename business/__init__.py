"""Init."""
# mypy: ignore-errors


def get_version() -> str:
    """Get package version."""
    from importlib.metadata import version

    return version("business")


# noinspection PyBroadException
try:
    __version__ = get_version()
except Exception:
    # development mode: set dev version if package is not installed
    __version__ = "dev"
