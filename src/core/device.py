import numpy as np

from src.interfaces.driver import IDriver, DriverError, DriverDeviceOrientation
from src.interfaces.screenshot import IScreenshot, ScreenshotError
from src.interfaces.touch import ITouch, TouchError


class CoreDeviceError(Exception):
    pass


class CoreDeviceDriverError(CoreDeviceError):
    pass


class CoreDeviceScreenshotError(CoreDeviceError):
    pass


class CoreDeviceTouchError(CoreDeviceError):
    pass


class CoreDevice:
    def __init__(self, driver: IDriver, screenshot: IScreenshot, touch: ITouch):
        self._driver = driver
        self._screenshot = screenshot
        self._touch = touch

    def connect(self):
        try:
            self._driver.connect()
            self._screenshot.setup()
            self._touch.setup()
        except DriverError as e:
            raise CoreDeviceDriverError(e)
        except ScreenshotError as e:
            raise CoreDeviceScreenshotError(e)
        except TouchError as e:
            raise CoreDeviceTouchError(e)

    def disconnect(self):
        try:
            self._touch.teardown()
            self._screenshot.teardown()
            self._driver.disconnect()
        except:
            pass

    def screenshot(self) -> np.ndarray:
        ss = self._screenshot.take()
        ss_height, ss_width, _ = ss.shape
        ss_orientation = 0 if ss_height > ss_width else 1

        # TODO: Make the target orientation configurable
        target = DriverDeviceOrientation.LANDSCAPE
        device = self._driver.get_device_orientation()

        # Calculate total rotation needed to rotate screenshot to target orientation
        # 1. Rotate screenshot to device orientation
        # 2. Rotate screenshot to target orientation
        image_to_device_rotation = (device.value - ss_orientation) % 4
        device_to_target_rotation = (target.value - device.value) % 4
        total_rotation = (image_to_device_rotation + device_to_target_rotation) % 4

        return np.rot90(ss, total_rotation * -1)
