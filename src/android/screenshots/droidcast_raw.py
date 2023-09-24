import numpy
import requests

from src.constants.path import BIN_FOLDER
from src.interfaces.driver import (
    IDriver,
    DriverServerError,
    DriverForwardError,
    DriverResolutionError,
    DriverCommandError,
)
from src.interfaces.screenshot import (
    IScreenshot,
    ScreenshotSetupError,
    ScreenshotTakeError,
    ScreenshotTeardownError,
)


class DroidcastRawScreenshot(IScreenshot):
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

    def setup(self) -> None:
        try:
            self._driver.push(self._apk_path.__str__(), self._android_path)
            self.pid = self._driver.run_daemon(
                f"CLASSPATH={self._android_path} app_process / ink.mol.droidcast_raw.Main --port={self.remote_port}"
            )
            self.local_port = self._driver.forward(self.remote_port)

            self._url = f"http://localhost:{self.local_port}"
            self._session = requests.Session()

            self.resolution = self._driver.get_device_resolution(landscape=True)
        except FileNotFoundError:
            raise ScreenshotSetupError(
                f"APK file does not exist. Make sure you don't delete {self._apk_path}"
            )
        except DriverServerError:
            raise ScreenshotSetupError("Error running droidcast raw server on device")
        except DriverForwardError:
            raise ScreenshotSetupError(
                f"Error forwarding droidcast port {self.remote_port} to {self.local_port}"
            )
        except DriverResolutionError:
            raise ScreenshotSetupError("Error getting device resolution")

    def teardown(self) -> None:
        try:
            _, exit_code = self._driver.execute(f"pkill -P {self.pid}")
            if exit_code == 0:
                self.pid = 0

            if self._driver.release_port(self.local_port):
                self.local_port = 0
        except DriverCommandError:
            raise ScreenshotTeardownError("Error killing droidcast raw server")
        except DriverForwardError:
            raise ScreenshotTeardownError(
                f"Error releasing droidcast port {self.local_port}"
            )

    def take(self) -> numpy.ndarray:
        if self._session is None:
            raise ScreenshotTakeError("Screenshot has not been setup")

        width, height = self.resolution
        res = self._session.get(f"{self._url}/screenshot?width={width}&height={height}")

        if res.status_code != 200:
            raise ScreenshotTakeError("Error taking screenshot")

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
