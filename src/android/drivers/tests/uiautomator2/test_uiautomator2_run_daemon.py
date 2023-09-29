from unittest import mock

import uiautomator2
from pytest_bdd import scenario, when, then, given
from requests import Response

from src.android.drivers.uiautomator2 import UIAutomator2


@scenario(
    feature_name="uiautomator2.feature",
    scenario_name="Run a daemon on an Android device",
)
def test_scenario():
    pass


@given("Driver is already connected to the device", target_fixture="driver")
def given1(mocker):
    mocker.patch("uiautomator2.connect_adb_wifi")
    serial = "127.0.0.1:16448"

    driver = UIAutomator2(serial)
    device = mock.Mock(spec=uiautomator2.Device)
    driver.device = device

    return driver


@given("ATX agent is running on the device")
def given2(driver):
    mock_response = mock.Mock(spec=Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"pid": 123}
    driver.device.http.post.return_value = mock_response


@when("I run a daemon", target_fixture="result")
def when1(driver: UIAutomator2):
    result = driver.run_daemon("sleep 123")
    return result


@then("Driver should return the pid of the daemon")
def then1(result):
    assert result == 123
