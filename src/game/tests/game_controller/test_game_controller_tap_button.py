from unittest import mock

import pytest
from pytest_bdd import scenario, given, then, when

from src.game.game_controller import GameController
from src.game.resource import ButtonResource


@scenario(
    feature_name="game_controller.feature",
    scenario_name="Find and tap a button",
)
def test_scenario():
    pass


@pytest.fixture
def game_controller():
    device = mock.Mock()
    return GameController(device)


@given("Button is in the screen", target_fixture="button")
def given1(game_controller):
    button = ButtonResource("")
    button.area = ((0, 0), (100, 100))

    game_controller.find_image_on_screen = mock.Mock(return_value=button.area)
    return button


@when("Controller tap the button", target_fixture="result")
def when1(game_controller, button):
    return game_controller.tap_button(button)


@then("It should return true")
def then1(result, button):
    assert result is True
