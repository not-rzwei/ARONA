Feature: UIAutomator2 driver for Android

  Scenario: Establishing a connection to an Android device
    Given I have an Android device serial address
    When I connect to the device
    Then Driver state should be connected
    And Device property should be set

  Scenario: Cannot establish a connection to an Android device
    Given I have an Android device serial address
    When Driver connect to the device 3 times
    Then Driver raise an error after reaching max retries