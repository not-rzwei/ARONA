from src.interfaces.driver import IDriver, DriverError
from src.interfaces.screenshot import IScreenshot
from src.interfaces.touch import ITouch


class CoreDeviceError(Exception):
    pass


class CoreDeviceDriverError(CoreDeviceError):
    pass


class CoreDevice:
    def __init__(self, driver: IDriver, screenshot: IScreenshot, touch: ITouch):
        self.driver = driver
        self.screenshot = screenshot
        self.touch = touch

    def connect(self):
        try:
            self.driver.connect()
            self.screenshot.setup()
            self.touch.setup()
        except DriverError as e:
            raise CoreDeviceDriverError(e)

    def disconnect(self):
        try:
            self.touch.teardown()
            self.screenshot.teardown()
            self.driver.disconnect()
        except:
            pass
