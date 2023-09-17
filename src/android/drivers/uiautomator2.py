from typing import Optional, Tuple

import uiautomator2

from src.interfaces.driver import (
    IDriver,
    auto_recovery,
    DriverState,
    DriverConnectionError,
)


class UiAutomator2Driver(IDriver):
    """Driver for UiAutomator2."""

    device: Optional[uiautomator2.Device]

    def __init__(self, u2, serial: str):
        """

        Args:
            u2 (uiautomator2): uiautomator2 package
            serial (str): Android device serial address
        """
        self.u2 = u2
        self.serial = serial

    def connect(self) -> None:
        try:
            self.device = self.u2.connect(self.serial)
            self.state = DriverState.CONNECTED
        except uiautomator2.ConnectError:
            raise DriverConnectionError(f"Failed to connect to {self.serial}")

    def disconnect(self) -> None:
        # TODO: Implement proper disconnect
        self.device = None
        self.state = DriverState.DISCONNECTED

    def reconnect(self) -> None:
        raise NotImplementedError

    @auto_recovery
    def execute(self, command: str) -> Tuple[str, int]:
        raise NotImplementedError

    @auto_recovery
    def run_daemon(self, command: str) -> int:
        raise NotImplementedError

    @auto_recovery
    def push(self, src: str, dst: str) -> None:
        raise NotImplementedError

    @auto_recovery
    def forward(self, remote: int, local: Optional[int] = None) -> int:
        raise NotImplementedError
