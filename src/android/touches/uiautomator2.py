from src.adapters.driver import DriverState
from src.adapters.ui_control import UIControlAdapter
from src.android.drivers.uiautomator2 import UIAutomator2


class UiAutomator2TouchAdapter(UIControlAdapter):
    """Touch implementation for UiAutomator2"""

    def __init__(self, driver: UIAutomator2) -> None:
        self.driver = driver

    def setup(self) -> None:
        if self.driver.state == DriverState.DISCONNECTED:
            self.driver.connect()

    def teardown(self) -> None:
        pass

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
