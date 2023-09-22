from abc import ABC, abstractmethod


class ITouch(ABC):
    """Touch interface"""

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
