from unittest import mock

from pytest_bdd import scenario, given, then, when

from src.game.navigator import Navigator


@scenario(
    feature_name="navigator.feature",
    scenario_name="No path found",
)
def test_scenario():
    pass


@given("Navigator is on Lobby", target_fixture="navigator")
def given1(lobby, campaign, mission):
    device = mock.Mock()
    navigator = Navigator(device)
    navigator.register(lobby, campaign, mission)
    navigator.set_current_page("Lobby")
    return navigator


@when("Navigator find path to Unknown", target_fixture="path")
def when1(navigator):
    return navigator.find_path("Unknown")


@then("Navigator should return None")
def then1(path):
    assert path is None
