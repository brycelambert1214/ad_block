"""
Validated configuration for DataAcquisition.
"""

from ad_block.screen_recorder import RecorderSettings
from . import exceptions as ex


class DataAcquisitionSettings:
    """
    Immutable configuration for DataAcquisition.

    Attributes
    ----------
    recorder : RecorderSettings
        Settings used to configure the screen recorder.
    event_timeout : int | float
        Maximum time to wait for user confirmation of an event.
    """

    __slots__ = ("_recorder", "_event_timeout")

    def __init__(
        self,
        recorder: RecorderSettings | None = None,
        event_timeout: int | float = 5,
    ):
        if recorder is None:
            recorder = RecorderSettings()

        self._validate_recorder(recorder)
        self._validate_event_timeout(event_timeout)

        self._recorder = recorder
        self._event_timeout = event_timeout

    @property
    def recorder(self) -> RecorderSettings:
        """Settings used by the screen recorder."""
        return self._recorder

    @recorder.setter
    def recorder(self, _: RecorderSettings) -> None:
        raise ex.InvalidAttributeSetting(
            "Cannot manually set recorder settings."
        )

    @property
    def event_timeout(self) -> int | float:
        """Maximum time to wait for event confirmation."""
        return self._event_timeout

    @event_timeout.setter
    def event_timeout(self, _: int | float) -> None:
        raise ex.InvalidAttributeSetting(
            "Cannot manually set event timeout."
        )

    def replace(
        self,
        recorder: RecorderSettings | None = None,
        event_timeout: int | float | None = None,
    ) -> "DataAcquisitionSettings":
        """
        Create a new settings object with selected values replaced.

        The original settings object is not modified.
        """
        return DataAcquisitionSettings(
            recorder=self.recorder if recorder is None else recorder,
            event_timeout=(
                self.event_timeout
                if event_timeout is None
                else event_timeout
            ),
        )

    @staticmethod
    def _validate_recorder(value: RecorderSettings) -> None:
        """Validate recorder settings."""
        if not isinstance(value, RecorderSettings):
            raise ex.InvalidType(
                "recorder must be a RecorderSettings object."
            )

    @staticmethod
    def _validate_event_timeout(value: int | float) -> None:
        """Validate event timeout."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ex.InvalidType(
                "event_timeout must be numeric."
            )

        if value <= 0:
            raise ex.NonPositiveValue(
                "event_timeout must be greater than zero."
            )

    def __repr__(self) -> str:
        """Return a string representation of the settings."""
        return (
            f"DataAcquisitionSettings("
            f"recorder={self.recorder!r}, "
            f"event_timeout={self.event_timeout})"
        )

    def __eq__(self, other: object) -> bool:
        """Check equality with another DataAcquisitionSettings object."""
        if not isinstance(other, DataAcquisitionSettings):
            return False

        return (
            self.recorder == other.recorder
            and self.event_timeout == other.event_timeout
        )

    def to_dict(self) -> dict[str, object]:
        """Return a dictionary representation of the settings."""
        return {
            "recorder": self.recorder.to_dict(),
            "event_timeout": self.event_timeout,
        }