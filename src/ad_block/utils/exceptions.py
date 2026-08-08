"""File for all custom exeptions in the project."""
import logging

class InvalidType(AttributeError):
    """Class for invalid type."""

    def __init__(self, level: int = logging.ERROR,
                  message:str = "InvalidType"):
        self.level = level
        self.message = message

    def __str__(self):
        return self.message

class DualityState(AttributeError):
    """Class for both ads and media being in the same state."""

    def __init__(self, level: int=logging.ERROR,
                 message: str="DualityState"):
        self.level = level
        self.message = message

    def __str__(self):
        return self.message

class NegativeValue(ValueError):
    """Class for any invalid negative value."""

    def __init__(self, level: int=logging.ERROR,
                 message: str="NegativeValue"):
        self.level = level
        self.message = message

    def __str__(self):
        return self.message