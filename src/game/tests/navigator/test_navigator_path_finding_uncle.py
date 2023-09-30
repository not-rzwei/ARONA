from unittest import mock

from pytest_bdd import scenario, given, then, when

from src.game.navigator import Navigator
from src.game.page import Page


@scenario(
    feature_name="navigator.feature",
    scenario_name="Find path to uncle page",
)
def test_scenario():
    pass


@given("Cafe is a sibling page of Campaign")
@given("Navigator is on Mission", target_fixture="navigator")
def given1(lobby, campaign, mission):
    cafe = Page("Cafe")
    lobby.link(cafe)

    device = mock.Mock()
    navigator = Navigator(device)
    navigator.register(lobby, campaign, mission, cafe)
    navigator.set_current_page("Mission")
    return navigator


@when("Navigator find path to Cafe", target_fixture="path")
def when1(navigator):
    return navigator.find_path("Cafe")


@then("Navigator should return Mission, Campaign, Lobby, Cafe")
def then1(path):
    assert len(path) == 4
    assert path[0].name == "Mission"
    assert path[1].name == "Campaign"
    assert path[2].name == "Lobby"
    assert path[3].name == "Cafe"
