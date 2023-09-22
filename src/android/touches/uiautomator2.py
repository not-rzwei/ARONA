from src.android.drivers.uiautomator2 import UiAutomator2Driver
from src.interfaces.touch import ITouch


class UiAutomator2Touch(ITouch):
    """Touch implementation for UiAutomator2"""

    def __init__(self, driver: UiAutomator2Driver) -> None:
        self.driver = driver

    def tap(self, point: tuple[int, int]) -> None:
        self.driver.device.click(point[0], point[1])

    def swipe(
        self,
        start_point: tuple[int, int],
        end_point: tuple[int, int],
        duration: float = 0.5,
    ) -> None:
        self.driver.device.swipe(
            start_point[0],
            start_point[1],
            end_point[0],
            end_point[1],
            duration=duration,
        )
