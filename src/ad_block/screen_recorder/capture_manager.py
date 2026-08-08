# TODO: Add the module doc string

from ad_block.screen_recorder.settings import RecorderSettings
from .ring_buffer import RingBuffer
from .capture import CaptureThread
from dataclasses import dataclass
import time


@dataclass
class CaptureStats:
    total_frames: int
    duration: float

    @property
    def fps(self):
        """Return the measured fps."""
        if self.duration == 0:
            return 0
        return self.total_frames / self.duration


class Manager:
    # TODO: Add a class level doc string


    def __init__(self, settings: RecorderSettings):
        self._settings = settings
        print(self._settings)
        self._buffer = RingBuffer(capacity=self._settings.num_frames)
        self._capture = CaptureThread(self._buffer, self._settings.monitor)
        self._start_time = None
        self._end_time = None

    @property
    def running(self):
        """Return if the system is currently running."""
        return self._capture.running

    def start(self):
        """Start the redording threading for the capture thread."""
        self._start_time = time.perf_counter()
        self._capture.start_capture()

    def stop(self):
        """Stop the recording threading for the capture thread"""
        self._capture.stop_capture()
        self._end_time = time.perf_counter()

    def current_stats(self):
        """Return the current stats."""
        return CaptureStats(total_frames=self._buffer.size,
                            duration=time.perf_counter() - self._start_time)

    def final_stats(self):
        """Return the final stats of the screen recording."""
        return CaptureStats(total_frames=self._buffer.size,
                            duration=self._end_time - self._start_time)

    def frames(self):
        """Return filled or partially filled buffer."""
        return self._buffer.snapshot()

    def latest(self):
        """Return the latest frame."""
        return self._buffer.latest()

    def _apply_settings(self, settings: RecorderSettings):
        """Apply new settings internals."""

