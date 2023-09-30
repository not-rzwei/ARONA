from unittest import mock

from pytest_bdd import scenario, given, then, when

from src.game.navigator import Navigator
from src.game.page import Page


@scenario(
    feature_name="navigator.feature",
    scenario_name="Find path to sibling page",
)
def test_scenario():
    pass


@given("Raid is a sibling page of Mission")
@given("Navigator is on Mission", target_fixture="navigator")
def given1(lobby, campaign, mission):
    raid = Page("Raid")
    campaign.link(raid)

    device = mock.Mock()
    navigator = Navigator(device)
    navigator.register(lobby, campaign, mission, raid)
    navigator.set_current_page("Mission")
    return navigator


@when("Navigator find path to Raid", target_fixture="path")
def when1(navigator):
    return navigator.find_path("Raid")


@then("Navigator should return Mission, Campaign, Raid")
def then1(path):
    assert len(path) == 3
    assert path[0].name == "Mission"
    assert path[1].name == "Campaign"
    assert path[2].name == "Raid"
