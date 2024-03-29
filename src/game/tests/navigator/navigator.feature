Feature: Navigator

  Background:
    Given Lobby is the main page
    And Campaign page can be accessed from Lobby
    And Mission page can be accessed from Campaign

  Scenario: Page path finding
    Given Navigator is on Lobby
    When Navigator find path to Mission
    Then Navigator should return Lobby, Campaign, Mission

  Scenario: Find path to sibling page
    Given Raid is a sibling page of Mission
    And Navigator is on Mission
    When Navigator find path to Raid
    Then Navigator should return Mission, Campaign, Raid

  Scenario: Find path to uncle page
    Given Cafe is a sibling page of Campaign
    And Navigator is on Mission
    When Navigator find path to Cafe
    Then Navigator should return Mission, Campaign, Lobby, Cafe

  Scenario: No path found
    Given Navigator is on Lobby
    When Navigator find path to Unknown
    Then Navigator should return None

  Scenario: Detect current page from screenshot
    Given Screenshot is taken from Lobby
    When Navigator detect page
    Then Navigator should return Lobby

  Scenario: Match current page with device
    Given Navigator is on Lobby
    And Screenshot is taken from Lobby
    When Navigator match current page
    Then Navigator should return true

  Scenario: Current page does not match with device
    Given Navigator is on Lobby
    And Screenshot is taken from Campaign
    When Navigator match current page
    Then Navigator should return false

  Scenario: Navigate to page
    Given Navigator is on Lobby
    When Navigator navigate to Campaign
    Then Navigator should be on Campaign

  Scenario: Remove first page from path when navigating
    Given Navigator is on Lobby
    And Screen is on Lobby
    When Navigator navigate to Campaign
    Then Navigator history should only have Campaign

  Scenario: Navigate to parent page with back button
    Given Navigator is on Mission
    And Screen is on Mission
    And Back button is set
    When Navigator navigates to Campaign
    Then Navigator history should only have Campaign
    And Back button should be tapped