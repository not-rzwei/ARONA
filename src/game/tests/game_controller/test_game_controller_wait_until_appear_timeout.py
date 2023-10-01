from unittest import mock

import pytest
from pytest_bdd import scenario, given, then, when

from src.game.game_controller import GameController
from src.game.page import Page


@scenario(
    feature_name="game_controller.feature",
    scenario_name="Timeout waiting for Lobby landmark to appear",
)
def test_scenario():
    pass


@pytest.fixture
def game_controller():
    device = mock.Mock()
    return GameController(device)


@given("The game is transitioning to Campaign page")
@given("The game stuck in Lobby page until timeout")
def given1(game_controller, mocker):
    mocker.patch("time.time", side_effect=[0, 1, 2])
    mocker.patch("time.sleep")

    game_controller.is_image_on_screen = mock.Mock(side_effect=[False, False])


@when(
    "Controller wait for Campaign landmark to appear with timeout 2 seconds",
    target_fixture="result",
)
def when1(game_controller):
    campaign = Page("Campaign")
    return game_controller.until_image_is_on_screen(campaign.cue, timeout=2)


@then("It should return false")
def then1(result):
    assert result is False
