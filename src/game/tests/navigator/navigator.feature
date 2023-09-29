Feature: Navigator

  Background:
    Given Lobby is the main page
    And Campaign page can be accessed from Lobby
    And Mission page can be accessed from Campaign

  Scenario: Page path finding
    Given Navigator is on Lobby
    When Navigator find path to Mission
    Then Navigator should return Lobby, Campaign, Mission

  Scenario: No path found
    Given Navigator is on Lobby
    When Navigator find path to Unknown
    Then Navigator should return None
