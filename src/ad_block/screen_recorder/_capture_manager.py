# TODO: Add the module doc string

from ad_block.screen_recorder.settings import RecorderSettings
from ad_block.screen_recorder._ring_buffer import _RingBuffer
from ad_block.screen_recorder._capture_mss import _CaptureMSS
from ad_block.screen_recorder.stats import CaptureStats
import ad_block.screen_recorder.exceptions as ex
import threading
import time

class _CaptureManager:
    # TODO: Add a class level doc string

    def __init__(self):
        self._settings = None
        self._buffer = _RingBuffer()
        self._capture = _CaptureMSS(self._buffer, self._frame_added)
        self._start_time = None
        self._end_time = None
        self._new_frame = threading.Event()

    @property
    def running(self):
        """Return if the system is currently running."""
        return self._capture.running

    @property
    def total_frames(self):
        """Property for the total number of captured frames."""
        return self._buffer.tot_added

    @total_frames.setter
    def total_frames(self, value: int) -> Exception:
        raise ex.InvalidAttributeSetting("Cannot set the total number of"
                                         " captured frames.")

    def _frame_added(self):
        self._new_frame.set()

    def wait_for_new_frame(self):
        self._new_frame.wait()
        self._new_frame.clear()

    def start(self):
        """Start the redording threading for the capture thread."""
        self._start_time = time.perf_counter()
        err = self._capture.start()
        if err is not None:
            return err

    def stop(self):
        """Stop the recording threading for the capture thread"""
        self._new_frame.set()

        err = self._capture.stop()
        self._end_time = time.perf_counter()
        if err is not None:
            return err

    def stats(self):
        """Decides which stats type to return."""
        if self._start_time is None:
            return self._pre_start_stats()
        if self._end_time is None:
            return self._current_stats()
        return self._final_stats()

    def _pre_start_stats(self):
        """Return the stats before the system starts."""
        return CaptureStats(status="Pre Start")

    def _current_stats(self):
        """Return the current stats."""
        return CaptureStats(total_frames=self._buffer.tot_added,
                            duration=time.perf_counter() - self._start_time,
                            status="Current")

    def _final_stats(self):
        """Return the final stats of the screen recording."""
        return CaptureStats(total_frames=self._buffer.tot_added,
                            duration=self._end_time - self._start_time,
                            status="Final")

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
