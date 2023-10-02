import pytest
from pytest_bdd import scenario, when, then, given

from src.android.device import AndroidDevice, AndroidDeviceScreenshotError


@scenario(
    feature_name="device.feature",
    scenario_name="Error connecting to Device due to screenshot error",
)
def test_scenario():
    pass


# noinspection PyProtectedMember
@given("The device is provided", target_fixture="device")
def given1(container):
    device = container.device()
    device._screenshot._apk_path = "invalid_path"
    yield device
    device.disconnect()


@when("I connect to the device")
def when1(device: AndroidDevice):
    with pytest.raises(AndroidDeviceScreenshotError):
        device.connect()


@then("I got an screenshot error message")
def then1(device: AndroidDevice):
    pass
