from unittest import mock

import pytest
import uiautomator2
from pytest_bdd import scenario, when, then, given
from requests import Response

from src.adapters.driver import DriverServerError
from src.android.drivers.uiautomator2 import UIAutomator2


@scenario(
    feature_name="uiautomator2.feature",
    scenario_name="Error running a daemon on an Android device because ATX return non 200",
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


@given("ATX agent can't process request")
def given2(driver):
    mock_response = mock.Mock(spec=Response)
    mock_response.status_code = 500
    driver.device.http.post.return_value = mock_response


@when("I run a daemon")
def when1(driver: UIAutomator2):
    with pytest.raises(DriverServerError):
        driver.run_daemon("sleep 123")


@then("Driver should raise an server error")
def then1():
    pass
