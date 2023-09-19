Feature: Screenshot using Droidcast Raw

  Scenario: Push droidcast raw apk to device on setup
    Given Driver is connected to device
    When I setup the screenshot
    Then Droidcast apk should be pushed to device

  Scenario: Error pushing droidcast raw apk to device on setup
    Given Driver is connected to device
    And APK file does not exist
    When I setup the screenshot
    Then Droidcast should raise an error

  Scenario: Run droidcast raw server on device on setup
    Given APK file has been pushed to device
    When I setup the screenshot
    Then Droidcast server PID should be set

  Scenario: Error running droidcast raw server on device on setup due
    Given APK file has been pushed to device
    And Device is glitchy
    When I setup the screenshot
    Then Droidcast should raise an error

  Scenario: Forward droidcast port to host on setup
    Given Droidcast server is running on device
    When I setup the screenshot
    Then Droidcast should return the local port number
    And Have URL for screenshot

  Scenario: Error forwarding droidcast port to host on setup
    Given Droidcast server is running on device
    And No local port is available
    When I setup the screenshot
    Then Droidcast should raise an error
