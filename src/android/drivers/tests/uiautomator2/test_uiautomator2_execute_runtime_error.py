from unittest import mock

import pytest
import uiautomator2
from pytest_bdd import scenario, when, then, given

from src.adapters.driver import DriverCommandError
from src.android.drivers.uiautomator2 import UIAutomator2


@scenario(
    feature_name="uiautomator2.feature",
    scenario_name="Error executing a shell command on an Android device",
)
def test_scenario():
    pass


@given("Driver is already connected to the device", target_fixture="driver")
def given1(mocker):
    mocker.patch("uiautomator2.connect_adb_wifi")
    serial = "127.0.0.1:16448"

    device = mock.Mock(spec=uiautomator2.Device)
    device.shell.side_effect = DriverCommandError

    dev = UIAutomator2(serial)
    dev.device = device
    return dev


@when("I execute a command")
def when1(driver: UIAutomator2):
    with pytest.raises(DriverCommandError):
        driver.execute("echo hello world")


@then("Driver should raise an error")
def then1():
    pass
