from unittest import mock

from pytest_bdd import scenario, when, then, given

from src.android.screenshots.droidcast_raw import DroidcastRawScreenshot
from src.interfaces.driver import IDriver


@scenario(
    feature_name="droidcast_raw.feature",
    scenario_name="Push droidcast raw apk to device on setup",
)
def test_scenario():
    pass


@given("Driver is connected to device", target_fixture="screenshot")
def given1():
    driver = mock.Mock(spec=IDriver)
    driver.push.return_value = None

    screenshot = DroidcastRawScreenshot(driver)
    return screenshot


@when("I setup the screenshot")
def when1(screenshot: DroidcastRawScreenshot):
    screenshot.setup()


@then("Droidcast apk should be pushed to device")
def then1(screenshot: DroidcastRawScreenshot):
    pass
