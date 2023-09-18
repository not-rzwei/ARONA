from unittest import mock

import uiautomator2
from pytest_bdd import scenario, when, then, given

from src.android.drivers.uiautomator2 import UiAutomator2Driver


@scenario(
    feature_name="uiautomator2.feature",
    scenario_name="Forward remote port to specified local port",
)
def test_scenario():
    pass


# noinspection PyProtectedMember
@given("Driver is already connected to the device", target_fixture="driver")
def given1():
    u2 = mock.Mock(spec=uiautomator2)
    serial = "127.0.0.1:16448"

    driver = UiAutomator2Driver(u2, serial)  # type: ignore
    device = mock.Mock(spec=uiautomator2.Device)
    device._adb_device.forward.return_value = 16969
    driver.device = device

    return driver


@when("I forward a port", target_fixture="result")
def when1(driver: UiAutomator2Driver):
    result = driver.forward(8080, 16969)
    return result


@then("Driver should return a local port")
def then1(result):
    assert result == 16969
