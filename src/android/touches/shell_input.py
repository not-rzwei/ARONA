from src.interfaces.driver import IDriver, DriverState, DriverConnectionError
from src.interfaces.touch import ITouch, TouchSetupError


class ShellInputTouch(ITouch):
    def __init__(self, driver: IDriver):
        self.driver = driver

    def setup(self) -> None:
        try:
            if self.driver.state == DriverState.DISCONNECTED:
                self.driver.connect()
        except DriverConnectionError as e:
            raise TouchSetupError(e)

    def tap(self, point: tuple[int, int]) -> None:
        self.driver.execute(f"input tap {point[0]} {point[1]}")

    def swipe(
        self, start_point: tuple[int, int], end_point: tuple[int, int], duration: float
    ) -> None:
        self.driver.execute(
            f"input swipe {start_point[0]} {start_point[1]} {end_point[0]} {end_point[1]} {duration}"
        )

    def teardown(self) -> None:
        pass
