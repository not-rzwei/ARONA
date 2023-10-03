from pytest_bdd import scenario, when, then, given


@scenario(
    feature_name="navigator.feature",
    scenario_name="Navigate to Lobby",
)
def test_scenario():
    pass


@given("The game is on Lobby")
def given1(navigator):
    navigator.set_current_page("Lobby")


@when("Navigator navigates to Campaign")
def when1(navigator):
    navigator.navigate_to("Campaign")


@then("Campaign screen is shown")
def then1(navigator):
    assert navigator.current_page.name == "Campaign"
