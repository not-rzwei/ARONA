from unittest import mock

import pytest
import uiautomator2
from pytest_bdd import scenario, when, then, given

from src.android.drivers.uiautomator2 import UiAutomator2Driver


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

    dev = UiAutomator2Driver(serial)
    return dev


@given("Device resolution is 720x1280")
def given1(mocker, driver):
    device = mock.MagicMock(spec=uiautomator2.Device)
    mock_resolution = {
        "width": 720,
        "height": 1280,
    }
    device.device_info.get.return_value = mock_resolution

    driver.device = device


@when("I get device resolution in landscape", target_fixture="result")
def when1(driver: UiAutomator2Driver):
    return driver.get_device_resolution(landscape=True)


@then("Driver should return a resolution of 1280x720")
def then1(result):
    assert result == (1280, 720)
