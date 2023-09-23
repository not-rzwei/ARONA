from unittest import mock

import pytest
import uiautomator2
from pytest_bdd import scenario, when, then, given

from src.android.drivers.uiautomator2 import UiAutomator2Driver
from src.interfaces.driver import DriverResolutionError


@scenario(
    feature_name="uiautomator2.feature",
    scenario_name="Error getting device resolution",
)
def test_scenario():
    pass


@pytest.fixture
def driver(mocker):
    mocker.patch("uiautomator2.connect_adb_wifi")
    serial = "127.0.0.1:16448"

    dev = UiAutomator2Driver(serial)
    return dev


@given("Driver is glitchy")
def given1(mocker, driver):
    device = mock.MagicMock(spec=uiautomator2.Device)
    mock_resolution = {}
    device.device_info.get.return_value = mock_resolution

    driver.device = device


@when("I get device resolution", target_fixture="result")
def when1(driver: UiAutomator2Driver):
    with pytest.raises(DriverResolutionError):
        driver.get_device_resolution()


@then("Driver should raise an error")
def then1(result):
    pass
