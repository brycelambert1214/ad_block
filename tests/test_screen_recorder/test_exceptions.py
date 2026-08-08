import logging
import pytest

from ad_block.screen_recorder import exceptions as ex


# TODO: Finish the following checklist of tests.
#
# [x] base exception
# [x] inheritance hierarchy
# [x] default messages
# [x] custom messages
# [x] logging levels
# [x] string representation
# [x] parent exception catching


# ------------------------------------------------------------
# Base exception tests
# ------------------------------------------------------------

def test_screen_recording_error():
    """Test base screen recording exception."""

    error = ex.ScreenRecordingError()

    assert isinstance(error, Exception)


# ------------------------------------------------------------
# Exception hierarchy tests
# ------------------------------------------------------------

@pytest.mark.parametrize(
    "exception",
    [
        ex.NegativeValue,
        ex.InvalidType,
        ex.RecordingInProgress,
        ex.InvalidMonitorIndex,
    ],
)
def test_exception_inherits_screen_recording_error(exception):
    """Test all exceptions inherit ScreenRecordingError."""

    error = exception()

    assert isinstance(error, ex.ScreenRecordingError)


def test_negative_value_inherits_value_error():
    """Test NegativeValue inheritance."""

    error = ex.NegativeValue()

    assert isinstance(error, ValueError)


def test_invalid_monitor_index_inherits_index_error():
    """Test InvalidMonitorIndex inheritance."""

    error = ex.InvalidMonitorIndex()

    assert isinstance(error, IndexError)


def test_invalid_type_inherits_type_error():
    """Test InvalidType inheritance."""

    error = ex.InvalidType()

    assert isinstance(error, TypeError)


# ------------------------------------------------------------
# Default attribute tests
# ------------------------------------------------------------

@pytest.mark.parametrize(
    "exception",
    [
        ex.NegativeValue,
        ex.InvalidType,
        ex.RecordingInProgress,
        ex.InvalidMonitorIndex,
    ],
)
def test_default_level(exception):
    """Test default logging level."""

    error = exception()

    assert error.level == logging.ERROR


@pytest.mark.parametrize(
    "exception",
    [
        ex.NegativeValue,
        ex.InvalidType,
        ex.RecordingInProgress,
        ex.InvalidMonitorIndex,
    ],
)
def test_default_message(exception):
    """Test default messages exist."""

    error = exception()

    assert isinstance(error.message, str)
    assert str(error) == error.message


# ------------------------------------------------------------
# Custom message tests
# ------------------------------------------------------------

@pytest.mark.parametrize(
    "exception",
    [
        ex.NegativeValue,
        ex.InvalidType,
        ex.RecordingInProgress,
        ex.InvalidMonitorIndex,
    ],
)
def test_custom_message(exception):
    """Test custom exception messages."""

    message = "Custom error message."

    error = exception(message=message)

    assert error.message == message
    assert str(error) == message


# ------------------------------------------------------------
# Custom level tests
# ------------------------------------------------------------

@pytest.mark.parametrize(
    "exception",
    [
        ex.NegativeValue,
        ex.InvalidType,
        ex.RecordingInProgress,
        ex.InvalidMonitorIndex,
    ],
)
def test_custom_level(exception):
    """Test custom logging level."""

    error = exception(level=logging.WARNING)

    assert error.level == logging.WARNING


# ------------------------------------------------------------
# Catching tests
# ------------------------------------------------------------

def test_negative_value_catches_value_error():
    """Test NegativeValue catches as ValueError."""

    with pytest.raises(ValueError):
        raise ex.NegativeValue()


def test_invalid_type_catches_type_error():
    """Test InvalidType catches as TypeError."""

    with pytest.raises(TypeError):
        raise ex.InvalidType()


def test_all_errors_catch_base_error():
    """Test all errors catch ScreenRecordingError."""

    errors = [
        ex.NegativeValue(),
        ex.InvalidType(),
        ex.RecordingInProgress(),
        ex.InvalidMonitorIndex(),
    ]

    for error in errors:
        with pytest.raises(ex.ScreenRecordingError):
            raise error