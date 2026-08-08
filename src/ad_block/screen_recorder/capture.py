"""
This is the method used for capturing all information from the screen.

Description
-----------
This module provides a thread-safe method for capturing screen shots using
the 'mss' package. The CaptureThread class allows starting and stopping screen
recording on a specified monitor.

The screen recording focuses on high capture speed. The actual achieved FPS
depends on the screen capture hardware and processing performance.

Classes
-------
CaptureThread
    Thread-managed capture method for taking screen shots.

Dependencies
------------
ReplayRecorder
    High-level interface for recording and exporting replay clips.

RingBuffer
    Thread-safe storage for the most recent captured frames.

RecorderSettings
    Validated recorder configuration.

exceptions
    Package-specific exceptions raised during recorder operation.

numpy
    Provides ndarray support for captured image frames.

Examples
--------
>>> from ad_block.screen_recorder.capture import CaptureThread
>>> from ad_block.screen_recorder.ring_buffer import RingBuffer
>>> from ad_block.screen_recorder.settings import RecorderSettings
>>> import time

>>> settings = RecorderSettings()
>>> buffer = RingBuffer(settings.num_frames)

>>> capture = CaptureThread(buffer, settings)

>>> capture.start_capture()
>>> time.sleep(2)
>>> capture.stop_capture()

>>> print(capture.runtime)
>>> print(capture.tot_count)
"""

import threading
import time

import mss
import numpy as np

from .settings import RecorderSettings
from .ring_buffer import RingBuffer
from . import exceptions as ex


class CaptureThread:
    """
    Capture all screen related information.

    Attributes
    ----------
    buffer : RingBuffer
        Stores the most recent captured frames.

    settings : RecorderSettings
        Provides validated recorder configuration.

    running : bool
        Current state of screen capture.

    tot_count : int
        Total number of frames recorded after capture stops.

    runtime : float
        Total time spent recording.

    fps : float
        Average achieved frames per second.

    Methods
    -------
    __init__(buffer: RingBuffer, settings: RecorderSettings)
        Initialize capture manager.

    start_capture() -> None
        Start screen recording.

    stop_capture() -> None
        Stop screen recording.

    run() -> None
        Capture frames until stopped.

    _validate_monitor() -> None
        Validate monitor index.
    """

    def __init__(
        self,
        buffer: RingBuffer,
        settings: RecorderSettings
    ):
        self.buffer = buffer
        self.settings = settings

        self._running = threading.Event()
        self._thread: threading.Thread | None = None

        self._monitor: dict | None = None

        self._tot_count = 0
        self._runtime = 0.0

    @property
    def settings(self) -> RecorderSettings:
        """Current recorder configuration."""
        return self._settings

    @settings.setter
    def settings(self, value: RecorderSettings):
        if not isinstance(value, RecorderSettings):
            raise ex.InvalidType(
                "settings must be a RecorderSettings object."
            )

        self._settings = value

    @property
    def running(self) -> bool:
        """Current state of the capture thread."""
        return self._running.is_set()

    @property
    def tot_count(self) -> int:
        """
       Total frames recorded.

        Cannot be accessed while recording is active.
        """
        if self.running:
            raise ex.RecordingInProgress(
                "Cannot get total count while recording is in progress."
            )

        return self._tot_count

    @property
    def runtime(self) -> float:
        """
        Total recording runtime.

        Cannot be accessed while recording is active.
        """
        if self.running:
            raise ex.RecordingInProgress(
                "Cannot get runtime while recording is in progress."
            )

        return self._runtime

    @property
    def fps(self) -> float:
        """Average achieved frames per second."""

        if self._runtime == 0:
            return 0.0

        return self._tot_count / self._runtime

    @property
    def thread(self) -> threading.Thread | None:
        """Current internal capture thread."""
        return self._thread

    def _validate_monitor(self) -> None:
        """Validate the monitor index."""

        with mss.MSS() as sct:

            if self.settings.monitor >= len(sct.monitors):
                raise ex.InvalidMonitorIndex(
                    f"Monitor {self.settings.monitor} does not exist. "
                    f"Available monitors: {len(sct.monitors) - 1}"
                )

            self._monitor = sct.monitors[self.settings.monitor]

    def start_capture(self) -> None:
        """Start the screen capture thread."""

        if self.running:
            return

        self._tot_count = 0
        self._runtime = 0.0

        self._validate_monitor()

        self._running.set()

        self._thread = threading.Thread(
            target=self.run,
            daemon=True
        )

        self._thread.start()

    def stop_capture(self) -> None:
        """Stop the screen capture thread."""

        if not self.running:
            return

        self._running.clear()

        if self._thread is not None:
            self._thread.join()

        self._thread = None
        self._monitor = None

    def run(self) -> None:
        """
        Capture frames until stopped.

        Frames are captured as quickly as possible and passed directly
        to the RingBuffer.
        """

        count = 0
        start = time.perf_counter()

        try:

            with mss.MSS() as sct:

                while self._running.is_set():

                    screenshot = sct.grab(self._monitor)

                    frame = np.asarray(
                        screenshot
                    )[:, :, :3]

                    self.buffer.add(frame)

                    count += 1

        except Exception:
            self._running.clear()
            raise

        finally:

            self._tot_count = count

            self._runtime = (
                time.perf_counter() - start
            )

            self._running.clear()
            self._monitor = None
