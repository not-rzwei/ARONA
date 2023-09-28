from unittest import mock

import pytest
from pytest_bdd import scenario, when, then, given

from src.android.screenshots.droidcast_raw import DroidcastRawScreenshot
from src.interfaces.driver import IDriver, DriverPushError
from src.interfaces.screenshot import ScreenshotSetupError


@scenario(
    feature_name="droidcast_raw.feature",
    scenario_name="Error pushing droidcast raw apk to device on setup",
)
def test_scenario():
    pass


@given("Driver is connected to device", target_fixture="screenshot")
def given1():
    driver = mock.Mock(spec=IDriver)
    screenshot = DroidcastRawScreenshot(driver)
    return screenshot


@given("APK file does not exist")
def given2(screenshot: DroidcastRawScreenshot):
    screenshot._driver.push.side_effect = DriverPushError


@when("I setup the screenshot")
def when1(screenshot: DroidcastRawScreenshot):
    with pytest.raises(ScreenshotSetupError):
        screenshot.setup()


@then("Droidcast should raise an error")
def then1(screenshot: DroidcastRawScreenshot):
    pass
