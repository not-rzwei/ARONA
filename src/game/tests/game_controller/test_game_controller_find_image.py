from unittest import mock

import pytest
from pytest_bdd import scenario, given, then, when

from src.game.game_controller import GameController
from src.game.resource import ImageResource


@scenario(
    feature_name="game_controller.feature",
    scenario_name="Find a matching image and get the area in Lobby page",
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


@when("Controller find the image", target_fixture="result")
def when1(game_controller):
    img = ImageResource("pages/campaign/ENTRYPOINT.png")
    return game_controller.find_image_on_screen(img)


@then("It should return the area of the image")
def then1(result):
    top_left, bottom_right = result
    assert top_left[0] > 0
    assert top_left[1] > 0
    assert bottom_right[0] > 0
    assert bottom_right[1] > 0
