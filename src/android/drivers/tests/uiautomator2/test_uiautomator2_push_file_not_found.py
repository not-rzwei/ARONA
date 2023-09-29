from unittest import mock

import pytest
import uiautomator2
from pytest_bdd import scenario, when, then, given

from src.adapters.driver import DriverPushError
from src.android.drivers.uiautomator2 import UIAutomator2


@scenario(
    feature_name="uiautomator2.feature",
    scenario_name="Error pushing a file to an Android device because file not found",
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
    dev = UIAutomator2(serial)
    dev.device = device
    return dev


@given("File to push is not found")
def given2(driver, mocker):
    mocker.patch("builtins.open", side_effect=FileNotFoundError)
    driver.device.push = mock.Mock()


@when("I push a file")
def when1(driver: UIAutomator2):
    with pytest.raises(DriverPushError):
        driver.push("a", "b")


@then("Driver should raise an error")
def then1():
    pass
