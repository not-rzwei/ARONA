from unittest import mock

from pytest_bdd import scenario, when, then, given

from src.adapters.driver import DriverAdapter
from src.android.screenshots.droidcast_raw import DroidCastRaw


@scenario(
    feature_name="droidcast_raw.feature",
    scenario_name="Set screenshot resolution on setup",
)
def test_scenario():
    pass


@given("Device resolution is 720x1280", target_fixture="screenshot")
def given1():
    driver = mock.Mock(spec=DriverAdapter)
    driver.get_device_resolution.return_value = (1280, 720)

    screenshot = DroidCastRaw(driver)
    return screenshot


@when("I setup the screenshot")
def when1(screenshot: DroidCastRaw):
    screenshot.setup()


@then("Droidcast should set the screenshot resolution to 1280x720")
def then1(screenshot: DroidCastRaw):
    assert screenshot.resolution == (1280, 720)
