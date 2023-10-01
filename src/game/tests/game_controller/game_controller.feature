Feature: Game Controller

  Scenario: Check if Lobby landmark is found in Lobby page
    Given The game is in Lobby page
    When Controller find Lobby landmark
    Then It should return true

  Scenario: Wait for Lobby landmark to appear
    Given The game is transitioning to Campaign page
    And Take 2 seconds to complete the transition
    When Controller wait for Campaign landmark to appear
    Then It should return true

  Scenario: Timeout waiting for Lobby landmark to appear
    Given The game is transitioning to Campaign page
    And The game stuck in Lobby page until timeout
    When Controller wait for Campaign landmark to appear with timeout 2 seconds
    Then It should return false
