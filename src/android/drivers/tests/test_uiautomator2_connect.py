from unittest import mock

import uiautomator2
from pytest_bdd import scenario, when, then, given

from src.android.drivers.uiautomator2 import UiAutomator2Driver
from src.interfaces.driver import DriverState


@scenario(
    feature_name="../features/uiautomator2.feature",
    scenario_name="Establishing a connection to an Android device",
)
def test_establishing_a_connection_to_an_android_device():
    pass


@given("I have an Android device serial address", target_fixture="driver")
def driver():
    u2 = mock.Mock(name="uiautomator2", spec=uiautomator2)
    serial = "127.0.0.1:16448"
    dev = UiAutomator2Driver(u2, serial)  # type: ignore
    return dev


@when("I connect to the device")
def driver_connect(driver: UiAutomator2Driver):
    driver.connect()


@then("Driver state should be connected")
def connected_state(driver: UiAutomator2Driver):
    assert driver.state == DriverState.CONNECTED


@then("Device property should be set")
def device_property(driver: UiAutomator2Driver):
    assert driver.device is not None
