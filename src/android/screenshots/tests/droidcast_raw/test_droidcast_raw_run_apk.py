from unittest import mock

from pytest_bdd import scenario, when, then, given

from src.android.screenshots.droidcast_raw import DroidcastRawScreenshot
from src.interfaces.driver import IDriver


@scenario(
    feature_name="droidcast_raw.feature",
    scenario_name="Run droidcast raw server on device on setup",
)
def test_scenario():
    pass


@given("APK file has been pushed to device", target_fixture="screenshot")
def given1():
    driver = mock.Mock(spec=IDriver)
    driver.push.return_value = None
    driver.run_daemon.return_value = 1234

    screenshot = DroidcastRawScreenshot(driver)
    return screenshot


@when("I setup the screenshot")
def when1(screenshot: DroidcastRawScreenshot):
    screenshot.setup()


@then("Droidcast server PID should be set")
def then1(screenshot: DroidcastRawScreenshot):
    assert screenshot.pid == 1234
