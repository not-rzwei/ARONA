from unittest import mock

import pytest
import uiautomator2
from pytest_bdd import scenario, when, then, given

from src.adapters.driver import DriverDeviceOrientation
from src.android.drivers.uiautomator2 import UIAutomator2


@scenario(
    feature_name="uiautomator2.feature",
    scenario_name="Get device resolution in landscape mode",
)
def test_scenario():
    pass


@pytest.fixture
def driver(mocker):
    mocker.patch("uiautomator2.connect_adb_wifi")
    serial = "127.0.0.1:16448"

    dev = UIAutomator2(serial)
    return dev


@given("Device resolution is 720x1280")
def given1(driver):
    device = mock.MagicMock(spec=uiautomator2.Device)
    mock_resolution = {
        "width": 1280,
        "height": 720,
    }
    device.device_info.get.return_value = mock_resolution

    driver.device = device


@given("Device is in landscape mode")
def given2(driver):
    orientation = mock.MagicMock(spec=DriverDeviceOrientation)
    orientation.value = 1
    driver.get_device_orientation = orientation


@when("I get device resolution in landscape", target_fixture="result")
def when1(driver: UIAutomator2):
    return driver.get_device_resolution()


@then("Driver should return a resolution of 1280x720")
def then1(result):
    assert result == (1280, 720)
