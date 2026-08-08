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
RingBuffer
    Stores the most recent captured frames.

CaptureThread
    Performs screen capture in a background thread.

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
>>> recorder.runtime_fps()  # output: Current frames per second
>>> recorder.runtime()  # output: Total runtime of the recording
>>> recorder.total_frames()  # output: Total number of frames recorded
>>> frames = recorder.frames()  # output: List of all frames in the buffer
>>> latest_frame = recorder.latest()  # output: Most recent frame
"""
from .ring_buffer import RingBuffer
from .capture import CaptureThread
from .settings import RecorderSettings
from .capture_manager import Manager
from . import exceptions as ex
import numpy as np
from dataclasses import dataclass


@dataclass(frozen=True)
class CaptureStats:
    total_frames: int
    runtime: float

    @property
    def fps(self):
        """Return the measured fps."""
        if self.runtime == 0:
            return 0
        return self.total_frames / self.runtime


class ReplayRecorder:
    """
    Class for recording the current screen information.

    Attributes
    ----------
    settings : RecorderSettings | None
        Configuration for the recorder, including fps, replay_seconds, and monitor index.
    buffer : RingBuffer
        Thread-safe ring buffer for storing captured frames.
    capture : CaptureThread
        Thread responsible for capturing screen frames and storing them in the buffer.
    running: bool
        State of if the system is currently recording the screen.

    Methods
    -------
    __init__(settings: RecorderSettings = None)
        Initilize the ReplayRecorder with specified RecorderSettings
    start() -> None
        Start the screen recording process.
    stop() -> None
        Stop the screen recording process.
    _configure() -> None
        Configure the settings throughout the system
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
        self._settings = settings or RecorderSettings()
        self._manager = Manager(settings)
        self._buffer = RingBuffer(self._settings.num_frames)
        self._capture = CaptureThread(self._buffer, self._settings)

    @property
    def settings(self) -> RecorderSettings:
        """Property for the current recorder configuration."""
        return self._settings

    @settings.setter
    def settings(self, value: RecorderSettings | None):
        self._configure(value or RecorderSettings())

    @property
    def running(self) -> bool:
        """Property of currently screen recording."""
        return self._capture.running

    def _configure(self, settings: RecorderSettings) -> None:
        """Apply a new recorder configuration."""

        if not isinstance(settings, RecorderSettings):
            raise ex.InvalidType(
                "settings must be a RecorderSettings object."
            )

        if self.running:
            raise ex.RecordingInProgress()

        if settings == self._settings:
            return

        self._buffer.resize(settings.num_frames)
        # self.capture.fps = settings.fps

        self._settings = settings

    def start(self) -> None:
        """Start screen recording."""
        if self.running:
            raise ex.RecordingInProgress()
        self._capture.start_capture()

    def stop(self) -> None:
        """Stop screen recording."""
        if not self.running:
            return
        self._capture.stop_capture()

    def latest(self) -> np.ndarray | None:
        """Return the most recent frame."""
        return self._buffer.latest()

    def frames(self) -> list[np.ndarray]:
        """Return all frames in the buffer."""
        return self._buffer.snapshot()

    def stats(self) -> CaptureStats:
        """Return screen recording stats."""
        return CaptureStats(total_frames=self._capture.tot_count,
                              runtime=self._capture.runtime)

