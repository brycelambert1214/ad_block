"""Provide background storage for acquired frame sequences."""

import queue
import threading
import time
from pathlib import Path

import numpy as np


class _Storage:
    """Store acquired frames using a background worker thread."""

    def __init__(self, directory: str = "data"):
        self._directory = Path(directory+r"\data")
        self._directory.mkdir(parents=True, exist_ok=True)

        self._queue: queue.Queue = queue.Queue()
        self._running = threading.Event()
        self._thread: threading.Thread | None = None

        self._start_time = 0.0

    def start(self) -> None:
        """Start the storage worker thread."""
        if self._running.is_set():
            return

        self._running.set()
        self._thread = threading.Thread(
            target=self._run,
            daemon=True,
        )
        self._thread.start()

    def stop(self) -> None:
        """Stop the storage worker after pending work is completed."""
        self._running.clear()

        if self._thread is not None:
            self._thread.join()

        self._thread = None

    def store_frames(
        self,
        frames: list[np.ndarray],
        is_start: bool,
    ) -> None:
        """Queue frames to be stored."""
        self._queue.put((frames, is_start))

    def _run(self) -> None:
        """Process queued storage operations."""
        while self._running.is_set() or not self._queue.empty():
            try:
                frames, is_start = self._queue.get(timeout=0.1)
            except queue.Empty:
                continue

            try:
                self._save_frames(frames, is_start)
            finally:
                self._queue.task_done()

    def _save_frames(
        self,
        frames: list[np.ndarray],
        is_start: bool,
    ) -> None:
        """Write a frame sequence to disk."""
        if is_start:
            self._start_time = time.time()
            filename = f"frames_1_{self._start_time:.3f}_start.npy"
        else:
            filename = f"frames_2_{self._start_time:.3f}_end.npy"

        path = self._directory / filename
        np.save(path, np.asarray(frames))
