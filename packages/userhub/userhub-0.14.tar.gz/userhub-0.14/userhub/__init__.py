"""
Initializing the Python package
"""

from .auth import detect_type, auth, token
from .model import BaseUser


__version__ = "0.14"

__all__ = (
    "__version__",
    "detect_type",
    "auth",
    "token",
    "BaseUser",
)
