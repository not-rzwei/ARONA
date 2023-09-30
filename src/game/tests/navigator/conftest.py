from pytest_bdd import given

from src.game.page import Page


@given("Lobby is the main page", target_fixture="lobby")
def lobby():
    return Page("Lobby")


@given("Campaign page can be accessed from Lobby", target_fixture="campaign")
def campaign(lobby):
    node = Page("Campaign")
    lobby.link(node)
    return node


@given("Mission page can be accessed from Campaign", target_fixture="mission")
def mission(campaign):
    node = Page("Mission")
    campaign.link(node)
    return node
