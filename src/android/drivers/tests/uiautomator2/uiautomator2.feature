Feature: UIAutomator2 driver for Android

#  Connection stuff
  Scenario: Establishing a connection to an Android device
    Given I have an Android device serial address
    When I connect to the device
    Then Driver state should be connected
    And Device property should be set

  Scenario: Cannot establish a connection to an Android device
    Given Device serial address is unreachable
    When I connect to the device
    Then Driver raise an error

  Scenario: Disconnecting from an Android device
    Given Driver is already connected to the device
    When I disconnect from the device
    Then Driver state should be disconnected
    And Device property should be None

#  Execute shell commands
  Scenario: Execute a shell command on an Android device
    Given Driver is already connected to the device
    When I execute a command
    Then Driver should return a response

  Scenario: Error executing a shell command on an Android device
    Given Driver is already connected to the device
    When I execute a command
    Then Driver should raise an error

#  Run a daemon
  Scenario: Run a daemon on an Android device
    Given Driver is already connected to the device
    And ATX agent is running on the device
    When I run a daemon
    Then Driver should return the pid of the daemon

  Scenario: Error running a daemon on an Android device because ATX return non 200
    Given Driver is already connected to the device
    And ATX agent can't process request
    When I run a daemon
    Then Driver should raise an server error

  Scenario: Error running a daemon on an Android device because invalid json
    Given Driver is already connected to the device
    And ATX agent return invalid json
    When I run a daemon
    Then Driver should raise an server error

  Scenario: Error running a daemon on an Android device because invalid pid
    Given Driver is already connected to the device
    And ATX agent return invalid pid
    When I run a daemon
    Then Driver should raise an server error

#  Push file
  Scenario: Push a file to an Android device
    Given Driver is already connected to the device
    When I push a file
    Then Driver should not raise an error

  Scenario: Error pushing a file to an Android device because file not found
    Given Driver is already connected to the device
    And File to push is not found
    When I push a file
    Then Driver should raise an error

  Scenario: Error pushing a file to an Android device because permission denied on device
    Given Driver is already connected to the device
    And Destination path is not writable
    When I push a file
    Then Driver should raise an error
