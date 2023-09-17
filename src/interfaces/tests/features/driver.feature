Feature: Driver

  Scenario: Auto connect driver if not connected
    Given Driver is not connected to the device
    When I execute a decorated command with auto connect
    Then Driver should be connected to the device
    And I get a result from the command
