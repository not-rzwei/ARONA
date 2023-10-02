from unittest import mock

import pytest
from pytest_bdd import scenario, given, then, when

from src.game.navigator import Navigator


@scenario(
    feature_name="navigator.feature",
    scenario_name="Remove first page from path when navigating",
)
def test_scenario():
    pass


@pytest.fixture
def navigator(lobby, campaign, mission):
    controller = mock.Mock()
    navigator = Navigator(controller)
    navigator.register(lobby, campaign, mission)
    return navigator


@given("Navigator is on Lobby")
@given("Screen is on Lobby")
def given1(navigator):
    navigator.set_current_page("Lobby")


@when("Navigator navigate to Campaign")
def when1(navigator):
    navigator.navigate_to("Campaign")


@then("Navigator history should only have Campaign")
def then1(navigator, campaign):
    assert navigator.history == [campaign]
