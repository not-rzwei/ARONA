from unittest import mock

import uiautomator2
from pytest_bdd import scenario, when, then, given

from src.android.drivers.uiautomator2 import UIAutomator2


@scenario(
    feature_name="uiautomator2.feature",
    scenario_name="Push a file to an Android device",
)
def test_scenario():
    pass


@given("Driver is already connected to the device", target_fixture="driver")
def given1(mocker):
    mocker.patch("uiautomator2.connect_adb_wifi")
    serial = "127.0.0.1:16448"

    device = mock.Mock(spec=uiautomator2.Device)
    device.push.side_effect = mock.Mock()
    mocker.patch("builtins.open")

    dev = UIAutomator2(serial)
    dev.device = device
    return dev


@when("I push a file")
def when1(driver: UIAutomator2):
    driver.push("src", "dst")


@then("Driver should not raise an error")
def then1():
    pass
