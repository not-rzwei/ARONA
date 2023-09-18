from unittest import mock

import uiautomator2
from pytest_bdd import scenario, when, then, given
from requests import Response

from src.android.drivers.uiautomator2 import UiAutomator2Driver
from src.interfaces.driver import DriverServerError


@scenario(
    feature_name="features/uiautomator2.feature",
    scenario_name="Error running a daemon on an Android device because ATX return non 200",
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


@given("ATX agent can't process request")
def atx(driver):
    mock_response = mock.Mock(spec=Response)
    mock_response.status_code = 500
    driver.device.http.post.return_value = mock_response


@when("I run a daemon", target_fixture="result")
def run_daemon(driver: UiAutomator2Driver):
    try:
        driver.run_daemon("sleep 123")
        return False
    except DriverServerError:
        return True


@then("Driver should raise an server error")
def check_exception(result):
    assert result is True
