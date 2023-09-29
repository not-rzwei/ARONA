from unittest import mock

from pytest_bdd import scenario, given, then, when

from src.game.navigator import Navigator
from src.game.page import Page


@scenario(
    feature_name="navigator.feature",
    scenario_name="Page path finding",
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


@given("Navigator is on Lobby", target_fixture="navigator")
def given1(pages):
    lobby, *_ = pages

    driver = mock.Mock()
    navigator = Navigator(driver)
    navigator.register(lobby, pages)
    return navigator


@when("Navigator find path to Mission", target_fixture="path")
def when1(navigator):
    return navigator.find_path("Mission")


@then("Navigator should return Lobby, Campaign, Mission")
def then1(path):
    assert path is not None
    assert len(path) == 3
    assert path[0].name == "Lobby"
    assert path[1].name == "Campaign"
    assert path[2].name == "Mission"
