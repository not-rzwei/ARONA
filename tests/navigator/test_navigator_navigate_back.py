from pytest_bdd import scenario, when, then, given


@scenario(
    feature_name="navigator.feature",
    scenario_name="Navigate to Bounty",
)
def test_scenario():
    pass


@given("The game is on Mission")
def given1(navigator):
    navigator.set_current_page("Mission")


@when("Navigator navigates to Bounty")
def when1(navigator):
    navigator.navigate_to("Bounty")


@then("The back button is tapped")
@then("Bounty entrypoint is tapped")
@then("Bounty screen is shown")
@then("History should be Campaign, Bounty")
def then1(navigator):
    assert navigator.back_button.is_tapped is True
    assert navigator.pages["Bounty"].entrypoint.is_tapped is True
    assert navigator.current_page.name == "Bounty"
    assert navigator.history == [
        navigator.pages["Campaign"],
        navigator.pages["Bounty"],
    ]
