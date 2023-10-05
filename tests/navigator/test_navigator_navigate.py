from pytest_bdd import scenario, when, then, given


@scenario(
    feature_name="navigator.feature",
    scenario_name="Navigate to Mission",
)
def test_scenario():
    pass


@given("The game is on Lobby")
def given1(navigator):
    navigator.set_current_page("Lobby")


@when("Navigator navigates to Mission")
def when1(navigator):
    navigator.navigate_to("Mission")


@then("Campaign entrypoint is tapped")
@then("Mission entrypoint is tapped")
@then("Mission screen is shown")
@then("History should be Campaign, Mission")
def then1(navigator):
    assert navigator.pages["Campaign"].entrypoint.is_tapped is True
    assert navigator.pages["Mission"].entrypoint.is_tapped is True
    assert navigator.current_page.name == "Mission"
    assert navigator.history == [
        navigator.pages["Campaign"],
        navigator.pages["Mission"],
    ]
