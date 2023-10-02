from unittest import mock

import pytest
from pytest_bdd import scenario, given, then, when

from src.game.navigator import Navigator
from src.game.resource import ImageResource


@scenario(
    feature_name="navigator.feature",
    scenario_name="Navigate to page",
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
def given1(navigator):
    navigator.set_current_page("Lobby")
    navigator._controller.is_image_on_screen.return_value = True

    return ImageResource("tests/pages/LOBBY.jpg").load()


@when("Navigator navigate to Campaign")
def when1(navigator):
    navigator.navigate_to("Campaign")


@then("Navigator should be on Campaign")
def then1(navigator, campaign):
    assert navigator.current_page == campaign
