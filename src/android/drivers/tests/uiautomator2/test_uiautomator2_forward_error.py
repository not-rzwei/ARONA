from unittest import mock

import pytest
import uiautomator2
from pytest_bdd import scenario, when, then, given

from src.android.drivers.uiautomator2 import UiAutomator2Driver
from src.interfaces.driver import DriverForwardError


@scenario(
    feature_name="uiautomator2.feature",
    scenario_name="Error forwarding remote port to local port",
)
def test_scenario():
    pass


@given("Driver is already connected to the device", target_fixture="driver")
def given1():
    u2 = mock.Mock(spec=uiautomator2)
    serial = "127.0.0.1:16448"

    driver = UiAutomator2Driver(u2, serial)  # type: ignore
    device = mock.Mock(spec=uiautomator2.Device)
    driver.device = device

    return driver


# noinspection PyProtectedMember
@given("Somehow can't forward port")
def given2(driver):
    driver.device._adb_device.forward_port.side_effect = RuntimeError


@when("I forward a port", target_fixture="result")
def when1(driver: UiAutomator2Driver):
    with pytest.raises(DriverForwardError):
        driver.forward(8080)


@then("Driver should raise an error")
def then1():
    pass
