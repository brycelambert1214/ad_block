import pytest
from unittest.mock import MagicMock, patch

from ad_block.screen_recorder.capture import CaptureThread
from ad_block.screen_recorder.settings import RecorderSettings
from ad_block.screen_recorder.ring_buffer import RingBuffer
from ad_block.screen_recorder import exceptions as ex


# TODO: Finish the following checklist of tests.
#
# Constructor
# [x] creates CaptureThread with valid buffer and settings
# [x] initializes running state as False
# [x] initializes frame count as zero
# [x] initializes runtime as zero
#
# Properties
# [x] settings getter returns RecorderSettings
# [x] settings setter accepts valid RecorderSettings
# [x] settings setter rejects invalid types
# [x] running returns current thread state
# [x] fps returns zero before recording
# [x] tot_count returns stored frame count
# [x] runtime returns stored runtime
# [x] tot_count raises RecordingInProgress while running
# [x] runtime raises RecordingInProgress while running
#
# Monitor Validation
# [x] validates existing monitor index
# [x] rejects invalid monitor index
# [ ] validates monitor after settings change
#
# Capture Control
# [x] start_capture validates monitor
# [x] start_capture changes running state
# [x] stop_capture clears running state
# [ ] starting capture twice does not create multiple threads
# [ ] stopping capture while inactive behaves correctly
# [ ] restarting capture after stopping works
#
# Capture Loop
# [ ] captures frames from mss
# [ ] converts screenshots into numpy arrays
# [ ] adds frames to RingBuffer
# [ ] counts captured frames
# [ ] calculates runtime correctly
# [ ] clears state after capture exception
#
# Thread Safety
# [ ] multiple start/stop calls are thread safe
# [ ] buffer access remains thread safe during capture
# [ ] capture thread exits cleanly
#
# Future Refactor
# [ ] remove direct dependency on threading.Thread
# [ ] separate capture logic from thread management
# [ ] allow CaptureThread object reuse after stopping
# [ ] support non-monitor capture sources (HDMI, cameras, etc.)# TODO: Finish the following checklist of tests.
#
# Constructor
# [x] creates CaptureThread with valid buffer and settings
# [x] initializes running state as False
# [x] initializes frame count as zero
# [x] initializes runtime as zero
#
# Properties
# [x] settings getter returns RecorderSettings
# [x] settings setter accepts valid RecorderSettings
# [x] settings setter rejects invalid types
# [x] running returns current thread state
# [x] fps returns zero before recording
# [x] tot_count returns stored frame count
# [x] runtime returns stored runtime
# [x] tot_count raises RecordingInProgress while running
# [x] runtime raises RecordingInProgress while running
#
# Monitor Validation
# [x] validates existing monitor index
# [x] rejects invalid monitor index
# [ ] validates monitor after settings change
#
# Capture Control
# [x] start_capture validates monitor
# [x] start_capture changes running state
# [x] stop_capture clears running state
# [ ] starting capture twice does not create multiple threads
# [ ] stopping capture while inactive behaves correctly
# [ ] restarting capture after stopping works
#
# Capture Loop
# [ ] captures frames from mss
# [ ] converts screenshots into numpy arrays
# [ ] adds frames to RingBuffer
# [ ] counts captured frames
# [ ] calculates runtime correctly
# [ ] clears state after capture exception
#
# Thread Safety
# [ ] multiple start/stop calls are thread safe
# [ ] buffer access remains thread safe during capture
# [ ] capture thread exits cleanly
#
# Future Refactor
# [ ] remove direct dependency on threading.Thread
# [ ] separate capture logic from thread management
# [ ] allow CaptureThread object reuse after stopping
# [ ] support non-monitor capture sources (HDMI, cameras, etc.)

# ------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------

@pytest.fixture
def settings():
    """Default recorder settings."""

    return RecorderSettings(
        expected_fps=30,
        replay_seconds=1,
        monitor=1,
    )


@pytest.fixture
def buffer():
    """Test ring buffer."""

    return RingBuffer(30)


@pytest.fixture
def capture(buffer, settings):
    """CaptureThread instance."""

    return CaptureThread(buffer, settings)


# ------------------------------------------------------------
# Constructor tests
# ------------------------------------------------------------

def test_constructor(capture, buffer, settings):
    """Test CaptureThread initialization."""

    assert capture.buffer is buffer
    assert capture.settings == settings
    assert capture.running is False
    assert capture.tot_count == 0
    assert capture.runtime == 0.0


# ------------------------------------------------------------
# Property tests
# ------------------------------------------------------------

def test_settings_property(capture, settings):
    """Test settings getter."""

    assert capture.settings == settings


def test_settings_setter():
    """Test settings validation."""

    capture = CaptureThread(
        RingBuffer(10),
        RecorderSettings()
    )

    new_settings = RecorderSettings(expected_fps=60)

    capture.settings = new_settings

    assert capture.settings == new_settings


@pytest.mark.parametrize(
    "value",
    [
        None,
        1,
        "settings",
        [],
        {},
    ],
)
def test_invalid_settings(value):
    """Test invalid settings types."""

    capture = CaptureThread(
        RingBuffer(10),
        RecorderSettings()
    )

    with pytest.raises(ex.InvalidType):
        capture.settings = value


def test_running_property(capture):
    """Test running state."""

    assert capture.running is False


def test_fps_before_recording(capture):
    """FPS should return zero before recording."""

    assert capture.fps == 0.0


# ------------------------------------------------------------
# Runtime statistics tests
# ------------------------------------------------------------

def test_tot_count_not_running(capture):
    """Test total count getter."""

    capture._tot_count = 100

    assert capture.tot_count == 100


def test_runtime_not_running(capture):
    """Test runtime getter."""

    capture._runtime = 5.0

    assert capture.runtime == 5.0


def test_tot_count_while_running(capture):
    """Cannot access count during capture."""

    capture._running.set()

    with pytest.raises(ex.RecordingInProgress):
        capture.tot_count


def test_runtime_while_running(capture):
    """Cannot access runtime during capture."""

    capture._running.set()

    with pytest.raises(ex.RecordingInProgress):
        capture.runtime


# ------------------------------------------------------------
# Monitor validation tests
# ------------------------------------------------------------

@patch("ad_block.screen_recorder.capture.mss.MSS")
def test_validate_monitor(mock_mss, capture):
    """Test valid monitor selection."""

    mock_context = MagicMock()

    mock_context.monitors = [
        None,
        {"top": 0, "left": 0},
    ]

    mock_mss.return_value.__enter__.return_value = mock_context

    capture._validate_monitor()

    assert capture._monitor == mock_context.monitors[1]


@patch("ad_block.screen_recorder.capture.mss.MSS")
def test_invalid_monitor(mock_mss, capture):
    """Test invalid monitor index."""

    mock_context = MagicMock()

    mock_context.monitors = [
        None,
    ]

    mock_mss.return_value.__enter__.return_value = mock_context

    with pytest.raises(ex.InvalidMonitorIndex):
        capture._validate_monitor()


# ------------------------------------------------------------
# Start / stop tests
# ------------------------------------------------------------

@patch.object(CaptureThread, "_validate_monitor")
def test_start_capture(mock_validate, capture):
    """Test starting capture."""

    capture.start_capture()

    mock_validate.assert_called_once()

    assert capture.running is True

    capture.stop_capture()


def test_stop_capture(capture):
    """Test stopping capture."""

    capture.stop_capture()

    assert capture.running is False


# ------------------------------------------------------------
# Buffer interaction tests
# ------------------------------------------------------------

def test_buffer_connection(capture):
    """Test buffer is connected."""

    assert len(capture.buffer) == 0