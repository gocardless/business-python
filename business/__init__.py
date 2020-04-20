"""Init."""


def get_version():
    """Get package version."""
    try:
        from importlib.metadata import version
    except ImportError:
        from importlib_metadata import version  # type: ignore
    return version("business")


# noinspection PyBroadException
try:
    __version__ = get_version()
except Exception:
    # development mode: set dev version if package is not installed
    __version__ = "dev"
