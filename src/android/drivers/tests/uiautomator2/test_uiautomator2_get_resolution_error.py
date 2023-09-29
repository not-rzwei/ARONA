from unittest import mock

import pytest
import uiautomator2
from pytest_bdd import scenario, when, then, given

from src.adapters.driver import DriverResolutionError
from src.android.drivers.uiautomator2 import UIAutomator2


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

    dev = UIAutomator2(serial)
    return dev


@given("Driver is glitchy")
def given1(mocker, driver):
    device = mock.MagicMock(spec=uiautomator2.Device)
    mock_resolution = {}
    device.device_info.get.return_value = mock_resolution

    driver.device = device


@when("I get device resolution", target_fixture="result")
def when1(driver: UIAutomator2):
    with pytest.raises(DriverResolutionError):
        driver.get_device_resolution()


@then("Driver should raise an error")
def then1(result):
    pass
