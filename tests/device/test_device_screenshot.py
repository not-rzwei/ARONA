import numpy as np
from dependency_injector import containers, providers
from pytest_bdd import scenario, when, then, given

from src.android.drivers.uiautomator2 import UiAutomator2Driver
from src.android.screenshots.droidcast_raw import DroidcastRawScreenshot
from src.android.touches.shell_input import ShellInputTouch
from src.core.device import CoreDevice


@scenario(
    feature_name="device.feature",
    scenario_name="Take screenshot in landscape mode",
)
def test_scenario():
    pass


@given("The driver is uiautomator2")
@given("Screenshot method is droidcast raw")
@given("Touch method is shell input")
class CoreDeviceContainer(containers.DeclarativeContainer):
    serial_address = providers.Object("127.0.0.1:16448")
    driver = providers.Singleton(UiAutomator2Driver, serial_address)
    screenshot = providers.Singleton(DroidcastRawScreenshot, driver=driver)
    touch = providers.Singleton(ShellInputTouch, driver=driver)
    device = providers.Factory(
        CoreDevice, driver=driver, screenshot=screenshot, touch=touch
    )


@given("The device is connected", target_fixture="device")
def given1():
    container = CoreDeviceContainer()
    device = container.device()
    device.connect()
    yield device
    device.disconnect()


@when("I take a screenshot", target_fixture="result")
def when1(device: CoreDevice):
    return device.screenshot()


@then("I got a screenshot")
def then1(device: CoreDevice, result: np.ndarray):
    assert isinstance(result, np.ndarray)


@then("The resolution is match the device resolution in landscape mode")
def then2(device: CoreDevice, result: np.ndarray):
    device_resolution = device._driver.get_device_resolution()
    ss_height, ss_width, _ = result.shape

    assert (ss_width, ss_height) == device_resolution
