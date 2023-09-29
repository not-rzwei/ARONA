from unittest import mock

import pytest
from pytest_bdd import scenario, when, then, given

from src.adapters.driver import DriverAdapter, DriverServerError
from src.adapters.screenshot import ScreenshotSetupError
from src.android.screenshots.droidcast_raw import DroidCastRaw


@scenario(
    feature_name="droidcast_raw.feature",
    scenario_name="Error running droidcast raw server on device on setup due",
)
def test_scenario():
    pass


@given("APK file has been pushed to device", target_fixture="screenshot")
def given1():
    driver = mock.Mock(spec=DriverAdapter)
    screenshot = DroidCastRaw(driver)
    return screenshot


@given("Device is glitchy")
def given2(screenshot: DroidCastRaw):
    screenshot._driver.run_daemon.side_effect = DriverServerError  # type: ignore


@when("I setup the screenshot")
def when1(screenshot: DroidCastRaw):
    with pytest.raises(ScreenshotSetupError):
        screenshot.setup()


@then("Droidcast should raise an error")
def then1(screenshot: DroidCastRaw):
    pass
