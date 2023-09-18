from unittest import mock

import uiautomator2
from pytest_bdd import scenario, when, then, given
from requests import Response

from src.android.drivers.uiautomator2 import UiAutomator2Driver


@scenario(
    feature_name="features/uiautomator2.feature",
    scenario_name="Run a daemon on an Android device",
)
def test_scenario():
    pass


@given("Driver is already connected to the device", target_fixture="driver")
def driver():
    u2 = mock.Mock(spec=uiautomator2)
    serial = "127.0.0.1:16448"

    driver = UiAutomator2Driver(u2, serial)  # type: ignore
    device = mock.Mock(spec=uiautomator2.Device)
    driver.device = device

    return driver


@given("ATX agent is running on the device")
def atx(driver):
    mock_response = mock.Mock(spec=Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"pid": 123}
    driver.device.http.post.return_value = mock_response


@when("I run a daemon", target_fixture="result")
def run_daemon(driver: UiAutomator2Driver):
    result = driver.run_daemon("sleep 123")
    return result


@then("Driver should return the pid of the daemon")
def check_pid(result):
    assert result == 123
