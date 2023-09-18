Feature: Driver

  Scenario: Auto recover driver if not connected
    Given Driver is not connected to the device
    When I execute a decorated command with auto recover
    Then Driver should be connected to the device
    And I get a result from the command

  Scenario: Abort auto recover if function throw other exception than DeviceNotConnectedException
    Given Driver is already connected to the device
    When I execute a decorated command with auto recover
    Then Driver raise the exception thrown by the function
    And Exit from auto recover