from unittest import mock

import pytest
from pytest_bdd import scenario, given, then, when

from src.game.game_controller import GameController
from src.game.page import Page
from src.game.resource import ImageResource


@scenario(
    feature_name="game_controller.feature",
    scenario_name="Check if Lobby landmark is found in Lobby page",
)
def test_scenario():
    pass


@pytest.fixture
def game_controller():
    device = mock.Mock()
    return GameController(device)


@given("The game is in Lobby page")
def given1(game_controller):
    game_controller._device.screenshot.return_value = ImageResource(
        "tests/pages/LOBBY.jpg"
    ).load()


@when("Controller find Lobby landmark", target_fixture="result")
def when1(game_controller):
    lobby = Page("Lobby")
    return game_controller.is_image_on_screen(lobby.cue)


@then("It should return true")
def then1(result):
    assert result is True
