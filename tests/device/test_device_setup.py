import time

import numpy as np
from dependency_injector import containers, providers
from pytest_bdd import scenario, when, then, given

from src.android.drivers.uiautomator2 import UiAutomator2Driver
from src.android.screenshots.droidcast_raw import DroidcastRawScreenshot
from src.android.touches.uiautomator2 import UiAutomator2Touch
from src.core.device import CoreDevice


@scenario(
    feature_name="device.feature",
    scenario_name="Connect to Device",
)
def test_scenario():
    pass


@given("The driver is uiautomator2")
@given("Screenshot method is droidcast raw")
@given("Touch method is uiautomator2")
class CoreDeviceContainer(containers.DeclarativeContainer):
    serial_address = providers.Object("127.0.0.1:16448")
    driver = providers.Singleton(UiAutomator2Driver, serial_address)
    screenshot = providers.Singleton(DroidcastRawScreenshot, driver=driver)
    touch = providers.Singleton(UiAutomator2Touch, driver=driver)
    device = providers.Factory(
        CoreDevice, driver=driver, screenshot=screenshot, touch=touch
    )


@given("The device is provided", target_fixture="device")
def given1():
    container = CoreDeviceContainer()
    device = container.device()
    yield device
    device.disconnect()


@when("I connect to the device")
def when1(device: CoreDevice):
    device.connect()


@then("I can take a screenshot")
def then1(device: CoreDevice):
    assert isinstance(device.screenshot.take(), np.ndarray)


@then("I can touch the screen")
def then2(device: CoreDevice):
    time.sleep(1)
    device.touch.tap((100, 100))
    time.sleep(1)
