"""Very simple logic for preliminary prediction of ads."""

from dataclasses import dataclass

from ._svd_detector import SVDChangeDetector

import time
@dataclass
class _Event:
    AD_START = None
    AD_END = None
    AD_CURRENT = None
    PROGRAM_CURRENT = None

    @property
    def UNKNOWN(self):
        if (self.AD_START is None
                and self.AD_END is None
                and self.AD_CURRENT is None
                and self.PROGRAM_CURRENT is None):
            return True
        return False

    @UNKNOWN.setter
    def UNKNOWN(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError  # TODO: add the custom error


class _DetectorManager:
    """Class for managing all data acquisition detection."""

    def __init__(self):
        self.detector = SVDChangeDetector()

    def clear_history(self):
        self.detector.reset_history()

    def detect(self, frames):
        changed = self.detector.detect(frames[-1])
        if changed:
            print("Screen change detected.")
        return changed