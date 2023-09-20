Feature: Screenshot using Droidcast Raw

# Setup: push apk
  Scenario: Push droidcast raw apk to device on setup
    Given Driver is connected to device
    When I setup the screenshot
    Then Droidcast apk should be pushed to device

  Scenario: Error pushing droidcast raw apk to device on setup
    Given Driver is connected to device
    And APK file does not exist
    When I setup the screenshot
    Then Droidcast should raise an error

# Setup: run apk
  Scenario: Run droidcast raw server on device on setup
    Given APK file has been pushed to device
    When I setup the screenshot
    Then Droidcast server PID should be set

  Scenario: Error running droidcast raw server on device on setup due
    Given APK file has been pushed to device
    And Device is glitchy
    When I setup the screenshot
    Then Droidcast should raise an error

# Setup: forward port
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

# Setup: get resolution
  Scenario: Set screenshot resolution on setup
    Given Device resolution is 720x1280
    When I setup the screenshot
    Then Droidcast should set the screenshot resolution to 1280x720

  Scenario: Error setting screenshot resolution on setup
    Given Driver is glitchy
    When I setup the screenshot
    Then Droidcast should raise an error

# Take screenshot
  Scenario: Take screenshot
    Given Droidcast server has been setup
    And Resolution is 1280x720
    When I take a screenshot
    Then Droidcast should return ndarray of screenshot
    And Screenshot should be 1280x720
    And Has BGR color space
