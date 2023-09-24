Feature: Device

  Background:
    Given The driver is uiautomator2
    And Screenshot method is droidcast raw
    And Touch method is shell input

  Scenario: Connect to Device
    Given The device is provided
    When I connect to the device
    Then I can take a screenshot
    Then I can touch the screen

  Scenario: Error connecting to Device due to unreachable device
    Given The device serial address is invalid
    When I connect to the device
    Then I got an driver error message

  Scenario: Error connecting to Device due to screenshot error
    Given The device is provided
    When I connect to the device
    Then I got an screenshot error message
