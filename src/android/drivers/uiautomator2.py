import logging
from functools import lru_cache
from typing import Optional, Tuple, Dict

import uiautomator2
from adbutils import AdbError

from src.core.logger import app_logger
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
    DriverReleasePortError,
)
from src.utils.error_message import ErrorMessage

# Disable uiautomator2 logger as it is too verbose
uiautomator2.logger.disabled = True
logging.getLogger("logzero").disabled = True


class Error(ErrorMessage):
    CONNECT_ERROR = "Failed to connect to {}"
    DISCONNECT_ERROR = "Failed to disconnect"
    PUSH_ERROR = "Failed to push file"
    FORWARD_ERROR = "Failed to forward port {}"
    RELEASE_PORT_ERROR = "Failed to release port {}"
    RESOLUTION_ERROR = "Failed to get device resolution"
    ORIENTATION_ERROR = "Failed to get device orientation"

    ATX_SERVER_ERROR = "ATX server returned {} for command {}"
    FILE_NOT_FOUND = "File {} not found"


class UiAutomator2Driver(IDriver):
    """Driver for UiAutomator2."""

    logger = app_logger(name="UIAUTOMATOR2")
    device: uiautomator2.Device

    def __init__(self, serial: str):
        """

        Args:
            serial (str): Android device serial address
        """
        self.serial = serial

    @logger.catch(DriverConnectionError, reraise=True, level="DEBUG")
    def connect(self) -> None:
        try:
            self.logger.debug(f"Connecting to {self.serial}")
            self.device = uiautomator2.connect(self.serial)
            self.device.set_new_command_timeout(30)
            self.state = DriverState.CONNECTED
        except (uiautomator2.ConnectError, RuntimeError) as e:
            raise DriverConnectionError(Error.CONNECT_ERROR.fmt(self.serial), str(e))

    # noinspection PyProtectedMember
    @logger.catch(DriverConnectionError, reraise=True, level="DEBUG")
    def disconnect(self) -> None:
        """Disconnect from the device.
        Cleanup the device by killing the atx-agent and releasing the port.
        """
        try:
            self.logger.debug("Killing atx-agent")
            self.device._adb_device.shell("pkill -f atx-agent")
            self.state = DriverState.DISCONNECTED

            self.logger.debug("Releasing port")
            atx_url = self.device._get_atx_agent_url()
            port = atx_url.split(":")[-1]
            self.release_port(int(port))
        except (DriverError, AdbError) as e:
            raise DriverConnectionError(Error.DISCONNECT_ERROR, str(e))

    @logger.catch(DriverCommandError, reraise=True, level="DEBUG")
    def execute(self, command: str) -> Tuple[str, int]:
        try:
            self.logger.debug(f"Executing command: {command}")
            output, exit_code = self.device.shell(command)
            output = output.rstrip("\n")
            self.logger.debug(f"Command exit code: {exit_code}. Output: {output}")
            return output, exit_code
        except RuntimeError as e:
            raise DriverCommandError(e)

    @logger.catch(DriverServerError, reraise=True, level="DEBUG")
    def run_daemon(self, command: str) -> int:
        try:
            self.logger.debug(f"Running daemon: {command}")
            resp = self.device.http.post("/shell/background", data={"command": command})

            if resp.status_code != 200:
                raise DriverServerError(
                    Error.ATX_SERVER_ERROR.fmt(resp.status_code, command)
                )
            content: Dict = resp.json()
            pid = content.get("pid")

            # check if response pid is number
            if pid is None:
                raise DriverServerError(
                    Error.ATX_SERVER_ERROR.fmt("invalid pid", command)
                )

            return pid
        except ValueError:
            raise DriverServerError(
                Error.ATX_SERVER_ERROR.fmt("invalid response", command)
            )

    @logger.catch(DriverPushError, reraise=True, level="DEBUG")
    def push(self, src: str, dst: str):
        try:
            self.logger.debug(f"Opening file {src}")
            with open(src, "rb") as f:
                self.logger.debug(f"Pushing file {src} to {dst}")
                self.device.push(f, dst)
        except FileNotFoundError:
            raise DriverPushError(Error.FILE_NOT_FOUND.fmt(src))
        except IOError as e:
            raise DriverPushError(Error.PUSH_ERROR.fmt(src, dst), str(e))

    # noinspection PyProtectedMember
    @logger.catch(DriverForwardError, reraise=True, level="DEBUG")
    def forward(self, remote: int, local: Optional[int] = None) -> int:
        try:
            if local is not None:
                self.logger.debug(f"Forwarding port {remote} to {local}")
                self.device._adb_device.forward(f"tcp:{remote}", f"tcp:{local}")
                return local

            self.logger.debug(f"Forwarding port {remote}")
            return self.device._adb_device.forward_port(remote)
        except (RuntimeError, AdbError) as e:
            raise DriverForwardError(Error.FORWARD_ERROR.fmt(remote), str(e))

    # noinspection PyProtectedMember
    @logger.catch(DriverReleasePortError, reraise=True, level="DEBUG")
    def release_port(self, local: int) -> bool:
        try:
            self.logger.debug(f"Releasing port {local}")
            self.device._adb_device.open_transport(f"killforward:tcp:{local}")
            return True
        except (RuntimeError, AdbError) as e:
            raise DriverReleasePortError(Error.RELEASE_PORT_ERROR.fmt(local), str(e))

    @lru_cache(maxsize=1)
    @logger.catch(DriverResolutionError, reraise=True, level="DEBUG")
    def get_device_resolution(self) -> Tuple[int, int]:
        resolution = self.device.device_info.get("display", {})
        width = resolution.get("width", 0)
        height = resolution.get("height", 0)
        self.logger.debug(f"Raw device resolution: {width}x{height}")

        if width == 0 or height == 0:
            raise DriverResolutionError(Error.RESOLUTION_ERROR)

        orientation = self.get_device_orientation()
        if orientation.value in (1, 3):
            self.logger.debug(
                f"Device resolution after {orientation} rotation: {height}x{width}"
            )
            return height, width

        return width, height

    @lru_cache(maxsize=1)
    @logger.catch(DriverCommandError, reraise=True, level="DEBUG")
    def get_device_orientation(self) -> DriverDeviceOrientation:
        try:
            self.logger.debug(f"Getting device orientation")
            orientation, exit_code = self.execute(
                "dumpsys display | grep orientation | awk -F 'orientation=' '{print $2}' | cut -d ',' -f 1"
            )
            if exit_code != 0:
                raise DriverCommandError(Error.ORIENTATION_ERROR)
            return DriverDeviceOrientation(int(orientation))
        except DriverCommandError:
            raise DriverCommandError(Error.ORIENTATION_ERROR)
