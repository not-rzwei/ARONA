from pytest_bdd import scenario, given, when, then

from src.game.page import Page


@scenario(
    "page.feature",
    "Linking a child to another child",
)
def test_scenario():
    pass


@given("Lobby is a parent of Campaign", target_fixture="pages")
def given1():
    lobby = Page("Lobby")
    campaign = Page("Campaign")

    lobby.link(campaign)

    return lobby, campaign


@when("Campaign links to Mission", target_fixture="mission")
def when1(pages):
    mission = Page("Mission")
    pages[1].link(mission)
    return mission


@then("Mission should become a child of Campaign")
@then("Mission should not become a child of Lobby")
def then1(pages, mission):
    lobby, campaign = pages
    assert mission in campaign.children
    assert mission not in lobby.children
