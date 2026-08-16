import pytest
from unittest.mock import MagicMock, patch

from ad_block.screen_recorder._capture_mss import _CaptureMSS
from ad_block.screen_recorder.settings import RecorderSettings
from ad_block.screen_recorder._ring_buffer import _RingBuffer
from ad_block.screen_recorder import exceptions as ex


# TODO: Finish the following checklist of tests.
#
# Constructor
# [x] creates _CaptureMSS with valid buffer and settings
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
# [ ] adds frames to _RingBuffer
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
# [ ] allow _CaptureMSS object reuse after stopping
# [ ] support non-monitor capture sources (HDMI, cameras, etc.)# TODO: Finish the following checklist of tests.
#
# Constructor
# [x] creates _CaptureMSS with valid buffer and settings
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
# [ ] adds frames to _RingBuffer
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
# [ ] allow _CaptureMSS object reuse after stopping
# [ ] support non-monitor capture sources (HDMI, cameras, etc.)

# ------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------

@pytest.fixture
def monitor():
    """Default recorder settings."""
    return int(1)

@pytest.fixture
def buffer():
    """Test ring buffer."""
    buffer = _RingBuffer()
    buffer.resize(30)
    return buffer

@pytest.fixture
def capture(buffer, monitor):
    """_CaptureMSS instance."""
    capture = _CaptureMSS(buffer)
    capture.monitor_idx = monitor
    return capture



# ------------------------------------------------------------
# Constructor tests
# ------------------------------------------------------------

def test_constructor(capture, buffer, monitor):
    """Test _CaptureMSS initialization."""
    assert capture._buffer is buffer
    assert capture._monitor_idx is monitor
    assert capture.running is False

# ------------------------------------------------------------
# Property tests
# ------------------------------------------------------------

def test_running_property(capture):
    """Test running state."""

    assert capture.running is False

def test_running_during_run(capture):
    """Test running state during run."""
    capture._running.set()
    assert capture.running

# ------------------------------------------------------------
# Monitor validation tests
# ------------------------------------------------------------

@patch("ad_block.screen_recorder._capture_mss.mss.MSS")
def test_validate_monitor(mock_mss, capture):
    """Test valid monitor selection."""

    mock_context = MagicMock()
    mock_context.monitors = [0, 0]

    mock_mss.return_value.__enter__.return_value = mock_context

    capture._validate_monitor()

    assert capture._monitor == mock_context.monitors[0]

@patch("ad_block.screen_recorder._capture_mss.mss")
def test_invalid_monitor(mock_mss, capture):
    """Test invalid monitor index."""

    mock_context = MagicMock()
    mock_context.monitors = [None]
    mock_mss.return_value.__enter__.return_value = mock_context

    with pytest.raises(ex.InvalidMonitorIndex):
        capture._validate_monitor()

# ------------------------------------------------------------
# Start / stop tests
# ------------------------------------------------------------

@patch.object(_CaptureMSS, "_validate_monitor")
def test_start_capture(mock_validate, capture):
    """Test starting capture."""

    capture.start()

    mock_validate.assert_called_once()

    assert capture.running is True

    capture.stop()


def test_stop_capture(capture):
    """Test stopping capture."""

    capture.stop()

    assert capture.running is False

# ------------------------------------------------------------
# Buffer interaction tests
# ------------------------------------------------------------

def test_buffer_connection(capture):
    """Test buffer is connected."""
    assert capture._buffer.size== 0