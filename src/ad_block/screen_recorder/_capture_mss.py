# TODO: Update the module level doc string
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
import mss
import numpy as np
from ._ring_buffer import _RingBuffer
from . import exceptions as ex

# TODO: add error handling for thread by storing error and raising in the stop
class _CaptureMSS:
    # TODO: Update the class level doc string
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

    def __init__(self,buffer: _RingBuffer, callback: function = None):
        self._buffer = buffer
        self._monitor_idx = None

        self._running = threading.Event()
        self._thread: threading.Thread | None = None
        self._callback = callback

        self._monitor: dict | None = None
        self._error: Exception | None = None

    @property
    def monitor_idx(self) -> int:
        """Property for monitor_idx."""
        return self._monitor_idx

    @monitor_idx.setter
    def monitor_idx(self, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int):
            raise ex.InvalidType("The monitor must be of type 'int'")
        if value <= 0:
            raise ex.InvalidMonitorIndex("The monitor of interest must"
                                         " be indexed above 0")
        self._monitor_idx = value

    @property
    def running(self) -> bool:
        """Current state of the capture thread."""
        return self._running.is_set()

    @running.setter
    def running(self, value: bool) -> Exception:
        raise ex.InvalidAttributeSetting("Cannot set the state of running.")

    def _validate_monitor(self) -> None:
        """Validate the monitor index."""
        with mss.MSS() as sct:

            # monitor index it over the number of real monitors
            if self._monitor_idx >= len(sct.monitors):
                x = len(sct.monitors)
                raise ex.InvalidMonitorIndex(
                    f"Monitor {self._monitor_idx} does not exist. "
                    f"Available monitors: {len(sct.monitors) - 1}"
                )
            self._monitor = sct.monitors[self._monitor_idx]

    def start(self) -> None | ex.RecordingInProgress:
        """Start the screen capture thread."""
        if self.running:
            return ex.RecordingInProgress()

        self._error = None
        self._validate_monitor()
        self._running.set()

        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None | ex.RecordingInProgress:
        """Stop the screen capture thread."""
        if not self.running:
            return ex.RecordingInProgress()

        self._running.clear()

        if self._thread is not None:
            self._thread.join()

        self._thread = None
        self._monitor = None

        if self._error is not None:
            raise self._error

    def _run(self) -> None:
        """
        Capture frames until stopped.

        Frames are captured as quickly as possible and passed directly
        to the RingBuffer.
        """
        try:
            with mss.MSS() as sct:
                while self._running.is_set():
                    screenshot = sct.grab(self._monitor)
                    frame = np.asarray(screenshot)[:, :, :3]
                    self._buffer.add(frame)

                    if self._callback is not None:
                        self._callback()

        except Exception as err:
            self._error = err

        finally:
            self._running.clear()
            self._monitor = None
