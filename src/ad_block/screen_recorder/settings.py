# TODO: Update the module level doc string
"""
Validated configuration for ReplayRecorder.

Description
-----------
This module validates the settings needed for the ReplayRecorder class.
It ensures that the provided values for frames per second (fps), replay
duration (replay_seconds), and monitor index (monitor) are of the correct
type and within acceptable ranges. If any of the values are invalid, it
raises appropriate exceptions to inform the user of the issue.

Classes
-------
RecorderSettings
    Immutable configuration for ReplayRecorder, with validation for fps,
    replay_seconds, and monitor index.

Dependencies
------------
config
    Default configuration values.

exceptions
    Package-specific exceptions used for input validation.

Examples
--------
>>> from ad_block.screen_recorder.settings import RecorderSettings
>>> settings = RecorderSettings(fps=30, replay_seconds=5, monitor=1)
>>> print(settings)  # output: RecorderSettings(fps=30, replay_seconds=5, monitor=1)
"""

from ad_block.screen_recorder.config import (DEFAULT_EXPECTED_FPS, DEFAULT_REPLAY_SECONDS,
                     MAX_BUFFER_FRAMES, MAX_EXPECTED_FPS, MAX_REPLAY_SECONDS)
from . import exceptions as ex
import math


class RecorderSettings:
    # TODO: Update the class level doc string
    """
    Immutable configuration for ReplayRecorder.
    
    Attributes
    ----------
    expected_fps : int
        Frames per second for screen capture. Must be a positive integer.
    replay_seconds : float | int
        Number of seconds stored in the replay buffer. Must be a positive number.
    monitor : int
        Monitor index used for capture. Must be a positive integer.
    num_frames : int
        Number of frames required for the replay buffer, calculated as fps * replay_seconds.

    Methods
    -------
    __init__(expected_fps: int = DEFAULT_FPS,
      replay_seconds: float | int = DEFAULT_REPLAY_SECONDS, monitor: int = 1)
        Initialize the RecorderSettings with validated values.
    __repr__() -> str
        Return a string representation of the settings.
    __eq__(other: object) -> bool
        Check equality with another RecorderSettings object.
    replace(fps: int | None = None, replay_seconds: float | None = None, monitor: int | None = None) -> "RecorderSettings"
        Create a new settings object with selected values replaced.
    to_dict() -> dict[str, object]
        Return a dictionary representation of the settings.
    replace(fps: int | None = None, replay_seconds: float | None = None, monitor: int | None = None) -> "RecorderSettings"
        Create a new settings object with selected values replaced.
    _validate_fps(value: int) -> None
        Validate frames per second.
    _validate_replay_seconds(value: float) -> None
        Validate replay duration.
    _validate_monitor(value: int) -> None
        Validate monitor index.
    """

    __slots__ = ("_expected_fps", "_replay_seconds", "_monitor")

    def __init__(self, expected_fps: int = DEFAULT_EXPECTED_FPS,
                  replay_seconds: float | int = DEFAULT_REPLAY_SECONDS,
                    monitor: int = 1):
        self._validate_expected_fps(expected_fps)
        self._validate_replay_seconds(replay_seconds)
        self._validate_monitor(monitor)
        self._validate_buffer_size(expected_fps=expected_fps,
                                    replay_seconds=replay_seconds)

        self._expected_fps: int = expected_fps
        self._replay_seconds: float | int = replay_seconds
        self._monitor: int = monitor

    @property
    def monitor(self) -> int:
        """Monitor index used for capture."""
        return self._monitor

    @monitor.setter
    def monitor(self, _: int) -> None:
        raise ex.InvalidAttributeSetting("Cannot manually set the monitor idx.")

    @property
    def expected_fps(self) -> int:
        """Frames per second for screen capture."""
        return self._expected_fps

    @expected_fps.setter
    def expected_fps(self, _: int | float) -> None:
        raise ex.InvalidAttributeSetting("Cannot manually set the expected fps.")

    @property
    def replay_seconds(self) -> int | float:
        """Number of seconds stored in the replay buffer."""
        return self._replay_seconds

    @replay_seconds.setter
    def replay_seconds(self, _: int | float) -> None:
        raise ex.InvalidAttributeSetting("Cannot manually set"
                                         " the replay seconds")

    @property
    def num_frames(self) -> int:
        """Number of frames required for the replay buffer."""
        
        return max(1, int(self.expected_fps * self.replay_seconds))

    @num_frames.setter
    def num_frames(self, _: int) -> None:
        raise ex.InvalidAttributeSetting("Cannot manually se the"
                                         " number of frames")

    def replace(self, expected_fps: int | None = None,
                replay_seconds: float | None = None,
                  monitor: int | None = None) -> "RecorderSettings":
        """
        Create a new settings object with selected values replaced.

        The original settings object is not modified.
        """

        return RecorderSettings(
            expected_fps=(self.expected_fps if expected_fps is None 
                                                            else expected_fps),
            replay_seconds=(self.replay_seconds if replay_seconds is None
                                                        else replay_seconds),
            monitor=(self.monitor if monitor is None else monitor)
        )

    @staticmethod
    def _validate_buffer_size(expected_fps, replay_seconds):
        """Validate the buffer size."""
        num_frames = int(expected_fps * replay_seconds)
        if num_frames > MAX_BUFFER_FRAMES:
            raise ex.OutofBufferMemoryRange("Buffer cannot allocate more than"
                                            f"{MAX_BUFFER_FRAMES} frames")

    @staticmethod
    def _validate_expected_fps(value: int) -> None:
        """Validate frames per second."""

        if isinstance(value, bool) or not isinstance(value, int):
            raise ex.InvalidType("expected_fps must be an integer.")

        if value <= 0:
            raise ex.NonPositiveValue("expected_fps must be greater than zero.")

        if value > MAX_EXPECTED_FPS:
            raise ex.OutofFramesPerSecondRange("Expected fps value cannont"
                                               f"be above {MAX_EXPECTED_FPS}")

    @staticmethod
    def _validate_replay_seconds(value: int | float) -> None:
        """Validate replay duration."""

        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ex.InvalidType("replay_seconds must be numeric.")

        if not math.isfinite(value):
            raise ex.InvalidInfiniteInput("Cannot support infinite replay time")

        if value <= 0:
            raise ex.NegativeValue("replay_seconds must be greater than zero.")

        if value > MAX_REPLAY_SECONDS:
            raise ex.OutofReplaySecondRange("Replay seconds must not be greater"
                                            f"than {MAX_REPLAY_SECONDS}")

    @staticmethod
    def _validate_monitor(value: int) -> None:
        """Validate monitor index."""
        if isinstance(value, bool) or not isinstance(value, int):
            raise ex.InvalidType("Monitor must be an integer.")

        if value <= 0:
            raise ex.InvalidMonitorIndex("Monitor must be greater than zero.")

    def __repr__(self) -> str:
        """Return a string representation of the settings."""
        return (
            f"RecorderSettings("
            f"expected_fps={self.expected_fps}, "
            f"replay_seconds={self.replay_seconds}, "
            f"monitor={self.monitor})"
        )

    def __eq__(self, other: object) -> bool:
        """Check equality with another RecorderSettings object."""
        if not isinstance(other, RecorderSettings):
            return False
        return (self.expected_fps == other.expected_fps
                and self.replay_seconds == other.replay_seconds
                and self.monitor == other.monitor)

    def to_dict(self) -> dict[str, object]:
        """Return a dictionary representation of the settings."""
        return {
            "expected_fps": self.expected_fps,
            "replay_seconds": self.replay_seconds,
            "num_frames": self.num_frames,
            "monitor": self.monitor,
        }
