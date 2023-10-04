from unittest import mock

import pytest
from pytest_bdd import scenario, given, then, when

from src.game.navigator import Navigator
from src.game.resource import ButtonResource


@scenario(
    feature_name="navigator.feature",
    scenario_name="Navigate to parent page with back button",
)
def test_scenario():
    pass


@pytest.fixture
def navigator(lobby, campaign, mission):
    controller = mock.Mock()
    navigator = Navigator(controller)
    navigator.register(lobby, campaign, mission)
    return navigator


@given("Navigator is on Mission")
@given("Screen is on Mission")
@given("Back button is set")
def given1(navigator):
    back_button = ButtonResource("test")
    navigator.set_back_button(back_button)
    navigator.set_current_page("Mission")

    return back_button


@when("Navigator navigates to Campaign")
def when1(navigator):
    navigator.navigate_to("Campaign")


@then("Navigator history should only have Campaign")
@then("Back button should be tapped")
def then1(navigator, campaign):
    assert navigator.history == [campaign]
    assert navigator._controller.tap_button.called_once_with(navigator.back_button)
