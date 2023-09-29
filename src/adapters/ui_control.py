from abc import ABC, abstractmethod


class UIControlError(Exception):
    pass


class UIControlSetupError(UIControlError):
    pass


class UIControlTapError(UIControlError):
    pass


class UIControlSwipeError(UIControlError):
    pass


class UIControlAdapter(ABC):
    """Touch interface"""

    @abstractmethod
    def setup(self) -> None:
        """Setup something for the touch to work"""
        raise NotImplementedError

    @abstractmethod
    def tap(self, point: tuple[int, int]) -> None:
        """Tap a point on the screen"""
        raise NotImplementedError

    @abstractmethod
    def swipe(
        self,
        start_point: tuple[int, int],
        end_point: tuple[int, int],
        duration: float,
    ) -> None:
        """Swipe from one point to another"""
        raise NotImplementedError

    @abstractmethod
    def teardown(self) -> None:
        """Teardown the setup"""
        raise NotImplementedError
