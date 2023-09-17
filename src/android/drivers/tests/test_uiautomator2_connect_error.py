from unittest import mock

import uiautomator2
from pytest_bdd import scenario, when, then, given

from src.android.drivers.uiautomator2 import UiAutomator2Driver
from src.interfaces.driver import DriverConnectionError


@scenario(
    feature_name="features/uiautomator2.feature",
    scenario_name="Cannot establish a connection to an Android device",
)
def test_establishing_a_connection_to_an_android_device():
    pass


@given("Device serial address is unreachable", target_fixture="driver")
def driver():
    u2 = mock.Mock(spec=uiautomator2)
    u2.connect.side_effect = uiautomator2.ConnectError

    serial = "127.0.0.1:6969"
    dev = UiAutomator2Driver(u2, serial)  # type: ignore
    return dev


@when("I connect to the device", target_fixture="driver_connect")
def driver_connect(driver: UiAutomator2Driver):
    try:
        driver.connect()
        return False
    except DriverConnectionError:
        return True


@then("Driver raise an error")
def connected_state(driver_connect):
    assert driver_connect is True
