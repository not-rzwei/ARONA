from unittest import mock

import pytest
from pytest_bdd import scenario, when, then, given

from src.adapters.driver import DriverAdapter, DriverPushError
from src.adapters.screenshot import ScreenshotSetupError
from src.android.screenshots.droidcast_raw import DroidCastRaw


@scenario(
    feature_name="droidcast_raw.feature",
    scenario_name="Error pushing droidcast raw apk to device on setup",
)
def test_scenario():
    pass


@given("Driver is connected to device", target_fixture="screenshot")
@given("APK file does not exist")
def given1():
    driver = mock.Mock(spec=DriverAdapter)
    driver.push.side_effect = DriverPushError
    screenshot = DroidCastRaw(driver)
    return screenshot


@when("I setup the screenshot")
def when1(screenshot: DroidCastRaw):
    with pytest.raises(ScreenshotSetupError):
        screenshot.setup()


@then("Droidcast should raise an error")
def then1(screenshot: DroidCastRaw):
    pass
