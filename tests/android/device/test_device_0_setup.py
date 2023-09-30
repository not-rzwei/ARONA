from dependency_injector import containers, providers
from pytest_bdd import scenario, when, then, given

from src.android.device import AndroidDevice
from src.android.drivers.uiautomator2 import UIAutomator2
from src.android.screenshots.droidcast_raw import DroidCastRaw
from src.android.touches.shell_input import ShellInput


@scenario(
    feature_name="device.feature",
    scenario_name="Connect to Device",
)
def test_scenario():
    pass


@given("The driver is uiautomator2")
@given("Screenshot method is droidcast raw")
@given("Touch method is shell input")
class CoreDeviceContainer(containers.DeclarativeContainer):
    serial_address = providers.Object("127.0.0.1:16448")
    driver = providers.Singleton(UIAutomator2, serial_address)
    screenshot = providers.Singleton(DroidCastRaw, driver=driver)
    touch = providers.Singleton(ShellInput, driver=driver)
    device = providers.Factory(
        AndroidDevice, driver=driver, screenshot=screenshot, touch=touch
    )


@given("The device is provided", target_fixture="device")
def given1():
    container = CoreDeviceContainer()
    device = container.device()
    yield device
    device.disconnect()


@when("I connect to the device")
def when1(device: AndroidDevice):
    device.connect()


@then("I can take a screenshot")
def then1(device: AndroidDevice):
    device._screenshot.take()


@then("I can touch the screen")
def then2(device: AndroidDevice):
    device._touch.tap((50, 50))
