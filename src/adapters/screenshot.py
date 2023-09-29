from abc import ABC, abstractmethod

import numpy


class ScreenshotError(Exception):
    pass


class ScreenshotSetupError(ScreenshotError):
    pass


class ScreenshotTakeError(ScreenshotError):
    pass


class ScreenshotTeardownError(ScreenshotError):
    pass


class ScreenshotAdapter(ABC):
    """Screenshot interface"""

    @abstractmethod
    def setup(self) -> None:
        """Setup something for the screenshot to work"""
        raise NotImplementedError

    @abstractmethod
    def take(self) -> numpy.ndarray:
        """Take a screenshot and return it as a numpy array"""
        raise NotImplementedError

    @abstractmethod
    def teardown(self) -> None:
        """Teardown the setup"""
        raise NotImplementedError
