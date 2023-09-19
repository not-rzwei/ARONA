from abc import ABC, abstractmethod

import numpy


class ScreenshotError(Exception):
    pass


class ScreenshotSetupError(Exception):
    pass


class IScreenshot(ABC):
    """Screenshot interface"""

    @abstractmethod
    def setup(self) -> None:
        """Setup something for the screenshot to work"""
        raise NotImplementedError

    @abstractmethod
    def take(self) -> numpy.ndarray:
        """Take a screenshot and return it as a numpy array"""
        raise NotImplementedError
