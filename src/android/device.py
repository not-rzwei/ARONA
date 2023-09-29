import numpy as np

from src.interfaces.driver import IDriver, DriverError, DriverDeviceOrientation
from src.interfaces.screenshot import IScreenshot, ScreenshotError
from src.interfaces.ui_control import UIControl, UIControlError
from src.utils.logger import app_logger


class AndroidDeviceError(Exception):
    pass


class AndroidDeviceDriverError(AndroidDeviceError):
    pass


class AndroidDeviceScreenshotError(AndroidDeviceError):
    pass


class AndroidDeviceTouchError(AndroidDeviceError):
    pass


class AndroidDevice:
    logger = app_logger(name="DEVICE")
    orientation: DriverDeviceOrientation

    def __init__(self, driver: IDriver, screenshot: IScreenshot, touch: UIControl):
        self._driver = driver
        self._screenshot = screenshot
        self._touch = touch

    def connect(self):
        try:
            self.logger.info(f"Connecting to device")

            self._driver.connect()
            self._screenshot.setup()
            self._touch.setup()

            self.orientation = self._driver.get_device_orientation()
            self.logger.info(f"Device orientation is {self.orientation}")
        except DriverError as e:
            self.logger.error(f"Failed to connect to device")

            raise AndroidDeviceDriverError(e)
        except ScreenshotError as e:
            self.logger.error(f"Failed to setup screenshot method")

            raise AndroidDeviceScreenshotError(e)
        except UIControlError as e:
            self.logger.error(f"Failed to setup touch method")

            raise AndroidDeviceTouchError(e)

    def disconnect(self):
        try:
            self.logger.info(f"Disconnecting from device")

            self._touch.teardown()
            self._screenshot.teardown()
            self._driver.disconnect()
        except:
            self.logger.warning(f"Failed to disconnect")

            pass

    def screenshot(self) -> np.ndarray:
        self.logger.info(f"Taking screenshot")
        ss = self._screenshot.take()
        ss_height, ss_width, _ = ss.shape
        ss_orientation = 0 if ss_height > ss_width else 1

        # TODO: Make the target orientation configurable
        target = DriverDeviceOrientation.LANDSCAPE
        device = self.orientation

        # Calculate total rotation needed to rotate screenshot to target orientation
        # 1. Rotate screenshot to device orientation
        # 2. Rotate screenshot to target orientation
        image_to_device_rotation = (device.value - ss_orientation) % 4
        device_to_target_rotation = (target.value - device.value) % 4
        total_rotation = (image_to_device_rotation + device_to_target_rotation) % 4

        return np.rot90(ss, total_rotation * -1)
