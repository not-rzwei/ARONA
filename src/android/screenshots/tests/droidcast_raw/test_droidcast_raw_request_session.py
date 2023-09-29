from unittest import mock

from pytest_bdd import scenario, when, then, given

from src.adapters.driver import DriverAdapter
from src.android.screenshots.droidcast_raw import DroidCastRaw


@scenario(
    feature_name="droidcast_raw.feature",
    scenario_name="Set request session on setup",
)
def test_scenario():
    pass


@given("Droidcast server is running on device", target_fixture="screenshot")
def given1():
    driver = mock.Mock(spec=DriverAdapter)
    driver.forward.return_value = 6969

    screenshot = DroidCastRaw(driver)
    return screenshot


@when("I setup the screenshot")
def when1(screenshot: DroidCastRaw):
    screenshot.setup()


@then("Droidcast should set the request session")
def then1(screenshot: DroidCastRaw):
    assert screenshot._session is not None
