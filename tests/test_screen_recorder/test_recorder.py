import pytest

from ad_block.screen_recorder import ReplayRecorder, RecorderSettings
from ad_block.screen_recorder.ring_buffer import RingBuffer
from ad_block.screen_recorder.capture import CaptureThread
from ad_block.screen_recorder import exceptions as ex

from test_screen_recorder.screen_recorder_data import (
    VALID_RECORDER_SETTINGS,
    INVALID_RECORDER_SETTINGS,
)

# TODO: Finish the following checklist of tests.
#
# [x] constructor
# [x] default settings
# [x] custom settings
#
# [x] properties
# [x] settings getter
# [x] settings setter
# [x] read-only buffer
# [x] read-only capture
# [x] running
#
# [x] latest
# [x] frames
# [x] runtime_fps
# [x] runtime
# [x] total_frames
#
# [x] invalid settings type
# [ ] start
# [ ] stop
# [ ] configure while running
# [ ] integration recording


# ------------------------------------------------------------
# Constructor tests
# ------------------------------------------------------------

def test_constructor_default():
    """Test ReplayRecorder default construction."""

    recorder = ReplayRecorder()

    assert isinstance(recorder.settings, RecorderSettings)
    assert isinstance(recorder._buffer, RingBuffer)
    assert isinstance(recorder._capture, CaptureThread)


@pytest.mark.parametrize(
    "settings",
    VALID_RECORDER_SETTINGS,
)
def test_constructor_custom(settings):
    """Test construction with valid settings."""

    recorder = ReplayRecorder(settings)

    assert recorder.settings == settings


# ------------------------------------------------------------
# Property tests
# ------------------------------------------------------------

def test_settings_property():
    """Test settings property."""

    recorder = ReplayRecorder()

    settings = RecorderSettings(
        expected_fps=60,
        replay_seconds=5,
        monitor=1,
    )

    recorder.settings = settings

    assert recorder.settings == settings


def test_running_property():
    """Test running property."""

    recorder = ReplayRecorder()

    assert recorder.running is False


# ------------------------------------------------------------
# Configuration tests
# ------------------------------------------------------------

@pytest.mark.parametrize(
    "settings",
    VALID_RECORDER_SETTINGS,
)
def test_configure(settings):
    """Test applying valid settings."""

    recorder = ReplayRecorder()

    recorder.settings = settings

    assert recorder.settings == settings


@pytest.mark.parametrize(
    "value",
    INVALID_RECORDER_SETTINGS,
)
def test_invalid_settings(value):
    """Test invalid settings types."""

    recorder = ReplayRecorder()

    with pytest.raises(ex.InvalidType):
        recorder.settings = value


# ------------------------------------------------------------
# Buffer forwarding tests
# ------------------------------------------------------------

def test_latest():
    """Test latest frame forwarding."""

    recorder = ReplayRecorder()

    assert recorder.latest() is None


def test_frames():
    """Test frames forwarding."""

    recorder = ReplayRecorder()

    assert recorder.frames() == []


# ------------------------------------------------------------
# Capture forwarding tests
# ------------------------------------------------------------
def test_stats():
    """Test the stats of a capture."""
    recorder = ReplayRecorder()

    stats = recorder.stats()
    assert stats.total_frames == recorder._capture.tot_count
    assert stats.runtime == recorder._capture.runtime
