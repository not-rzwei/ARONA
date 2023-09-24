from typing import Optional, Tuple, Dict

import uiautomator2
from adbutils import AdbError

from src.interfaces.driver import (
    IDriver,
    DriverState,
    DriverConnectionError,
    DriverCommandError,
    DriverServerError,
    DriverPushError,
    DriverForwardError,
    DriverResolutionError,
    DriverError,
    DriverDeviceOrientation,
)


class UiAutomator2Driver(IDriver):
    """Driver for UiAutomator2."""

    device: uiautomator2.Device

    def __init__(self, serial: str):
        """

        Args:
            serial (str): Android device serial address
        """
        self.serial = serial

    def connect(self) -> None:
        try:
            self.device = uiautomator2.connect_adb_wifi(self.serial)
            self.device.set_new_command_timeout(30)
            self.state = DriverState.CONNECTED
        except uiautomator2.ConnectError:
            raise DriverConnectionError(f"Failed to connect to {self.serial}")

    # noinspection PyProtectedMember
    def disconnect(self) -> None:
        """Disconnect from the device.
        Cleanup the device by killing the atx-agent and releasing the port.
        """
        try:
            self.state = DriverState.DISCONNECTED
            self.device._adb_device.shell("pkill -f atx-agent")

            atx_url = self.device._get_atx_agent_url()
            port = atx_url.split(":")[-1]
            self.release_port(int(port))
        except (DriverError, AdbError) as e:
            raise DriverConnectionError("Failed to disconnect", e)

    def execute(self, command: str) -> Tuple[str, int]:
        try:
            output, exit_code = self.device.shell(command)
            output = output.rstrip("\n")
            return output, exit_code
        except RuntimeError as e:
            raise DriverCommandError(e)

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

    def push(self, src: str, dst: str):
        try:
            with open(src, "rb") as f:
                self.device.push(f, dst)
        except FileNotFoundError:
            raise FileNotFoundError(f"File {src} not found")
        except IOError:
            raise DriverPushError("Failed to push file")

    # noinspection PyProtectedMember
    def forward(self, remote: int, local: Optional[int] = None) -> int:
        try:
            if local is not None:
                self.device._adb_device.forward(f"tcp:{remote}", f"tcp:{local}")
                return local

            return self.device._adb_device.forward_port(remote)
        except RuntimeError as e:
            raise DriverForwardError(f"Cannot forward port {remote}", e)
        except AdbError as e:
            raise DriverConnectionError("Device is not connected", e)

    # noinspection PyProtectedMember
    def release_port(self, local: int) -> bool:
        try:
            self.device._adb_device.open_transport(f"killforward:tcp:{local}")
            return True
        except RuntimeError as e:
            raise DriverForwardError(f"Cannot release port {local}", e)
        except AdbError as e:
            raise DriverConnectionError("Cannot release unlisted port", e)

    def get_device_resolution(self, respect_orientation=True) -> Tuple[int, int]:
        resolution = self.device.device_info.get("display", {})
        width = resolution.get("width", 0)
        height = resolution.get("height", 0)

        if width == 0 or height == 0:
            raise DriverResolutionError("Failed to get device resolution")

        if respect_orientation:
            orientation = self.get_device_orientation()
            if orientation.value in (1, 3):
                return height, width

        return width, height

    def get_device_orientation(self) -> DriverDeviceOrientation:
        try:
            orientation, exit_code = self.execute(
                "dumpsys display | grep orientation | awk -F 'orientation=' '{print $2}' | cut -d ',' -f 1"
            )
            if exit_code != 0:
                raise DriverCommandError("Failed to get screen orientation")
            return DriverDeviceOrientation(int(orientation))
        except DriverCommandError:
            raise DriverCommandError("Failed to get screen orientation")
