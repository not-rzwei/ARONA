from unittest import mock

from pytest_bdd import given, when, then, scenario

from src.interfaces.driver import (
    IDriver,
    auto_recovery,
    DriverConnectionError,
    DriverCommandError,
)


@scenario(
    "features/driver.feature",
    "Abort auto recover if function throw other exception than DeviceNotConnectedException",
)
def test_scenario():
    pass


@given("Driver is already connected to the device", target_fixture="driver")
def driver():
    mock_driver = mock.Mock(spec=IDriver)
    mock_driver.execute.side_effect = [
        DriverConnectionError,
        DriverCommandError,
        DriverConnectionError,
    ]

    return mock_driver


@when("I execute a decorated command with auto recover", target_fixture="result")
def call_decorated_method(driver):
    try:
        return auto_recovery(driver.execute)(driver, "test")
    except Exception as e:
        return e


@then("Driver raise the exception thrown by the function")
def driver_connected(result):
    assert issubclass(type(result), DriverCommandError)


@then("Exit from auto recover")
def exit_auto_recover(driver):
    assert driver.execute.call_count == 2
