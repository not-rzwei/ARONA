from src.interfaces.driver import IDriver
from src.interfaces.screenshot import IScreenshot
from src.interfaces.touch import ITouch


class CoreDevice:
    def __init__(self, driver: IDriver, screenshot: IScreenshot, touch: ITouch):
        self.driver = driver
        self.screenshot = screenshot
        self.touch = touch

    def setup(self):
        try:
            self.driver.connect()
            self.screenshot.setup()
            self.touch.setup()
        except:
            raise

    def teardown(self):
        self.touch.teardown()
        self.screenshot.teardown()
        self.driver.disconnect()
