from typing import Optional, Tuple, Dict

import uiautomator2

from src.interfaces.driver import (
    IDriver,
    auto_recovery,
    DriverState,
    DriverConnectionError,
    DriverCommandError,
    DriverServerError,
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

    @auto_recovery
    def execute(self, command: str) -> Tuple[str, int]:
        if self.device is None:
            raise DriverConnectionError("Device is not connected")
        try:
            output, exit_code = self.device.shell(command)
            output = output.rstrip("\n")
            return output, exit_code
        except RuntimeError as e:
            raise DriverCommandError(e)

    @auto_recovery
    def run_daemon(self, command: str) -> int:
        if self.device is None:
            raise DriverConnectionError("Device is not connected")

        try:
            resp = self.device.http.post("/shell/background", data={"command": command})

            if resp.status_code != 200:
                raise DriverServerError(
                    f"ATX server returned {resp.status_code} for command {command}"
                )
            content: Dict = resp.json()
            pid = content.get("pid")

            # check if response pid is number
            if pid is None:
                raise DriverServerError(
                    f"ATX server returned invalid pid {pid} for command {command}"
                )

            return pid
        except ValueError:
            raise DriverServerError(
                f"ATX server returned invalid json for command {command}"
            )

    @auto_recovery
    def push(self, src: str, dst: str) -> None:
        raise NotImplementedError

    @auto_recovery
    def forward(self, remote: int, local: Optional[int] = None) -> int:
        raise NotImplementedError
