Feature: Page

  Scenario: Linking a child page to a parent page
    Given Lobby page and Campaign page
    When Lobby links to Campaign
    Then Campaign should become a child of Lobby
    And Lobby should become a parent of Campaign

  Scenario: Linking a child to another child
    Given Lobby is a parent of Campaign
    When Campaign links to Mission
    Then Mission should become a child of Campaign
    And Mission should not become a child of Lobby
