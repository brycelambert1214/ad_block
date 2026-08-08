# TODO: Update the module level doc string
"""
This file is in charge of maintaining the buffered information.

Description
-----------
This module provides a thread-safe ring buffer implementation for storing frames
captured during screen recording. The RingBuffer class allows for adding frames,
retrieving the latest frame, taking snapshots of the current frames, and resizing
the buffer while preserving the most recent frames. It ensures that access to the
buffer is synchronized across multiple threads, preventing data corruption and
ensuring consistent behavior.

Classes
-------
RingBuffer
    A thread-safe ring buffer for storing captured frames.

Dependencies
------------
collections.deque
    Efficient fixed-capacity FIFO container for frame storage.

threading
    Synchronization primitives used to provide thread-safe access.

ad_block.screen_recorder.exceptions
    Package-specific exceptions used for input validation.

Examples
--------
>>> from ad_block.screen_recorder.ring_buffer import RingBuffer
>>> import numpy as np

>>> buffer = RingBuffer(capacity=10)
>>> # Assume this is a captured frame (e.g., a numpy array)
>>> frame = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
>>> buffer.add(frame)  # Add a frame to the buffer
>>> latest_frame = buffer.latest()  # Get the most recent frame
>>> snapshot = buffer.snapshot()  # Get a list of all current frames
>>> buffer.resize(20)  # Change the capacity of the buffer to 20
>>> print(len(buffer))  # Get the number of frames currently stored
>>> buffer.clear()  # Clear all frames from the buffer
>>> print(len(buffer))  # Get the number of frames currently stored (should be 0)
"""
from collections import deque
import threading
from . import exceptions as ex
import numpy as np


class RingBuffer:
    # TODO: Update the class level doc string
    """
    Keeps track of the current and recent screens.
    
    Attributes
    ----------
    capacity : int
        Maximum number of frames the buffer can hold.
    size : int
        Current number of frames stored in the buffer.

    Methods
    -------
    __init__(capacity: int)
        Initialize the ring buffer with a specified capacity.
    __len__() -> int
        Return the number of frames currently stored in the buffer.
    resize(capacity: int) -> None
        Change the capacity of the buffer while preserving the most recent frames.
    clear() -> None
        Remove all stored frames from the buffer.
    add(frame) -> None
        Add a frame to the buffer.
    snapshot() -> list[np.ndarray]
        Return a list of all current frames in the buffer.
    latest() -> np.ndarray
        Return the most recently added frame.
    """

    def __init__(self, capacity: int):
        self._validate_capacity(capacity)

        self._capacity = capacity
        self._lock = threading.Lock()
        self._frames = deque(maxlen=capacity)

    @property
    def capacity(self) -> int:
        """Property for the maximum number of frames in the buffer."""
        return self._capacity

    @property
    def size(self) -> int:
        """Current number of stored frames."""
        with self._lock:
            return len(self._frames)

    def add(self, frame: np.ndarray) -> None:
        """Add a frame to the buffered video."""
        # with the buffer specific thread
        with self._lock:
            self._frames.append(frame)

    def snapshot(self) -> list[np.ndarray]:
        """Return current frames."""
        # using the buffer specific thread return
        with self._lock:
            return list(self._frames)

    def latest(self) -> np.ndarray | None:
        """Return the most recently read frame."""
        # using the buffer specific thread return
        with self._lock:
            if not self._frames:
                return None
            return self._frames[-1]

    def resize(self, capacity: int) -> None:
        """Change capacity while preserving newest frames."""
        self._validate_capacity(capacity)

        with self._lock:
            self._capacity = capacity
            self._frames = deque(self._frames, maxlen=self._capacity)
    
    def clear(self) -> None:
        """Remove all stored frames."""
        with self._lock:
            self._frames.clear()

    def __len__(self) -> int:
        """Length of the recorded frames."""
        with self._lock:
            return len(self._frames)

    @staticmethod
    def _validate_capacity(value: int) -> None:
        """Validate buffer size."""
        if isinstance(value, bool):
            raise ex.InvalidType("Capacity cannot be a boolean.")
        if not isinstance(value, int):
            raise ex.InvalidType("Capacity must be an integer.")
        if value <= 0:
            raise ex.NegativeValue("Capacity must be greater than 0.")