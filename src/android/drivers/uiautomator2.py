from typing import Optional, Tuple, Dict

import uiautomator2
from adbutils import AdbError

from src.interfaces.driver import (
    IDriver,
    auto_recovery,
    DriverState,
    DriverConnectionError,
    DriverCommandError,
    DriverServerError,
    DriverPushError,
    DriverForwardError,
    DriverResolutionError,
)


class UiAutomator2Driver(IDriver):
    """Driver for UiAutomator2."""

    device: uiautomator2.Device

    def __init__(self, serial: str):
        """

        Args:
            u2 (uiautomator2): uiautomator2 package
            serial (str): Android device serial address
        """
        self.serial = serial

    def connect(self) -> None:
        try:
            self.device = uiautomator2.connect_adb_wifi(self.serial)
            self.state = DriverState.CONNECTED
        except uiautomator2.ConnectError:
            raise DriverConnectionError(f"Failed to connect to {self.serial}")

    def disconnect(self) -> None:
        # TODO: Implement proper disconnect
        self.state = DriverState.DISCONNECTED

    @auto_recovery
    def execute(self, command: str) -> Tuple[str, int]:
        try:
            output, exit_code = self.device.shell(command)
            output = output.rstrip("\n")
            return output, exit_code
        except RuntimeError as e:
            raise DriverCommandError(e)

    @auto_recovery
    def run_daemon(self, command: str) -> int:
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
    def push(self, src: str, dst: str):
        try:
            with open(src, "rb") as f:
                self.device.push(f, dst)
        except FileNotFoundError:
            raise FileNotFoundError(f"File {src} not found")
        except IOError as e:
            raise DriverPushError("Failed to push file")

    # noinspection PyProtectedMember
    @auto_recovery
    def forward(self, remote: int, local: Optional[int] = None) -> int:
        try:
            if local is not None:
                return self.device._adb_device.forward(remote, local)

            return self.device._adb_device.forward_port(remote)
        except RuntimeError as e:
            raise DriverForwardError(f"Cannot forward port {remote}", e)
        except AdbError as e:
            raise DriverConnectionError("Device is not connected", e)

    def get_device_resolution(self, landscape: bool = True) -> Tuple[int, int]:
        resolution = self.device.device_info.get("display", {})
        width = resolution.get("width", 0)
        height = resolution.get("height", 0)

        if width == 0 or height == 0:
            raise DriverResolutionError("Failed to get device resolution")

        if landscape and width < height:
            return height, width

        return width, height
