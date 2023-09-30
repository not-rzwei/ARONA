from pytest_bdd import scenario, given, when, then

from src.game.page import Page


@scenario(
    "page.feature",
    "Linking a child page to a parent page",
)
def test_scenario():
    pass


@given("Lobby page and Campaign page", target_fixture="pages")
def given1():
    lobby = Page("Lobby")
    campaign = Page("Campaign")

    return lobby, campaign


@when("Lobby links to Campaign")
def when1(pages):
    lobby, campaign = pages
    lobby.link(campaign)


@then("Campaign should become a child of Lobby")
def then1(pages):
    lobby, campaign = pages
    assert campaign in lobby.links


@then("Lobby should become a parent of Campaign")
def then2(pages):
    lobby, campaign = pages
    assert campaign.parent == lobby
