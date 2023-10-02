import numpy.typing as npt
from pytest_bdd import scenario, when, then, given

from src.android.device import AndroidDevice


@scenario(
    feature_name="device.feature",
    scenario_name="Take screenshot in landscape mode",
)
def test_scenario():
    pass


@given("The device is connected", target_fixture="device")
def given1(container):
    device = container.device()
    device.connect()
    yield device
    device.disconnect()


@when("I take a screenshot", target_fixture="result")
def when1(device: AndroidDevice):
    return device.screenshot()


@then("I got a screenshot")
@then("The resolution is match the device resolution in landscape mode")
def then2(device: AndroidDevice, result: npt.NDArray):
    device_resolution = device._driver.get_device_resolution()
    ss_height, ss_width, _ = result.shape

    assert (ss_width, ss_height) == device_resolution
