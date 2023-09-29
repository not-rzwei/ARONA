from src.adapters.driver import (
    DriverAdapter,
    DriverState,
    DriverConnectionError,
    DriverCommandError,
)
from src.adapters.ui_control import (
    UIControlAdapter,
    UIControlSetupError,
    UIControlTapError,
    UIControlSwipeError,
)


class ShellInput(UIControlAdapter):
    def __init__(self, driver: DriverAdapter):
        self.driver = driver

    def setup(self) -> None:
        try:
            if self.driver.state == DriverState.DISCONNECTED:
                self.driver.connect()
        except DriverConnectionError as e:
            raise UIControlSetupError(e)

    def tap(self, point: tuple[int, int]) -> None:
        try:
            output, exit_code = self.driver.execute(f"input tap {point[0]} {point[1]}")
            if exit_code != 0:
                raise UIControlTapError(f"Input tap failed", output)
        except DriverCommandError as e:
            raise UIControlTapError(f"Failed to send input tap {point}", e)

    def swipe(
        self, start_point: tuple[int, int], end_point: tuple[int, int], duration: float
    ) -> None:
        try:
            output, exit_code = self.driver.execute(
                f"input swipe {start_point[0]} {start_point[1]} {end_point[0]} {end_point[1]} {duration}"
            )
            if exit_code != 0:
                raise UIControlSwipeError(f"Input swipe failed", output)
        except DriverCommandError as e:
            raise UIControlSwipeError(
                f"Failed to send input swipe {start_point} -> ${end_point}", e
            )

    def teardown(self) -> None:
        pass
