Feature: Device

  Scenario: Connect to Device
    Given I provide the driver, screenshot and touch method
    When I connect to the device
    Then I can take a screenshot
    Then I can touch the screen