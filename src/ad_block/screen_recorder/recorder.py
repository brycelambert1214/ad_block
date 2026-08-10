"""
Pythonic based screen recording.

Description
-----------
This module provides a high-level interface for recording the screen,
retrieving replay frames, and configuring the recorder.

Classes
-------
ReplayRecorder
    Api for recording the current screen information.

Dependencies
------------
CaptureManager
    Class for managing all internal behavior of system.

RecorderSettings
    Provides validated, immutable recorder configuration.

exceptions
    Custom exceptions raised by the recorder.

numpy
    Represents captured image frames as ndarrays.

Examples
--------
>>> from ad_block import ReplayRecorder, RecorderSettings
>>> import time

>>> # Create a ReplayRecorder instance with and without custom settings
>>> recorder = ReplayRecorder()
>>> settings = RecorderSettings(fps=30, replay_seconds=5, monitor=1)
>>> recorder.settings = settings
>>> recorder.settings  # output: RecorderSettings(fps=30, replay_seconds=5, monitor=1)

>>> # Start and stop recording
>>> recorder.running  # output: False
>>> recorder.start()
>>> recorder.running  # output: True
>>> time.sleep(3)  # Record for 3 seconds
>>> recorder.stop()
>>> recorder.running  # output: False

>>> # Retrieve recording statistics and frames
>>> stats = recorder.runtime_fps()  # output: Current frames per second
>>> print(stats) # output: Capture Stats:
>>>              # output:     Total Number of Frames:: <<num_frames>>
>>>              # output:     Duration::               <<duration>>
>>>              # output:     Average fps::            <<fps>>
>>> frames = recorder.frames()  # output: List of all frames in the buffer
>>> latest_frame = recorder.latest()  # output: Most recent frame
"""
from .settings import RecorderSettings
from .capture_manager import CaptureManager, CaptureStats
from . import exceptions as ex
import numpy as np

class ReplayRecorder:
    """
    Class for recording the current screen information.

    Attributes
    ----------
    settings : RecorderSettings | None
        Configuration for the recorder, including fps, replay_seconds, and monitor index.
    manager: CaptureManager
        Manager for the internal behavior of the system.
    running: bool
        State of if the system is currently recording the screen.

    Public Methods
    --------------
    __init__(settings: RecorderSettings = None)
        Initilize the ReplayRecorder with specified RecorderSettings
    start() -> None
        Start the screen recording process.
    stop() -> None
        Stop the screen recording process.
    latest() -> np.ndarray | None
        Return the latest frame
    frames() -> list[np.ndarray]
        Return the set of all buffered frames.
    runtime_fps() -> float
        The frames per second of the whole capture time.
    runtime() -> float
        The time of the whole screen recording.
    total_frames() -> int
        The total number of frames recorded.

    Private Methods
    ---------------
    _validate_settings(
                    value: RecorderSettings | None) -> RecorderSettings | None
        Validate the input settings.
    """

    def __init__(self, settings: RecorderSettings = None):
        self._manager = CaptureManager()
        self.settings = RecorderSettings() if settings is None else settings

    @property
    def settings(self) -> RecorderSettings:
        """Property for the current recorder configuration."""
        return self._settings

    @settings.setter
    def settings(self, value: RecorderSettings | None):
        settings = self._validate_settings(value)
        if settings is not None:
            self._manager.apply_settings(settings)
            self._settings = settings

    @property
    def running(self) -> bool:
        """Property of currently screen recording."""
        return self._manager.running

    def start(self) -> None:
        """Start screen recording."""
        if self.running:
            raise ex.RecordingInProgress()
        self._manager.start()

    def stop(self) -> None:
        """Stop screen recording."""
        if not self.running:
            return
        self._manager.stop()

    def latest(self) -> np.ndarray | None:
        """Return the most recent frame."""
        return self._manager.latest()

    def frames(self) -> list[np.ndarray]:
        """Return all frames in the buffer."""
        return self._manager.frames()

    def stats(self) -> CaptureStats:
        """Return screen recording stats."""
        return self._manager.final_stats()

    def _validate_settings(
        self, value: RecorderSettings | None) -> RecorderSettings | None:
        """Validate the input settings."""
        if value is None:
            return RecorderSettings()

        if not isinstance(value, RecorderSettings):
            raise ex.InvalidType("settings must be a RecorderSettings object.")

        if hasattr(self, "_settings") and  value == self._settings:
            return None

        return value
