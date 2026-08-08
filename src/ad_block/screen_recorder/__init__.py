"""
Public API for the screen recorder package.

Only objects imported here are considered part of the stable public API.
Everything else under this package is considered an implementation detail
and may change without notice.
"""

from .recorder import ReplayRecorder
from .settings import RecorderSettings
from .exceptions import ScreenRecordingError

__all__ = [
    "ReplayRecorder",
    "RecorderSettings",
    "ScreenRecordingError",
]