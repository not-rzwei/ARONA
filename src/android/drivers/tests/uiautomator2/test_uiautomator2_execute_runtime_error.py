from unittest import mock

import uiautomator2
from pytest_bdd import scenario, when, then, given

from src.android.drivers.uiautomator2 import UiAutomator2Driver
from src.interfaces.driver import DriverCommandError


@scenario(
    feature_name="uiautomator2.feature",
    scenario_name="Error executing a shell command on an Android device",
)
def test_scenario():
    pass


@given("Driver is already connected to the device", target_fixture="driver")
def given1():
    u2 = mock.Mock(spec=uiautomator2)
    serial = "127.0.0.1:16448"

    device = mock.Mock(spec=uiautomator2.Device)
    device.shell.side_effect = DriverCommandError

    dev = UiAutomator2Driver(u2, serial)  # type: ignore
    dev.device = device
    return dev


@when("I execute a command", target_fixture="is_error")
def when1(driver: UiAutomator2Driver):
    try:
        driver.execute("echo hello world")
        return False
    except DriverCommandError:
        return True


@then("Driver should raise an error")
def then1(is_error):
    assert is_error is True
