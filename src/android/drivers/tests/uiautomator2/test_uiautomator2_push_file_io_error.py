from unittest import mock

import pytest
import uiautomator2
from pytest_bdd import scenario, when, then, given

from src.android.drivers.uiautomator2 import UiAutomator2Driver
from src.interfaces.driver import DriverPushError


@scenario(
    feature_name="uiautomator2.feature",
    scenario_name="Error pushing a file to an Android device because permission denied on device",
)
def test_scenario():
    pass


@given(
    "Driver is already connected to the device",
    target_fixture="driver",
)
def given1(mocker):
    mocker.patch("uiautomator2.connect_adb_wifi")
    serial = "127.0.0.1:16448"

    device = mock.Mock(spec=uiautomator2.Device)
    dev = UiAutomator2Driver(serial)
    dev.device = device
    return dev


@given("Destination path is not writable")
def given2(driver, mocker):
    mocker.patch("builtins.open")
    driver.device.push = mock.Mock(side_effect=IOError)


@when("I push a file")
def when1(driver: UiAutomator2Driver):
    with pytest.raises(DriverPushError):
        driver.push("a", "b")


@then("Driver should raise an error")
def then1():
    pass
