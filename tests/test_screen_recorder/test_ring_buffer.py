import numpy as np
import pytest

from ad_block.screen_recorder.ring_buffer import RingBuffer
from ad_block.screen_recorder import exceptions as ex

from test_screen_recorder.screen_recorder_data import (
    VALID_BUFFER_CAPACITIES,
    INVALID_BUFFER_CAPACITY_VALUES,
    INVALID_BUFFER_CAPACITY_TYPES,
)

# TODO: Finish the following checklist of tests.
#
# Constructor
#  [x] constructor
#  [x] valid capacity values
#
# Validation
#  [x] invalid capacity values
#  [x] invalid capacity types
#
# Properties
#  [x] capacity property
#  [ ] size property
#  [ ] read-only property behavior
#
# Frame Operations
#  [x] add
#  [x] latest
#  [x] latest empty
#  [x] snapshot
#  [x] len
#  [x] clear
#
# Buffer Management
#  [x] resize larger capacity
#  [x] resize smaller capacity
#  [ ] overwrite behavior when capacity is exceeded
#
# Thread Safety
#  [ ] thread safety with concurrent writers
#  [ ] thread safety with concurrent readers/writers
#
# Internal Behavior
#  [x] lock exists during operations
#  [ ] verify locking prevents race conditions


# ------------------------------------------------------------
# Constructor tests
# ------------------------------------------------------------

def test_constructor():
    """Test RingBuffer construction."""

    buffer = RingBuffer()
    buffer.resize(5)

    assert buffer._capacity == 5
    assert len(buffer) == 0


@pytest.mark.parametrize(
    "capacity",
    VALID_BUFFER_CAPACITIES,
)
def test_valid_capacity(capacity):
    """Test valid buffer capacities."""

    buffer = RingBuffer()
    buffer.resize(capacity)

    assert buffer._capacity == capacity


# ------------------------------------------------------------
# Add tests
# ------------------------------------------------------------

def test_add():
    """Test adding a frame."""

    buffer = RingBuffer()
    buffer.resize(5)

    frame = np.zeros((5, 5))

    buffer.add(frame)

    assert len(buffer) == 1
    assert buffer.latest() is frame


# ------------------------------------------------------------
# Latest tests
# ------------------------------------------------------------

def test_latest():
    """Test latest returns newest frame."""

    buffer = RingBuffer()
    buffer.resize(2)

    frame1 = np.zeros((2, 2))
    frame2 = np.ones((2, 2))

    buffer.add(frame1)
    buffer.add(frame2)

    assert buffer.latest() is frame2


def test_latest_empty():
    """Test latest on empty buffer."""

    buffer = RingBuffer()
    buffer.resize(5)

    assert buffer.latest() is None


# ------------------------------------------------------------
# Snapshot tests
# ------------------------------------------------------------

def test_snapshot():
    """Test snapshot returns current frames."""

    buffer = RingBuffer()
    buffer.resize(5)

    frame1 = np.zeros((2, 2))
    frame2 = np.ones((2, 2))

    buffer.add(frame1)
    buffer.add(frame2)

    snapshot = buffer.snapshot()

    assert len(snapshot) == 2
    assert np.array_equal(snapshot[0], frame1)
    assert np.array_equal(snapshot[1], frame2)


# ------------------------------------------------------------
# Length tests
# ------------------------------------------------------------

def test_len():
    """Test length of buffer."""

    buffer = RingBuffer()
    buffer.resize(5)

    buffer.add(np.zeros((1, 1)))
    buffer.add(np.zeros((1, 1)))

    assert len(buffer) == 2


# ------------------------------------------------------------
# Clear tests
# ------------------------------------------------------------

def test_clear():
    """Test clearing all frames."""

    buffer = RingBuffer()
    buffer.resize(5)

    buffer.add(np.zeros((1, 1)))
    buffer.add(np.zeros((1, 1)))

    buffer.clear()

    assert len(buffer) == 0
    assert buffer.latest() is None


# ------------------------------------------------------------
# Resize tests
# ------------------------------------------------------------

def test_resize_grow():
    """Test increasing buffer capacity."""

    buffer = RingBuffer()
    buffer.resize(3)

    buffer.resize(10)

    assert buffer._capacity == 10


def test_resize_shrink():
    """Test shrinking buffer preserves newest frames."""

    buffer = RingBuffer()
    buffer.resize(5)

    frames = [np.array([i]) for i in range(5)]

    for frame in frames:
        buffer.add(frame)

    buffer.resize(3)

    result = buffer.snapshot()

    assert len(result) == 3

    for actual, expected in zip(result, frames[-3:]):
        assert np.array_equal(actual, expected)


# ------------------------------------------------------------
# Capacity validation
# ------------------------------------------------------------

@pytest.mark.parametrize(
    "capacity",
    INVALID_BUFFER_CAPACITY_VALUES,
)
def test_invalid_capacity_values(capacity):
    """Test invalid capacity values."""

    capacity = (
        capacity.values[0]
        if hasattr(capacity, "values")
        else capacity
    )
    print(capacity)

    with pytest.raises(ex.NegativeValue):
        buffer = RingBuffer()
        buffer.resize(capacity)


@pytest.mark.parametrize(
    "capacity",
    INVALID_BUFFER_CAPACITY_TYPES,
)
def test_invalid_capacity_types(capacity):
    """Test invalid capacity types."""

    with pytest.raises(ex.InvalidType):
        buffer = RingBuffer()
        buffer.resize(capacity)