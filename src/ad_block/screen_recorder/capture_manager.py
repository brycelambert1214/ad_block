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

    def __init__(self, settings: RecorderSettings):
        self._settings = settings
        self._buffer = RingBuffer(capacity=self._settings.num_frames)
        # TODO: add the type of capture to the settings
        self._capture = CaptureThread(self._settings.monitor)
        self._start_time = None
        self._end_time = None

    @property
    def running(self):
        """Return if the system is currently running."""

    def start(self):
        """Start the redording threading for the capture thread."""
        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the recording threading for the capture thread"""
        # other stuff
        self._end_time = time.perf_counter()

    def current_stats(self):
        """Return the current stats."""

    def final_stats(self):
        """Return the final stats of the screen recording."""

    def frames(self):
        """Return filled or partially filled buffer."""

    def latest(self):
        """Return the latest frame."""

    def _apply_settings(self, settings: RecorderSettings):
        """Apply new settings internals."""

