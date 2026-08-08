"""This file is used to determine the current state of the media."""
from ad_block import exceptions as ex
from ad_block import current_frame as cf

class State():
    """Class for tracking the system state information."""

    def __init__(self):
        self._ads_current = False
        self._media_current = False

    @property
    def current(self):
        """Property for tracking the current state."""
        if self.ads_current and self.media_current:
            raise ex.DualityState()
        if not self.ads_current and not self.media_current:
            raise ex.DualityState()
        if self.ads_current:
            return "ads"
        if self.media_current:
            return "media"

    @property
    def ads_current(self):
        """Property for tracking ads."""
        if not isinstance(self._ads_current, bool):
            raise ex.InvalidType()
        return self._ads_current

    @ads_current.setter
    def ads_current(self, value):
        if not isinstance(value, bool):
            raise ex.InvalidType()
        self.ads_current = value

    @property
    def media_current(self):
        """Property for tracking ads."""
        if not isinstance(self._media_current, bool):
            raise ex.InvalidType()
        return self._media_current

    @media_current.setter
    def media_current(self, value):
        if not isinstance(value, bool):
            raise ex.InvalidType()
        self.media_current = value


class InputData():
    """Class for handling the current input."""

    def __init__(self):
        self.state = State()
        self.frame = cf.Frame()
        self.input_type = None

    @property
    def current_frame(self):
        self.frame.frame


def main():
    current = State.current