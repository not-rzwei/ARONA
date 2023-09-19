from unittest import mock

import pytest
from pytest_bdd import scenario, when, then, given

from src.android.screenshots.droidcast_raw import DroidcastRawScreenshot
from src.interfaces.driver import IDriver, DriverForwardError
from src.interfaces.screenshot import ScreenshotSetupError


@scenario(
    feature_name="droidcast_raw.feature",
    scenario_name="Error forwarding droidcast port to host on setup",
)
def test_scenario():
    pass


@given("Droidcast server is running on device", target_fixture="screenshot")
def given1():
    driver = mock.Mock(spec=IDriver)
    screenshot = DroidcastRawScreenshot(driver)
    return screenshot


@given("No local port is available")
def given2(screenshot: DroidcastRawScreenshot):
    screenshot._driver.forward.side_effect = DriverForwardError  # type: ignore


@when("I setup the screenshot")
def when1(screenshot: DroidcastRawScreenshot):
    with pytest.raises(ScreenshotSetupError):
        screenshot.setup()


@then("Droidcast should raise an error")
def then1(screenshot: DroidcastRawScreenshot):
    pass
