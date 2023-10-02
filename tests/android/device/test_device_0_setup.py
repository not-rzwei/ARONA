from pytest_bdd import scenario, when, then, given

from src.android.device import AndroidDevice


@scenario(
    feature_name="device.feature",
    scenario_name="Connect to Device",
)
def test_scenario():
    pass


@given("The device is provided", target_fixture="device")
def given1(container):
    device = container.device()
    yield device
    device.disconnect()


@when("I connect to the device")
def when1(device: AndroidDevice):
    device.connect()


@then("I can take a screenshot")
def then1(device: AndroidDevice):
    device._screenshot.take()


@then("I can touch the screen")
def then2(device: AndroidDevice):
    device._touch.tap((50, 50))
