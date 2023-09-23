import pytest
import uiautomator2
from pytest_bdd import scenario, when, then, given

from src.android.drivers.uiautomator2 import UiAutomator2Driver
from src.interfaces.driver import DriverConnectionError


@scenario(
    feature_name="uiautomator2.feature",
    scenario_name="Cannot establish a connection to an Android device",
)
def test_scenario():
    pass


@given("Device serial address is unreachable", target_fixture="driver")
def given1(mocker):
    mocker.patch("uiautomator2.connect_adb_wifi", side_effect=uiautomator2.ConnectError)

    serial = "127.0.0.1:6969"
    dev = UiAutomator2Driver(serial)
    return dev


@when("I connect to the device")
def when1(driver: UiAutomator2Driver):
    with pytest.raises(DriverConnectionError):
        driver.connect()


@then("Driver raise an error")
def then1():
    pass
