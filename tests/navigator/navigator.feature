Feature: Navigator

  Background:
    Given Navigator is initialized
    And Pages are loaded
      """
      Lobby => Campaign, Club
      Campaign => Mission, Bounty
      """

  Scenario: Navigate to Mission
    Given The game is on Lobby
    When Navigator navigates to Mission
    Then Campaign entrypoint is tapped
    And Mission entrypoint is tapped
    And Mission screen is shown
    And History should be Campaign, Mission

  Scenario: Navigate to Bounty
    Given The game is on Mission
    When Navigator navigates to Bounty
    Then The back button is tapped
    And Bounty entrypoint is tapped
    And Bounty screen is shown
    And History should be Campaign, Bounty

  # Go to lobby directly instead navigating back
  Scenario: Navigate to Club
    Given The game is on Bounty
    When Navigator navigates to Club
    Then Lobby entrypoint is tapped
    And Club entrypoint is tapped
    And Club screen is shown
    And History should be Lobby, Club