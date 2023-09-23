from pytest_bdd import scenario, when, then, given

from src.android.drivers.uiautomator2 import UiAutomator2Driver
from src.interfaces.driver import DriverState


@scenario(
    feature_name="uiautomator2.feature",
    scenario_name="Establishing a connection to an Android device",
)
def test_scenario():
    pass


@given("I have an Android device serial address", target_fixture="driver")
def given1(mocker):
    serial = "127.0.0.1:16448"
    dev = UiAutomator2Driver(serial)
    mocker.patch("uiautomator2.connect_adb_wifi")
    return dev


@when("I connect to the device")
def when1(driver: UiAutomator2Driver):
    driver.connect()


@then("Driver state should be connected")
def then1(driver: UiAutomator2Driver):
    assert driver.state == DriverState.CONNECTED


@then("Device property should be set")
def device_property(driver: UiAutomator2Driver):
    assert driver.device is not None
