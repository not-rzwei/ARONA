Feature: Navigator

  Background:
    Given Navigator is initialized
    And Pages are loaded
      """
      Lobby Page
      Campaign Page is child of Lobby Page
      """

  Scenario: Navigate to Lobby
    Given The game is on Lobby
    When Navigator navigates to Campaign
    Then Campaign screen is shown

  Scenario: Back to Lobby
    Given The game is on Campaign
    And Back button is set
    When Navigator navigates to Lobby
    Then Lobby screen is shown
