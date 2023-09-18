from unittest import mock

import uiautomator2
from pytest_bdd import scenario, when, then, given

from src.android.drivers.uiautomator2 import UiAutomator2Driver


@scenario(
    feature_name="uiautomator2.feature",
    scenario_name="Execute a shell command on an Android device",
)
def test_scenario():
    pass


@given("Driver is already connected to the device", target_fixture="driver")
def given1():
    u2 = mock.Mock(spec=uiautomator2)
    serial = "127.0.0.1:16448"

    device = mock.Mock(spec=uiautomator2.Device)
    device.shell.return_value = ("hello world", 0)

    dev = UiAutomator2Driver(u2, serial)  # type: ignore
    dev.device = device
    return dev


@when("I execute a command", target_fixture="result")
def when1(driver: UiAutomator2Driver):
    result = driver.execute("echo hello world")
    return result


@then("Driver should return a response")
def then1(result):
    assert result == ("hello world", 0)
