Feature: UIAutomator2 driver for Android

  Scenario: Establishing a connection to an Android device
    Given I have an Android device serial address
    When I connect to the device
    Then Driver state should be connected
    And Device property should be set

  Scenario: Cannot establish a connection to an Android device
    Given Device serial address is unreachable
    When I connect to the device
    Then Driver raise an error