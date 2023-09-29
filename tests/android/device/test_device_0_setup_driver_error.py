import pytest
from dependency_injector import containers, providers
from pytest_bdd import scenario, when, then, given

from src.android.device import AndroidDevice, AndroidDeviceDriverError
from src.android.drivers.uiautomator2 import UiAutomator2Driver
from src.android.screenshots.droidcast_raw import DroidcastRawScreenshot
from src.android.touches.shell_input import ShellInputTouch


@scenario(
    feature_name="device.feature",
    scenario_name="Error connecting to Device due to unreachable device",
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
        AndroidDevice, driver=driver, screenshot=screenshot, touch=touch
    )


@given("The device serial address is invalid", target_fixture="device")
def given1():
    container = CoreDeviceContainer()
    container.serial_address.override(providers.Object("127.0.0.1:6969"))

    device = container.device()
    yield device
    device.disconnect()


@when("I connect to the device")
def when1(device: AndroidDevice):
    with pytest.raises(AndroidDeviceDriverError):
        device.connect()


@then("I got an driver error message")
def then1(device: AndroidDevice):
    pass
