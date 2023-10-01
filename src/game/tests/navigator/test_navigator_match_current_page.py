from unittest import mock

import pytest
from pytest_bdd import scenario, given, then, when

from src.game.navigator import Navigator
from src.game.resource import ImageResource


@scenario(
    feature_name="navigator.feature",
    scenario_name="Match current page with device",
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
@given("Screenshot is taken from Lobby")
def given1(navigator):
    navigator.set_current_page("Lobby")
    navigator._controller.is_image_on_screen.return_value = True

    return ImageResource("tests/pages/LOBBY.jpg").load()


@when("Navigator match current page", target_fixture="is_current_page")
def when1(navigator):
    return navigator.match_current_page()


@then("Navigator should return true")
def then1(is_current_page):
    assert is_current_page is True
