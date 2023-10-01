from unittest import mock

import pytest
from pytest_bdd import scenario, given, then, when

from src.game.game_controller import GameController
from src.game.resource import ButtonResource


@scenario(
    feature_name="game_controller.feature",
    scenario_name="Tap a button",
)
def test_scenario():
    pass


@pytest.fixture
def game_controller():
    device = mock.Mock()
    return GameController(device)


@given("Button area is ((0, 0), (100, 100))", target_fixture="button")
def given1():
    button = ButtonResource("")
    button.area = ((0, 0), (100, 100))
    return button


@when("Controller tap the button", target_fixture="result")
def when1(game_controller, button):
    return game_controller.tap_button(button)


@then("It should return true if the button is tapped")
def then1(result, button):
    assert result is True
    assert button.is_tapped is True
