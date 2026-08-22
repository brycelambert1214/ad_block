import numpy as np
import pytest

from ad_block.data_acquisition._svd_detector import SVDChangeDetector
from ad_block.data_acquisition._detector import _DetectorManager


def test_detect_returns_false_for_unchanged_frames():
    frame = np.zeros((4, 4, 3), dtype=np.uint8)

    assert SVDChangeDetector().detect([frame, frame.copy()]) is False


def test_detect_returns_true_for_changed_frames():
    first = np.zeros((4, 4), dtype=np.uint8)
    second = first.copy()
    second[0, 0] = 255

    detector = SVDChangeDetector(threshold=0.01)

    assert detector.detect([first, second]) is True
    assert detector.change_score(first, second) > 0.01


def test_detect_handles_empty_and_single_frame_sequences():
    detector = SVDChangeDetector()

    assert detector.detect([]) is False
    assert detector.detect([np.zeros((2, 2))]) is False


@pytest.mark.parametrize("frames", [None, "frame", [np.zeros((2, 2)), np.zeros((3, 3))]])
def test_detect_rejects_invalid_frames(frames):
    with pytest.raises((TypeError, ValueError)):
        SVDChangeDetector().detect(frames)


def test_detector_rejects_negative_threshold():
    with pytest.raises(ValueError):
        SVDChangeDetector(threshold=-1)