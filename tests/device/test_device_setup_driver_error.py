import pytest
from dependency_injector import containers, providers
from pytest_bdd import scenario, when, then, given

from src.android.drivers.uiautomator2 import UiAutomator2Driver
from src.android.screenshots.droidcast_raw import DroidcastRawScreenshot
from src.android.touches.uiautomator2 import UiAutomator2Touch
from src.core.device import CoreDevice, CoreDeviceDriverError


@scenario(
    feature_name="device.feature",
    scenario_name="Error connecting to Device due to unreachable device",
)
def test_scenario():
    pass


class CoreDeviceContainer(containers.DeclarativeContainer):
    driver = providers.Singleton(UiAutomator2Driver, "127.0.0.1:16969")
    screenshot = providers.Singleton(DroidcastRawScreenshot, driver=driver)
    touch = providers.Singleton(UiAutomator2Touch, driver=driver)
    device = providers.Factory(
        CoreDevice, driver=driver, screenshot=screenshot, touch=touch
    )


@given("I provide the driver, screenshot and touch method", target_fixture="device")
def given1():
    container = CoreDeviceContainer()
    device = container.device()
    yield device
    device.disconnect()


@when("I connect to the device")
def when1(device: CoreDevice):
    with pytest.raises(CoreDeviceDriverError):
        device.connect()


@then("I got an driver error message")
def then1(device: CoreDevice):
    pass
