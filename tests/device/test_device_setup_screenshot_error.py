import pytest
from dependency_injector import containers, providers
from pytest_bdd import scenario, when, then, given

from src.android.drivers.uiautomator2 import UiAutomator2Driver
from src.android.screenshots.droidcast_raw import DroidcastRawScreenshot
from src.android.touches.shell_input import ShellInputTouch
from src.core.device import CoreDevice, CoreDeviceScreenshotError


@scenario(
    feature_name="device.feature",
    scenario_name="Error connecting to Device due to screenshot error",
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


@given("The device is provided", target_fixture="device")
def given1():
    container = CoreDeviceContainer()
    device = container.device()
    device.screenshot._apk_path = "invalid_path"
    yield device
    device.disconnect()


@when("I connect to the device")
def when1(device: CoreDevice):
    with pytest.raises(CoreDeviceScreenshotError):
        device.connect()


@then("I got an screenshot error message")
def then1(device: CoreDevice):
    pass
