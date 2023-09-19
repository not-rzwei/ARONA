from unittest import mock

import pytest
from pytest_bdd import scenario, when, then, given

from src.android.screenshots.droidcast_raw import DroidcastRawScreenshot
from src.interfaces.driver import IDriver, DriverServerError
from src.interfaces.screenshot import ScreenshotSetupError


@scenario(
    feature_name="droidcast_raw.feature",
    scenario_name="Error running droidcast raw server on device on setup due",
)
def test_scenario():
    pass


@given("APK file has been pushed to device", target_fixture="screenshot")
def given1():
    driver = mock.Mock(spec=IDriver)
    screenshot = DroidcastRawScreenshot(driver)
    return screenshot


@given("Device is glitchy")
def given2(screenshot: DroidcastRawScreenshot):
    screenshot._driver.run_daemon.side_effect = DriverServerError  # type: ignore


@when("I setup the screenshot")
def when1(screenshot: DroidcastRawScreenshot):
    with pytest.raises(ScreenshotSetupError):
        screenshot.setup()


@then("Droidcast should raise an error")
def then1(screenshot: DroidcastRawScreenshot):
    pass
