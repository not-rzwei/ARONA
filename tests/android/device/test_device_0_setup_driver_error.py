import pytest
from dependency_injector import providers
from pytest_bdd import scenario, when, then, given

from src.android.device import AndroidDevice, AndroidDeviceDriverError


@scenario(
    feature_name="device.feature",
    scenario_name="Error connecting to Device due to unreachable device",
)
def test_scenario():
    pass


@given("The device serial address is invalid", target_fixture="device")
def given1(container):
    container.serial_address.override(providers.Object("127.0.0.1:6969"))

    device = container.device()
    yield device
    device.disconnect()


@when("I connect to the device")
def when1(device: AndroidDevice):
    with pytest.raises(AndroidDeviceDriverError):
        device.connect()


@then("I got an driver error message")
def then1(device: AndroidDevice):
    pass
