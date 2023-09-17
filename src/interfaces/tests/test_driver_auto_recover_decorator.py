from unittest import mock

import pytest
from pytest_bdd import given, when, then, scenario

from src.interfaces.driver import (
    IDriver,
    DriverState,
    auto_recovery,
    DriverConnectionError,
    DriverRetryError,
)


@pytest.fixture
def disconnected_driver():
    mock_driver = mock.Mock(spec=IDriver)
    mock_driver.state = DriverState.DISCONNECTED

    return mock_driver


@scenario(
    "features/driver.feature",
    "Auto connect driver if not connected",
)
def test_scenario():
    pass


@given("Driver is not connected to the device", target_fixture="driver")
def driver():
    mock_driver = mock.Mock(spec=IDriver)
    mock_driver.execute.side_effect = [
        DriverConnectionError,
        ("test", 0),
    ]

    mock_driver.reconnect.side_effect = lambda: setattr(
        mock_driver, "state", DriverState.CONNECTED
    )

    return mock_driver


@when("I execute a decorated command with auto connect", target_fixture="result")
def call_decorated_method(driver):
    try:
        return auto_recovery(driver.execute)(driver, "test")
    except DriverRetryError:
        assert False, "DriverRetryError should not be raised"


@then("Driver should be connected to the device")
def driver_connected(driver):
    assert driver.state == DriverState.CONNECTED


@then("I get a result from the command")
def command_result(result):
    assert result == ("test", 0)
