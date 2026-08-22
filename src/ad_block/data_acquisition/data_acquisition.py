"""
This Module will provide the API for acquiring training data.
"""
import threading
import time

from ad_block.data_acquisition import exceptions as ex
from ad_block.data_acquisition._detector import _DetectorManager
from ad_block.data_acquisition._interface import _Interface
from ad_block.data_acquisition._storage import _Storage
from ad_block.data_acquisition.settings import DataAcquisitionSettings
from ad_block.screen_recorder import ReplayRecorder


class DataAcquisition:
    """Class for user based data acquisition."""

    def __init__(self, settings: DataAcquisitionSettings | None = None):
        self.settings = (DataAcquisitionSettings() if settings is None
                         else settings)
        self._detector = _DetectorManager()
        self._storage = _Storage(r"C:\Users\bryce\Documents\Projects\ad_block")
        self._interface = _Interface()
        self._recorder = ReplayRecorder()
        self._is_event = None
        self._running = threading.Event()
        self._thread: threading.Thread | None = None
        self._skip_frame = False

    @property
    def settings(self) -> DataAcquisitionSettings:
        """Property for data acquisition settings."""
        return self._settings

    @settings.setter
    def settings(self, value: DataAcquisitionSettings | None):
        settings = self._validate_settings(value)
        if settings is not None:
            self._apply_settings(settings)
            self._settings = settings

    def _validate_settings(self, value:
              DataAcquisitionSettings | None) -> DataAcquisitionSettings | None:
        pass

    def _apply_settings(self, value:
              DataAcquisitionSettings | None) -> DataAcquisitionSettings | None:
        pass

    @property
    def running(self) -> bool:
        """Current state of the capture thread."""
        return self._running.is_set()

    @running.setter
    def running(self, value: bool) -> Exception:
        raise ex.InvalidAttributeSetting("Cannot set the state of running.")

    def start(self):
        if self.running:
            return ex.RecordingInProgress()

        try:
            self._recorder.start()

            self._running.set()
            self._storage.start()
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()

        except Exception:
            self._running.clear()
            self._thread = None

            if self._recorder.running:
                self._recorder.stop()
                self._storage.stop()
            raise

    def stop(self):
        if not self.running:
            return ex.RecordingInProgress()

        self._running.clear()

        self._recorder.stop()
        self._storage.stop()

        if self._thread is not None:
            self._thread.join()

        self._thread = None
        

    def _run(self):
        count = 1
        while self.running:
            if self._skip_frame:
                self._skip_frame = False
                continue
            self._recorder.wait_for_new_frame()
            print(count)
            count += 1
            if not self.running:
                break

            self._check_event()

    def _check_event(self):

        frames = self._recorder.frames()

        if not self._detector.detect(frames):
            return

        response = self._interface.get_event_confirmation()

        if response:
            frames = self._recorder.frames()
            self._storage.store_frames(frames, True)
            self._detector.clear_history()
            time.sleep(4)
            frames = self._recorder.frames()
            self._storage.store_frames(frames, False)
        else:
            self._detector.clear_history()
            self._skip_frame = True
            time.sleep(0.2)


def main():
    acquisition = DataAcquisition()
    acquisition.start()

    try:
        while acquisition.running:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        acquisition.stop()
 

if __name__ == "__main__":
    main()