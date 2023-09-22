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
    screenshot = DroidcastRawScreenshot(driver)

    screenshot.resolution = (2, 1)
    screenshot._session = mock.Mock()
    screenshot._session.get.return_value.status_code = 200
    screenshot._session.get.return_value.content = b"\xFF\x00\x1F\x07"

    return screenshot


@when("I take a screenshot", target_fixture="result")
def when1(screenshot: DroidcastRawScreenshot):
    return screenshot.take()


@then("Droidcast should return ndarray of screenshot")
def then1(result: np.ndarray):
    assert result.shape == (2, 1, 3)
