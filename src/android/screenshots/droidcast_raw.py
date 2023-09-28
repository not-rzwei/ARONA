import numpy
import requests

from src.constants.path import BIN_FOLDER
from src.interfaces.driver import (
    IDriver,
    DriverServerError,
    DriverForwardError,
    DriverResolutionError,
    DriverCommandError,
    DriverPushError,
)
from src.interfaces.screenshot import (
    IScreenshot,
    ScreenshotSetupError,
    ScreenshotTakeError,
    ScreenshotTeardownError,
)
from src.utils.error_message import ErrorMessage
from src.utils.logger import app_logger


class Error(ErrorMessage):
    APK_NOT_FOUND = "APK file not found. Make sure the {} file exists"
    SERVER_ERROR = "Error running droidcast raw server on device"
    FORWARD_ERROR = "Error forwarding droidcast port {} to {}"
    RESOLUTION_ERROR = "Error getting device resolution"
    DROIDCAST_KILL_ERROR = "Error killing droidcast raw server"
    RELEASE_PORT_ERROR = "Error releasing droidcast port {}"

    SCREENSHOT_NOT_SETUP = "Screenshot has not been setup"
    SCREENSHOT_ERROR_CODE = "Error taking screenshot. Error code: {}"


class DroidcastRawScreenshot(IScreenshot):
    logger = app_logger(name="DROIDCAST_RAW")

    def __init__(self, driver: IDriver):
        self._driver = driver

    _apk_path = BIN_FOLDER / "droidcast_raw/droidcast_raw.apk"
    _android_path = "/data/local/tmp/droidcast_raw.apk"

    _url = ""
    _session = None

    resolution = (0, 0)
    pid = 0
    local_port = 0
    remote_port = 16969

    @logger.catch(exception=ScreenshotSetupError, reraise=True, level="DEBUG")
    def setup(self) -> None:
        try:
            self.logger.debug("Pushing droidcast raw apk to device")
            self._driver.push(self._apk_path.__str__(), self._android_path)

            self.logger.debug("Killing existing droidcast raw server")
            self._driver.execute("pkill -f ink.mol.droidcast_raw.Main")

            self.logger.debug("Running droidcast raw server on device")
            self.pid = self._driver.run_daemon(
                f"CLASSPATH={self._android_path} app_process / ink.mol.droidcast_raw.Main --port={self.remote_port}"
            )

            self.logger.debug("Forwarding droidcast raw port")
            self.local_port = self._driver.forward(self.remote_port)
            self._url = f"http://localhost:{self.local_port}"
            self._session = requests.Session()

            self.logger.debug("Getting device resolution")
            self.resolution = self._driver.get_device_resolution()
        except DriverPushError as e:
            raise ScreenshotSetupError(e)
        except DriverServerError:
            raise ScreenshotSetupError(Error.SERVER_ERROR)
        except DriverForwardError:
            raise ScreenshotSetupError(
                Error.FORWARD_ERROR.fmt(self.remote_port, self.local_port)
            )
        except DriverResolutionError:
            raise ScreenshotSetupError(Error.RESOLUTION_ERROR)

    @logger.catch(exception=ScreenshotTeardownError, reraise=True, level="DEBUG")
    def teardown(self) -> None:
        if self.pid == 0 or self.local_port == 0:
            self.logger.debug("Skipping teardown. Droidcast raw server not running")
            return

        try:
            self.logger.debug("Killing droidcast raw server")
            _, exit_code = self._driver.execute(f"pkill -P {self.pid}")
            if exit_code == 0:
                self.pid = 0

            self.logger.debug("Releasing droidcast port")
            if self._driver.release_port(self.local_port):
                self.local_port = 0
        except DriverCommandError:
            raise ScreenshotTeardownError(Error.DROIDCAST_KILL_ERROR)
        except DriverForwardError:
            raise ScreenshotTeardownError(Error.RELEASE_PORT_ERROR.fmt(self.local_port))

    @logger.catch(exception=ScreenshotTakeError, reraise=True, level="DEBUG")
    def take(self) -> numpy.ndarray:
        if self._session is None:
            raise ScreenshotTakeError(Error.SCREENSHOT_NOT_SETUP)

        self.logger.debug(f"Device resolution is {self.resolution}")
        width, height = self.resolution

        self.logger.debug(f"Taking screenshot from {self._url}")
        res = self._session.get(f"{self._url}/screenshot?width={width}&height={height}")

        if res.status_code != 200:
            raise ScreenshotTakeError(Error.SCREENSHOT_ERROR_CODE.fmt(res.status_code))

        image = numpy.frombuffer(res.content, dtype=numpy.uint16)
        image = image.reshape((width, height))
        return self._bitmap_byte_array_to_rgb565(image)

    def _bitmap_byte_array_to_rgb565(self, image: numpy.ndarray) -> numpy.ndarray:
        """Converts a bitmap byte array to a RGB565 numpy array
        No idea how this works, but it works, so don't touch it
        """
        blue_channel = (image & 0x1F) << 3
        green_channel = ((image >> 5) & 0x3F) << 2
        red_channel = ((image >> 11) & 0x1F) << 3

        return numpy.dstack((red_channel, green_channel, blue_channel))
