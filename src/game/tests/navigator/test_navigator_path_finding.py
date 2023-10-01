from unittest import mock

from pytest_bdd import scenario, given, then, when

from src.game.navigator import Navigator


@scenario(
    feature_name="navigator.feature",
    scenario_name="Page path finding",
)
def test_scenario():
    pass


@given("Navigator is on Lobby", target_fixture="navigator")
def given1(lobby, campaign, mission):
    controller = mock.Mock()
    navigator = Navigator(controller)
    navigator.register(lobby, campaign, mission)
    navigator.set_current_page("Lobby")
    return navigator


@when("Navigator find path to Mission", target_fixture="path")
def when1(navigator):
    return navigator.find_path("Mission")


@then("Navigator should return Lobby, Campaign, Mission")
def then1(path):
    assert len(path) == 3
    assert path[0].name == "Lobby"
    assert path[1].name == "Campaign"
    assert path[2].name == "Mission"
