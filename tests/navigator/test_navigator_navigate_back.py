from pytest_bdd import scenario, when, then, given

from src.game.resource import ButtonResource


@scenario(
    feature_name="navigator.feature",
    scenario_name="Back to Lobby",
)
def test_scenario():
    pass


@given("The game is on Campaign")
@given("Back button is set")
def given1(navigator):
    navigator.set_current_page("Campaign")

    back_button = ButtonResource("common/NAVIGATION_BACK.png")
    navigator.set_back_button(back_button)


@when("Navigator navigates to Lobby")
def when1(navigator):
    navigator.navigate_to("Lobby")


@then("Lobby screen is shown")
def then1(navigator):
    assert navigator.current_page.name == "Lobby"
