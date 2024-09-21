"""MySpeed API Python client."""

import python_myspeed.exceptions  # noqa: F401
from python_myspeed._version import (
    __author__,
    __copyright__,  # noqa: F401
    __email__,
    __license__,
    __title__,
    __version__,
)
from python_myspeed.core import MySpeedAPI  # noqa: F401

__all__ = [
    "__author__",
    "__copyright__",
    "__email__",
    "__license__",
    "__title__",
    "__version__",
    "MySpeedAPI",
]
__all__.extend(python_myspeed.exceptions.__all__)
