import logging
from functools import lru_cache
from typing import Optional, Tuple, Dict

import uiautomator2
from adbutils import AdbError, AdbTimeout

from src.adapters.driver import (
    DriverAdapter,
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
from src.utils.logger import app_logger

# Disable uiautomator2 logger as it is too verbose
uiautomator2.logger.disabled = True
logging.getLogger("logzero").disabled = True
logging.getLogger("uiautomator2").disabled = True
logging.getLogger("uiautomator2.client").disabled = True


class Error(ErrorMessage):
    CONNECT_ERROR = "Failed to connect to {}"
    DISCONNECT_ERROR = "Failed to disconnect"
    NOT_CONNECTED_ERROR = "Driver is not connected"

    PUSH_ERROR = "Failed to push file"
    FORWARD_ERROR = "Failed to forward port {}"
    RELEASE_PORT_ERROR = "Failed to release port {}"
    RESOLUTION_ERROR = "Failed to get device resolution"
    ORIENTATION_ERROR = "Failed to get device orientation"

    ATX_ERROR = "atx-agent returned {} for command {}"
    FILE_NOT_FOUND = "File {} not found"


class UIAutomator2(DriverAdapter):
    """Driver for UiAutomator2."""

    logger = app_logger(name="UIAUTOMATOR2")

    def __init__(self, serial: str):
        """

        Args:
            serial (str): Android device serial address
        """
        self.serial = serial
        self.state = DriverState.DISCONNECTED
        self.device: Optional[uiautomator2.Device] = None

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
        if self.state == DriverState.DISCONNECTED or self.device is None:
            self.logger.debug("Skipping disconnect. Already disconnected")
            return

        try:
            self.logger.debug("Killing atx-agent")
            self.device._adb_device.shell("pkill -f atx-agent")
            self.state = DriverState.DISCONNECTED

            atx_url = self.device._get_atx_agent_url()
            port = atx_url.split(":")[-1]
            self.logger.debug(f"Releasing atx-agent port {port}")
            self.release_port(int(port))
        except (DriverError, AdbError, AdbTimeout) as e:
            raise DriverConnectionError(Error.DISCONNECT_ERROR, str(e))

    @logger.catch(DriverCommandError, reraise=True, level="DEBUG")
    def execute(self, command: str) -> Tuple[str, int]:
        if self.device is None:
            raise DriverConnectionError(Error.NOT_CONNECTED_ERROR)

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
        if self.device is None:
            raise DriverConnectionError(Error.NOT_CONNECTED_ERROR)

        try:
            self.logger.debug(f"Running daemon: {command}")
            resp = self.device.http.post("/shell/background", data={"command": command})

            if resp.status_code != 200:
                raise DriverServerError(Error.ATX_ERROR.fmt(resp.status_code, command))
            content: Dict = resp.json()
            pid: int = content.get("pid", 0)

            # check if response pid is number
            if pid == 0:
                raise DriverServerError(Error.ATX_ERROR.fmt("invalid pid", command))

            return pid
        except ValueError:
            raise DriverServerError(Error.ATX_ERROR.fmt("invalid response", command))

    @logger.catch(DriverPushError, reraise=True, level="DEBUG")
    def push(self, src: str, dst: str):
        if self.device is None:
            raise DriverConnectionError(Error.NOT_CONNECTED_ERROR)

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
        if self.device is None:
            raise DriverConnectionError(Error.NOT_CONNECTED_ERROR)

        try:
            if local is not None:
                self.logger.debug(f"Forwarding port {remote} to {local}")
                self.device._adb_device.forward(f"tcp:{remote}", f"tcp:{local}")
                return local

            self.logger.debug(f"Forwarding port {remote}")
            return self.device._adb_device.forward_port(remote)  # type: ignore
        except (RuntimeError, AdbError) as e:
            raise DriverForwardError(Error.FORWARD_ERROR.fmt(remote), str(e))

    # noinspection PyProtectedMember
    @logger.catch(DriverReleasePortError, reraise=True, level="DEBUG")
    def release_port(self, local: int) -> bool:
        if self.device is None:
            raise DriverConnectionError(Error.NOT_CONNECTED_ERROR)

        try:
            self.logger.debug(f"Releasing port {local}")
            self.device._adb_device.open_transport(f"killforward:tcp:{local}")
            return True
        except (RuntimeError, AdbError) as e:
            raise DriverReleasePortError(Error.RELEASE_PORT_ERROR.fmt(local), str(e))

    @lru_cache(maxsize=1)
    @logger.catch(DriverResolutionError, reraise=True, level="DEBUG")
    def get_device_resolution(self) -> Tuple[int, int]:
        if self.device is None:
            raise DriverConnectionError(Error.NOT_CONNECTED_ERROR)

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
        if self.device is None:
            raise DriverConnectionError(Error.NOT_CONNECTED_ERROR)

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
