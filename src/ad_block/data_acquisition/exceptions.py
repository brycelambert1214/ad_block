import logging


class DataAcquisitionError(Exception):
    """Base class for all screen recording exceptions."""


################################################################################
#                           Configuration Error                                #
################################################################################

class StateError(DataAcquisitionError):
    """Base class for all configuration exceptions."""


class AttributeDoesNotExist(StateError, RuntimeError):
    """Unsupported negative value in system configuration."""

    def __init__(self, level: int=logging.ERROR,
                 message: str="Accessed attribute does not exist."):
        self.level = level
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class RecordingInProgress(StateError):
    """Class for all errors caused by current screen recording."""

    def __init__(self, level: int=logging.ERROR,
                 message: str="Recording in progress."):
        self.level = level
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class ConfigurationError(DataAcquisitionError):
    """Base class for all configuration exceptions."""


class  NonPositiveValue(ConfigurationError, AttributeError):
    """Class for expected positive value."""

    def __init__(self, level: int=logging.ERROR,
                    message: str="Expected a positive value."):
        self.level = level
        self.message = message
        super().__init__(message)


class InvalidType(ConfigurationError, TypeError):
    """Invalid type during system configuration"""

    def __init__(self, level: int=logging.ERROR,
                 message: str="Invalid type provided."):
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