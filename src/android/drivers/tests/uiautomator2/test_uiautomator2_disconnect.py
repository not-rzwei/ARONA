import unittest.mock as mock

import uiautomator2
from pytest_bdd import scenario, when, then, given

from src.adapters.driver import DriverState
from src.android.drivers.uiautomator2 import UIAutomator2


@scenario(
    feature_name="uiautomator2.feature",
    scenario_name="Disconnecting from an Android device",
)
def test_scenario():
    pass


# noinspection PyProtectedMember
@given("Driver is already connected to the device", target_fixture="driver")
def given1(mocker):
    serial = "127.0.0.1:16448"
    dev = mock.Mock(spec=uiautomator2.Device)
    dev._get_atx_agent_url.return_value = "http://localhost:6969"

    driver = UIAutomator2(serial)
    driver.state = DriverState.CONNECTED
    driver.device = dev
    return driver


@when("I disconnect from the device")
def when1(driver: UIAutomator2):
    driver.disconnect()


@then("Driver state should be disconnected")
def then1(driver: UIAutomator2):
    assert driver.state == DriverState.DISCONNECTED
