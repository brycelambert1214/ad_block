"""
Method for easy navigation of screen recording stats.

Classes
-------
CaptureStats:
    Class for all screen recording stats.
"""

from dataclasses import dataclass

@dataclass
class CaptureStats:
    """
    Class for representing all capture stats.

    Methods
    -------
    __str__():
        Return a string with the information of capture stats.

    Examples
    --------
    >>> from ad_block.screen_recorder import CaptureStats
    >>> stats = CaptureStats(total_frames=tot_frames,
    >>>                      duration=time_of_capture, status = "system_status")
    >>> print(stats)
    >>> # output:
    >>> # CaptureStats: system_status
    >>> #     Total Number of Frames:: tot_frames
    >>> #     Duration::               time_of_capture
    >>> #     Average fps::            tot_frames / time_of_capture
    """
    total_frames: int = 0
    duration: float = 0.0
    status: str | None = None

    @property
    def fps(self):
        """Return the measured fps."""
        if self.duration == 0:
            return 0
        return self.total_frames / self.duration

    def __str__(self):
        return (f"Capture Stats: {self.status}\n"
                f"\tTotal Number of Frames:: {self.total_frames:>5}\n"
                f"\tDuration::               {self.duration:>7.3f}\n"
                f"\tAverage fps::            {self.fps:>8.3f}")