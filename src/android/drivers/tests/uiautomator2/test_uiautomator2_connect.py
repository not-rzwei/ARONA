from pytest_bdd import scenario, when, then, given

from src.adapters.driver import DriverState
from src.android.drivers.uiautomator2 import UIAutomator2


@scenario(
    feature_name="uiautomator2.feature",
    scenario_name="Establishing a connection to an Android device",
)
def test_scenario():
    pass


@given("I have an Android device serial address", target_fixture="driver")
def given1(mocker):
    serial = "127.0.0.1:16448"
    dev = UIAutomator2(serial)
    mocker.patch("src.android.drivers.uiautomator2.uiautomator2")
    return dev


@when("I connect to the device")
def when1(driver: UIAutomator2):
    driver.connect()


@then("Driver state should be connected")
def then1(driver: UIAutomator2):
    assert driver.state == DriverState.CONNECTED


@then("Device property should be set")
def device_property(driver: UIAutomator2):
    assert driver.device is not None
