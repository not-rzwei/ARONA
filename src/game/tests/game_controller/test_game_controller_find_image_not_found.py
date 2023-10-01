from unittest import mock

import pytest
from pytest_bdd import scenario, given, then, when

from src.game.game_controller import GameController
from src.game.resource import ImageResource


@scenario(
    feature_name="game_controller.feature",
    scenario_name="Not found a matching image in Lobby page",
)
def test_scenario():
    pass


@pytest.fixture
def game_controller():
    device = mock.Mock()
    return GameController(device)


@given("The game is in Lobby page")
def given1(game_controller, mocker):
    game_controller._device.screenshot.return_value = ImageResource(
        "tests/pages/LOBBY.jpg"
    ).load()


@when("Controller find the image not in Lobby", target_fixture="result")
def when1(game_controller):
    img = ImageResource("pages/campaign/LANDMARK.png")
    return game_controller.find_image_on_screen(img)


@then("It should return zero area")
def then1(result):
    assert result == ((0, 0), (0, 0))
