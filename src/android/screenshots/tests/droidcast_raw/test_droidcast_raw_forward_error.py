from unittest import mock

import pytest
from pytest_bdd import scenario, when, then, given

from src.adapters.driver import DriverAdapter, DriverForwardError
from src.adapters.screenshot import ScreenshotSetupError
from src.android.screenshots.droidcast_raw import DroidCastRaw


@scenario(
    feature_name="droidcast_raw.feature",
    scenario_name="Error forwarding droidcast port to host on setup",
)
def test_scenario():
    pass


@given("Droidcast server is running on device", target_fixture="screenshot")
def given1():
    driver = mock.Mock(spec=DriverAdapter)
    screenshot = DroidCastRaw(driver)
    return screenshot


@given("No local port is available")
def given2(screenshot: DroidCastRaw):
    screenshot._driver.forward.side_effect = DriverForwardError  # type: ignore


@when("I setup the screenshot")
def when1(screenshot: DroidCastRaw):
    with pytest.raises(ScreenshotSetupError):
        screenshot.setup()


@then("Droidcast should raise an error")
def then1(screenshot: DroidCastRaw):
    pass
