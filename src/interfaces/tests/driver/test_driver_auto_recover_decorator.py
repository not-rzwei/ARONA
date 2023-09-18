from unittest import mock

from pytest_bdd import given, when, then, scenario

from src.interfaces.driver import (
    IDriver,
    DriverState,
    auto_recovery,
    DriverConnectionError,
    DriverRetryError,
)


@scenario(
    "driver.feature",
    "Auto recover driver if not connected",
)
def test_scenario():
    pass


@given("Driver is not connected to the device", target_fixture="driver")
def given1():
    mock_driver = mock.Mock(spec=IDriver)
    mock_driver.execute.side_effect = [
        DriverConnectionError,
        ("test", 0),
    ]

    mock_driver.connect.side_effect = lambda: setattr(
        mock_driver, "state", DriverState.CONNECTED
    )

    return mock_driver


@when("I execute a decorated command with auto recover", target_fixture="result")
def when1(driver):
    try:
        return auto_recovery(driver.execute)(driver, "test")
    except DriverRetryError:
        assert False, "DriverRetryError should not be raised"


@then("Driver should be connected to the device")
def then1(driver):
    assert driver.state == DriverState.CONNECTED


@then("I get a result from the command")
def then2(result):
    assert result == ("test", 0)
