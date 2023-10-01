from unittest import mock

import pytest
from pytest_bdd import scenario, given, then, when

from src.game.game_controller import GameController
from src.game.resource import ImageResource


@scenario(
    feature_name="game_controller.feature",
    scenario_name="Wait for Lobby landmark to appear",
)
def test_scenario():
    pass


@pytest.fixture
def game_controller():
    device = mock.Mock()
    return GameController(device)


@given("The game is transitioning to Campaign page")
@given("Take 2 seconds to complete the transition")
def given1(game_controller, mocker):
    mocker.patch("time.time", side_effect=[0, 1, 2])
    mocker.patch("time.sleep")

    game_controller.is_image_on_screen = mock.Mock(side_effect=[False, True])


@when("Controller wait for Campaign landmark to appear", target_fixture="result")
def when1(game_controller):
    return game_controller.until_image_is_on_screen(ImageResource("test"))


@then("It should return true")
def then1(game_controller, result):
    assert result is True
    assert game_controller.is_image_on_screen.call_count == 2
