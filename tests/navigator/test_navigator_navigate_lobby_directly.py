from pytest_bdd import scenario, when, then, given


@scenario(
    feature_name="navigator.feature",
    scenario_name="Navigate to Club",
)
def test_scenario():
    pass


@given("The game is on Bounty")
def given1(navigator):
    navigator.set_current_page("Bounty")


@when("Navigator navigates to Club")
def when1(navigator):
    navigator.navigate_to("Club")


@then("Lobby entrypoint is tapped")
@then("Club entrypoint is tapped")
@then("Club screen is shown")
@then("History should be Lobby, Club")
def then1(navigator):
    assert navigator.pages["Lobby"].entrypoint.is_tapped is True
    assert navigator.pages["Club"].entrypoint.is_tapped is True
    assert navigator.current_page.name == "Club"
    assert navigator.history == [
        navigator.pages["Lobby"],
        navigator.pages["Club"],
    ]
