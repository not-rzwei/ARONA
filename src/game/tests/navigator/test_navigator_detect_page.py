from unittest import mock

import pytest
from pytest_bdd import scenario, given, then, when

from src.game.navigator import Navigator
from src.game.resource import ImageResource


@scenario(
    feature_name="navigator.feature",
    scenario_name="Detect current page from screenshot",
)
def test_scenario():
    pass


@pytest.fixture
def navigator(lobby, campaign, mission):
    device = mock.Mock()
    navigator = Navigator(device)
    navigator.register(lobby, campaign, mission)
    return navigator


@given("Screenshot is taken from Lobby", target_fixture="screenshot")
def given1():
    return ImageResource("tests/pages/LOBBY.jpg").load()


@when("Navigator detect page", target_fixture="page")
def when1(navigator, screenshot):
    return navigator.detect_page(screenshot)


@then("Navigator should return Lobby")
def then1(page):
    assert page.name == "Lobby"
