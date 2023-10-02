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

  Scenario: Find a matching image and get the area in Lobby page
    Given The game is in Lobby page
    When Controller find the image
    Then It should return the area of the image

  Scenario: Find a matching image with cache enabled
    Given The game is in Lobby page
    When Controller find the same image twice
    Then It should return the area of the image
    And Matching should be done only once

  Scenario: Not found a matching image in Lobby page
    Given The game is in Lobby page
    When Controller find the image not in Lobby
    Then It should return zero area

  Scenario: Find and tap a button
    Given Button is in the screen
    When Controller tap the button
    Then It should return true if the button is tapped

  Scenario: Tap a button outside the screen
    Given Button area is ((0,0), (0,0))
    When Controller tap the button
    Then It should return false