import pytest

from ad_block.screen_recorder import RecorderSettings
from ad_block.screen_recorder import exceptions as ex

# TODO:
# Add the valid data for all unimplemented tests
from test_screen_recorder.screen_recorder_data import (
    VALID_SETTINGS,
    INVALID_FPS_VALUES,
    INVALID_FPS_TYPES,
    INVALID_REPLAY_SECONDS_VALUES,
    INVALID_REPLAY_SECONDS_TYPES,
    INVALID_MONITOR_VALUES,
    INVALID_MONITOR_TYPES,
)

# TODO: Finish the following checklist of tests.
#
#  [x] default construction
#  [x] valid construction
#  [x] properties
#  [x] num_frames
#  [x] replace
#  [x] equality
#  [x] repr
#  [x] to_dict

#  [ ] valid fps values
#  [x] invalid fps values
#  [x] invalid fps types
#  [ ] bool fps behavior

#  [ ] valid replay_seconds values
#  [x] invalid replay_seconds values
#  [x] invalid replay_seconds types
#  [ ] fractional replay_seconds behavior

#  [ ] valid monitor values
#  [x] invalid monitor values
#  [x] invalid monitor types
#  [ ] bool monitor behavior

#  [ ] immutability (if intended)
#  [ ] slots behavior
#  [ ] equality edge cases

# ------------------------------------------------------------
# Constructor tests
# ------------------------------------------------------------

def test_default_settings():
    """Test default RecorderSettings construction."""
    settings = RecorderSettings()

    assert settings.expected_fps > 0
    assert settings.replay_seconds > 0
    assert settings.monitor >= 1


@pytest.mark.parametrize(
    "fps,replay_seconds,monitor",
    VALID_SETTINGS,
)
def test_valid_settings(fps, replay_seconds, monitor):
    """Test valid settings configurations."""
    settings = RecorderSettings(
        expected_fps=fps,
        replay_seconds=replay_seconds,
        monitor=monitor,
    )

    assert settings.expected_fps == fps
    assert settings.replay_seconds == replay_seconds
    assert settings.monitor == monitor


# ------------------------------------------------------------
# Property tests
# ------------------------------------------------------------

def test_num_frames():
    """Test number of frames calculation."""
    settings = RecorderSettings(
        expected_fps=60,
        replay_seconds=5,
    )

    assert settings.num_frames == 300


def test_num_frames_minimum():
    """Test num_frames never returns zero."""
    settings = RecorderSettings(
        expected_fps=1,
        replay_seconds=0.1,
    )

    assert settings.num_frames == 1


# ------------------------------------------------------------
# Replace tests
# ------------------------------------------------------------

def test_replace_returns_new_object():
    """Test replace creates a new settings object."""
    original = RecorderSettings(
        expected_fps=30,
        replay_seconds=5,
        monitor=1,
    )

    updated = original.replace(
        expected_fps=90,
    )

    assert original.expected_fps == 30
    assert updated.expected_fps == 90


def test_replace_keeps_original_values():
    """Test replace only changes requested values."""
    original = RecorderSettings(
        expected_fps=30,
        replay_seconds=5,
        monitor=1,
    )

    updated = original.replace(
        monitor=3,
    )

    assert updated.expected_fps == 30
    assert updated.replay_seconds == 5
    assert updated.monitor == 3


# ------------------------------------------------------------
# Equality tests
# ------------------------------------------------------------

def test_equal_settings():
    """Test settings equality."""
    settings_a = RecorderSettings(
        expected_fps=60,
        replay_seconds=5,
        monitor=1,
    )

    settings_b = RecorderSettings(
        expected_fps=60,
        replay_seconds=5,
        monitor=1,
    )

    assert settings_a == settings_b


def test_not_equal_settings():
    """Test settings inequality."""
    settings_a = RecorderSettings(
        expected_fps=60,
        replay_seconds=5,
        monitor=1,
    )

    settings_b = RecorderSettings(
        expected_fps=90,
        replay_seconds=5,
        monitor=1,
    )

    assert settings_a != settings_b


# ------------------------------------------------------------
# Representation tests
# ------------------------------------------------------------

def test_repr():
    """Test string representation."""
    settings = RecorderSettings(
        expected_fps=60,
        replay_seconds=5,
        monitor=2,
    )

    result = repr(settings)

    assert "fps=60" in result
    assert "replay_seconds=5" in result
    assert "monitor=2" in result


def test_to_dict():
    """Test dictionary conversion."""
    settings = RecorderSettings(
        expected_fps=60,
        replay_seconds=5,
        monitor=2,
    )

    assert settings.to_dict() == {
        "expected_fps": 60,
        "replay_seconds": 5,
        "num_frames": 300,
        "monitor": 2,
    }


# ------------------------------------------------------------
# FPS validation
# ------------------------------------------------------------

@pytest.mark.parametrize(
    "fps",
    INVALID_FPS_VALUES,
)
def test_invalid_fps_values(fps):
    """Test invalid FPS numeric values."""

    fps = fps.values[0] if hasattr(fps, "values") else fps

    with pytest.raises(ex.NonPositiveValue):
        RecorderSettings(expected_fps=fps)



@pytest.mark.parametrize(
    "fps",
    INVALID_FPS_TYPES,
)
def test_invalid_fps_types(fps):
    """Test invalid FPS types."""
    with pytest.raises(ex.InvalidType):
        RecorderSettings(expected_fps=fps)


# ------------------------------------------------------------
# Replay duration validation
# ------------------------------------------------------------

@pytest.mark.parametrize(
    "seconds",
    INVALID_REPLAY_SECONDS_VALUES,
)
def test_invalid_replay_seconds_values(seconds):
    """Test invalid replay duration values."""

    seconds = seconds.values[0] if hasattr(seconds, "values") else seconds

    with pytest.raises(ex.NegativeValue):
        RecorderSettings(
            replay_seconds=seconds,
        )


@pytest.mark.parametrize(
    "seconds",
    INVALID_REPLAY_SECONDS_TYPES,
)
def test_invalid_replay_seconds_types(seconds):
    """Test invalid replay duration types."""
    with pytest.raises(ex.InvalidType):
        RecorderSettings(
            replay_seconds=seconds,
        )


# ------------------------------------------------------------
# Monitor validation
# ------------------------------------------------------------

@pytest.mark.parametrize(
    "monitor",
    INVALID_MONITOR_VALUES,
)
def test_invalid_monitor_values(monitor):
    """Test invalid monitor indexes."""

    monitor = monitor.values[0] if hasattr(monitor, "values") else monitor

    with pytest.raises(ex.InvalidMonitorIndex):
        RecorderSettings(
            monitor=monitor,
        )


@pytest.mark.parametrize(
    "monitor",
    INVALID_MONITOR_TYPES,
)
def test_invalid_monitor_types(monitor):
    """Test invalid monitor types."""
    with pytest.raises(ex.InvalidType):
        RecorderSettings(
            monitor=monitor,
        )