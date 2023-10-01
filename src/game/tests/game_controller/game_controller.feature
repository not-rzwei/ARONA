Feature: Game Controller

  Scenario: Check if Lobby landmark is found in Lobby page
    Given The game is in Lobby page
    When Controller find Lobby landmark
    Then It should return true

