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

CaptureStats
    Dataclass for organizing all capture stats.

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
from ._capture_manager import _CaptureManager, CaptureStats
from . import exceptions as ex
import numpy as np
import warnings

class ReplayRecorder:
    """
    Class for recording the current screen information.

    Attributes
    ----------
    settings : RecorderSettings | None
        Configuration for the recorder, including fps, replay_seconds, and monitor index.
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
    """

    def __init__(self, settings: RecorderSettings = None):
        self._manager = _CaptureManager()
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

    @running.setter
    def running(self, value: bool) -> Exception:
        raise ex.InvalidAttributeSetting("Cannot manually"
                                         " set the running state.")

    @property
    def total_frames(self) -> int:
        """Property for the total number of frames recorded."""
        return self._manager.total_frames

    @total_frames.setter
    def total_frames(self, value: int) -> Exception:
        raise ex.InvalidAttributeSetting("Cannot set the total number of"
                                         " captured frames.")

    def wait_for_new_frame(self):
        self._manager.wait_for_new_frame()

    def start(self) -> None:
        """Start screen recording."""
        err = self._manager.start()
        if err is not None:
            warnings.warn(str(err), ex.StateWarning, stacklevel=2)

    def stop(self) -> None:
        """Stop screen recording."""
        err = self._manager.stop()
        if err is not None:
            warnings.warn(str(err), ex.StateWarning, stacklevel=2)

    def latest(self) -> np.ndarray | None:
        """Return the most recent frame."""
        return self._manager.latest()

    def frames(self) -> list[np.ndarray]:
        """Return all frames in the buffer."""
        return self._manager.frames()

    def stats(self) -> CaptureStats:
        """
        Return screen recording stats.

        Description
        -----------
        This function returns the stats at this moment in time. If called before
        the capture has begun it returns zeros with a status of "Pre Start". If
        the recorder is currently recording the stats are for that time, and if
        the recording is done it returns the final stats for the run. 
        """
        return self._manager.stats()

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
