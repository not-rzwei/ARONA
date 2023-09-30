from unittest import mock

import cv2
import pytest
from pytest_bdd import scenario, given, then, when

from src.constants.path import RES_FOLDER
from src.game.navigator import Navigator
from src.game.page import Page


@scenario(
    feature_name="navigator.feature",
    scenario_name="Detecting current page",
)
def test_scenario():
    pass


@given("Lobby is the main page", target_fixture="pages")
@given("Campaign page can be accessed from Lobby")
@given("Mission page can be accessed from Campaign")
def background():
    lobby = Page("Lobby")
    campaign = Page("Campaign")
    mission = Page("Mission")

    lobby.link(campaign)
    campaign.link(mission)

    return lobby, campaign, mission


@pytest.fixture
def navigator(pages):
    lobby, *_ = pages

    device = mock.Mock()
    navigator = Navigator(device)
    navigator.register(lobby, pages)
    return navigator


@given("Screenshot is taken from Lobby", target_fixture="screenshot")
def given1():
    img = cv2.imread(str(RES_FOLDER / "tests/pages/LOBBY.jpg"))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


@when("Navigator detect page", target_fixture="page")
def when1(navigator, screenshot):
    return navigator.detect_page(screenshot)


@then("Navigator should return Lobby")
def then1(page):
    assert page.name == "Lobby"
