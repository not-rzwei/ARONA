from unittest import mock

import pytest
from pytest_bdd import scenario, when, then, given

from src.android.screenshots.droidcast_raw import DroidcastRawScreenshot
from src.interfaces.driver import IDriver, DriverResolutionError
from src.interfaces.screenshot import ScreenshotSetupError


@scenario(
    feature_name="droidcast_raw.feature",
    scenario_name="Error setting screenshot resolution on setup",
)
def test_scenario():
    pass


@given("Driver is glitchy", target_fixture="screenshot")
def given1():
    driver = mock.Mock(spec=IDriver)
    driver.get_device_resolution.side_effect = DriverResolutionError

    screenshot = DroidcastRawScreenshot(driver)
    return screenshot


@when("I setup the screenshot")
def when1(screenshot: DroidcastRawScreenshot):
    with pytest.raises(ScreenshotSetupError):
        screenshot.setup()


@then("Droidcast should raise an error")
def then1(screenshot: DroidcastRawScreenshot):
    pass
