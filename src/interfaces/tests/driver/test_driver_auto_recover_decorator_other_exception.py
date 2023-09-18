from unittest import mock

import pytest
from pytest_bdd import given, when, then, scenario

from src.interfaces.driver import (
    IDriver,
    auto_recovery,
    DriverConnectionError,
    DriverCommandError,
)


@scenario(
    "driver.feature",
    "Abort auto recover if function throw other exception than DeviceNotConnectedException",
)
def test_scenario():
    pass


@given("Driver is already connected to the device", target_fixture="driver")
def given1():
    mock_driver = mock.Mock(spec=IDriver)
    mock_driver.execute.side_effect = [
        DriverConnectionError,
        DriverCommandError,
        DriverConnectionError,
    ]

    return mock_driver


@when("I execute a decorated command with auto recover", target_fixture="result")
def when1(driver):
    with pytest.raises(Exception) as e:
        auto_recovery(driver.execute)(driver, "test")
        return e


@then("Driver raise the exception thrown by the function")
def then1():
    pass


@then("Exit from auto recover")
def then2(driver):
    assert driver.execute.call_count == 2
