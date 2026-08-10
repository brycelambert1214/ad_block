# TODO: Add the module doc string

from ad_block.screen_recorder.settings import RecorderSettings
from .ring_buffer import RingBuffer
from .capture_mss import CaptureMSS
from dataclasses import dataclass
import ad_block.screen_recorder.exceptions as ex
import time


@dataclass
class CaptureStats:
    """
    Class for representing all capture stats.

    Methods
    -------
    __str__():
        Return a string with the information of capture stats.

    Examples
    --------
    >>> stats = CaptureStats(total_frames=tot_frames, duration=time_of_capture)
    >>> print(stats)
    >>> # output:
    >>> # CaptureStats:
    >>> #     Total Number of Frames:: tot_frames
    >>> #     Duration::               time_of_capture
    >>> #     Average fps::            tot_frames / time_of_capture
    """
    total_frames: int
    duration: float

    @property
    def fps(self):
        """Return the measured fps."""
        if self.duration == 0:
            return 0
        return self.total_frames / self.duration

    def __str__(self):
        return (f"Capture Stats:\n"
                f"\tTotal Number of Frames:: {self.total_frames:>5}\n"
                f"\tDuration::               {self.duration:>7.3f}\n"
                f"\tAverage fps::            {self.fps:>8.3f}")
    


class CaptureManager:
    # TODO: Add a class level doc string

    def __init__(self):
        self._settings = None
        self._buffer = RingBuffer()
        self._capture = CaptureMSS(self._buffer)
        self._start_time = None
        self._end_time = None

    @property
    def running(self):
        """Return if the system is currently running."""
        return self._capture.running

    def start(self):
        """Start the redording threading for the capture thread."""
        self._start_time = time.perf_counter()
        self._capture.start()

    def stop(self):
        """Stop the recording threading for the capture thread"""
        self._capture.stop()
        self._end_time = time.perf_counter()

    def current_stats(self):
        """Return the current stats."""
        return CaptureStats(total_frames=self._buffer.tot_added,
                            duration=time.perf_counter() - self._start_time)

    def final_stats(self):
        """Return the final stats of the screen recording."""
        return CaptureStats(total_frames=self._buffer.tot_added,
                            duration=self._end_time - self._start_time)

    def frames(self):
        """Return filled or partially filled buffer."""
        return self._buffer.snapshot()

    def latest(self):
        """Return the latest frame."""
        return self._buffer.latest()

    def apply_settings(self, settings: RecorderSettings):
        """Apply new settings internals."""
        if self.running:
            raise ex.RecordingInProgress("Cannot apply settings during run.")
        self._buffer.resize(settings.num_frames)
        self._capture.monitor_idx = settings.monitor
        self._settings = settings
