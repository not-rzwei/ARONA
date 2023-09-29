from unittest import mock

from pytest_bdd import scenario, when, then, given

from src.adapters.driver import DriverAdapter
from src.android.screenshots.droidcast_raw import DroidCastRaw


@scenario(
    feature_name="droidcast_raw.feature",
    scenario_name="Teardown setup",
)
def test_scenario():
    pass


@given("Droidcast server has been setup", target_fixture="screenshot")
def given1():
    driver = mock.Mock(spec=DriverAdapter)
    driver.push.return_value = None
    driver.run_daemon.return_value = 1234
    driver.forward.return_value = 1234

    driver.execute.return_value = ("", 0)
    driver.release_port.return_value = True

    screenshot = DroidCastRaw(driver)
    screenshot.setup()
    return screenshot


@when("I teardown the screenshot")
def when1(screenshot: DroidCastRaw):
    screenshot.teardown()


@then("Droidcast server PID should be unset")
def then1(screenshot: DroidCastRaw):
    assert screenshot.pid == 0


@then("Local port should be released")
def then2(screenshot: DroidCastRaw):
    assert screenshot.local_port == 0
