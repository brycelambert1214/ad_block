"""
Module for all screen_recorder custom exceptions.

Descriptions
------------
This module defines the exception hierarchy used throughout the
screen recorder package. Each exception belongs to one of three categories:
 configuration errors, state errors, or capture errors.

Hierarchy
---------
ScreenRecordingError
    - ConfigurationError
        - NegativeValue
        - InvalidType
        - InvalidMonitorIndex
    - StateError
        - RecordingInProgress
    - CaptureError
    

General Attributes
------------------
- message: Human-readable description of the error.
- level: Suggested logging level associated with the exception.

Examples
--------
>>> from ad_block.screen_recorder import exceptions as ex

>>> try:
>>>     raise ex.NegativeValue(message="Test the negative value error.")
>>> except ex.ScreenRecordingError as err:
>>>     print(err.level)  # output: 40
>>>     print(err)  # output: 'Test the negative value error.'

>>> try:
>>>     raise ex.NegativeValue(message="Test the negative value error.")
>>> except ex.Configuration as err:
>>>     print(err.level)  # output: 40
>>>     print(err)  # output: 'Test the negative value error.'

>>> try:
>>>     raise ex.NegativeValue(message="Test the negative value error.")
>>> except ValueError as err:
>>>     print(err.level)  # output: 40
>>>     print(err)  # output: 'Test the negative value error.'
"""
import logging
import warnings


class ScreenRecordingError(Exception):
    """Base class for all screen recording exceptions."""


################################################################################
#                           Configuration Error                                #
################################################################################

class ConfigurationError(ScreenRecordingError):
    """Base class for all configuration exceptions."""


class NegativeValue(ConfigurationError, ValueError):
    """Unsupported negative value in system configuration."""

    def __init__(self, level: int=logging.ERROR,
                 message: str="Negative values are not allowed."):
        self.level = level
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message

class InvalidType(ConfigurationError, TypeError):
    """Invalid type during system configuration"""

    def __init__(self, level: int=logging.ERROR,
                 message: str="Invalid type provided."):
        self.level = level
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message

class InvalidMonitorIndex(ConfigurationError, IndexError):
    """Unrecognized monitor in system configuration."""

    def __init__(self, level: int=logging.ERROR,
                 message: str="Invalid monitor index provided."):
        self.level = level
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class InvalidAttributeSetting(ConfigurationError, AttributeError):
    """Class for all invalid attribute stting"""

    def __init__(self, level: int=logging.ERROR,
                     message: str="Invalid setting of attribute."):
            self.level = level
            self.message = message
            super().__init__(message)
    
    def __str__(self):
        return self.message


class  OutofFramesPerSecondRange(ConfigurationError, AttributeError):
    """Class for too high of an excpeted frames per second."""

    def __init__(self, level: int=logging.ERROR,
                    message: str="Invalid expected frames per second."):
        self.level = level
        self.message = message
        super().__init__(message)


class  NonPositiveValue(ConfigurationError, AttributeError):
    """Class for expected positive value."""

    def __init__(self, level: int=logging.ERROR,
                    message: str="Expected a positive value."):
        self.level = level
        self.message = message
        super().__init__(message)

################################################################################
#                              Runtime Error                                   #
################################################################################

class StateError(ScreenRecordingError):
    """Base class for all runtime exceptions."""


class RecordingInProgress(StateError):
    """Class for all errors caused by current screen recording."""

    def __init__(self, level: int=logging.ERROR,
                 message: str="Recording in progress."):
        self.level = level
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class CaptureError(ScreenRecordingError):
    """Base class for all capture based exceptions."""

################################################################################
#                                Warnings                                      #
################################################################################


class ScreenRecordingWarning(Warning):
    """Base warning for screen recording package."""


class ConfigurationWarning(ScreenRecordingWarning):
    """Base warning for all configuration Warnings."""


class StateWarning(ScreenRecordingWarning):
    """Base warning for all state warnings."""

class CaptureWarning(ScreenRecordingWarning):
    """Base class for all capture based warnings."""