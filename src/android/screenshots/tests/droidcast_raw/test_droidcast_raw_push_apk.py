from unittest import mock

from pytest_bdd import scenario, when, then, given

from src.adapters.driver import DriverAdapter
from src.android.screenshots.droidcast_raw import DroidCastRaw


@scenario(
    feature_name="droidcast_raw.feature",
    scenario_name="Push droidcast raw apk to device on setup",
)
def test_scenario():
    pass


@given("Driver is connected to device", target_fixture="screenshot")
def given1():
    driver = mock.Mock(spec=DriverAdapter)
    driver.push.return_value = None

    screenshot = DroidCastRaw(driver)
    return screenshot


@when("I setup the screenshot")
def when1(screenshot: DroidCastRaw):
    screenshot.setup()


@then("Droidcast apk should be pushed to device")
def then1(screenshot: DroidCastRaw):
    pass
