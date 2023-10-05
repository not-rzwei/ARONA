Feature: Navigator

  Background:
    Given Navigator is initialized
    And Pages are loaded
      """
      Lobby => Campaign
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
