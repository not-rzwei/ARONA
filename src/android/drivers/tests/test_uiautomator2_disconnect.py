from unittest import mock

import uiautomator2
from pytest_bdd import scenario, when, then, given

from src.android.drivers.uiautomator2 import UiAutomator2Driver
from src.interfaces.driver import DriverState


@scenario(
    feature_name="features/uiautomator2.feature",
    scenario_name="Disconnecting from an Android device",
)
def test_scenario():
    pass


@given("Driver is already connected to the device", target_fixture="driver")
def driver():
    u2 = mock.Mock(name="uiautomator2", spec=uiautomator2)
    serial = "127.0.0.1:16448"
    dev = UiAutomator2Driver(u2, serial)  # type: ignore
    dev.state = DriverState.CONNECTED
    return dev


@when("I disconnect from the device")
def driver_disconnect(driver: UiAutomator2Driver):
    driver.disconnect()


@then("Driver state should be disconnected")
def connected_state(driver: UiAutomator2Driver):
    assert driver.state == DriverState.DISCONNECTED


@then("Device property should be None")
def device_property(driver: UiAutomator2Driver):
    assert driver.device is None
