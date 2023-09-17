from unittest import mock

import uiautomator2
from pytest_bdd import scenario, when, then, given

from src.android.drivers.uiautomator2 import UiAutomator2Driver
from src.interfaces.driver import DriverRetryError


@scenario(
    feature_name="features/uiautomator2.feature",
    scenario_name="Cannot establish a connection to an Android device",
)
def test_establishing_a_connection_to_an_android_device():
    pass


@given("I have an Android device serial address", target_fixture="driver")
def driver():
    u2 = mock.Mock(spec=uiautomator2)
    u2.connect = mock.Mock(
        side_effect=[
            uiautomator2.ConnectError,
            uiautomator2.ConnectError,
            uiautomator2.ConnectError,
        ],
    )

    serial = "127.0.0.1:16448"
    dev = UiAutomator2Driver(u2, serial)  # type: ignore
    return dev


@when("Driver connect to the device 3 times", target_fixture="driver_connect")
def driver_connect(driver: UiAutomator2Driver):
    try:
        driver.connect()
        return False
    except DriverRetryError:
        return True


@then("Driver raise an error after reaching max retries")
def connected_state(driver_connect):
    assert driver_connect is True
