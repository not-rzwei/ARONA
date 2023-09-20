import numpy
import requests

from src.interfaces.driver import (
    IDriver,
    DriverServerError,
    DriverForwardError,
    DriverResolutionError,
)
from src.interfaces.screenshot import IScreenshot, ScreenshotSetupError


class DroidcastRawScreenshot(IScreenshot):
    def __init__(self, driver: IDriver):
        self._driver = driver

    _apk_path = "bin/droidcast_raw/droidcast_raw.apk"
    _android_path = "/data/local/tmp/droidcast_raw.apk"

    _url = ""
    _session = None

    resolution = (0, 0)
    pid = 0
    local_port = 0
    remote_port = 16969

    def setup(self) -> None:
        try:
            self._driver.push(self._apk_path, self._android_path)
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

    def take(self) -> numpy.ndarray:
        return numpy.array([])
