from unittest import mock

import pytest
from pytest_bdd import scenario, given, then, when

from src.game.game_controller import GameController
from src.game.resource import ButtonResource


@scenario(
    feature_name="game_controller.feature",
    scenario_name="Find button area if area hasn't been set before tapping",
)
def test_scenario():
    pass


@pytest.fixture
def game_controller():
    device = mock.Mock()
    gc = GameController(device)
    gc.find_image_on_screen = mock.Mock(return_value=((0, 0), (100, 100)))
    return gc


@given("Button area is ((0,0), (0,0))", target_fixture="button")
def given1():
    button = ButtonResource("")
    button.area = ((0, 0), (0, 0))
    return button


@when("Controller tap the button", target_fixture="result")
def when1(game_controller, button):
    return game_controller.tap_button(button)


@then("Find button area should be called")
@then("It should return true if the button is tapped")
def then1(game_controller, result, button):
    assert game_controller.find_image_on_screen.called is True
    assert result is True
    assert button.is_tapped is True
