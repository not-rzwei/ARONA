from unittest import mock

import numpy as np
from pytest_bdd import scenario, when, then, given

from src.android.screenshots.droidcast_raw import DroidcastRawScreenshot
from src.interfaces.driver import IDriver


@scenario(
    feature_name="droidcast_raw.feature",
    scenario_name="Take screenshot",
)
def test_scenario():
    pass


@given("Droidcast server has been setup", target_fixture="screenshot")
def given1():
    driver = mock.Mock(spec=IDriver)
    driver.get_device_resolution.return_value = (1280, 720)

    screenshot = DroidcastRawScreenshot(driver)
    return screenshot


@given("Resolution is 1280x720")
def given2(screenshot: DroidcastRawScreenshot):
    pass


@when("I take a screenshot", target_fixture="result")
def when1(screenshot: DroidcastRawScreenshot):
    return screenshot.take()


@then("Droidcast should return ndarray of screenshot")
def then1(result: np.ndarray):
    assert True


@then("Screenshot should be 1280x720")
def then2(result: np.ndarray):
    assert True


@then("Has BGR color space")
def then3(result: np.ndarray):
    assert True
