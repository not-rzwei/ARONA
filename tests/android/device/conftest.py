from dependency_injector import containers, providers
from pytest_bdd import given

from src.android.device import AndroidDevice
from src.android.drivers.uiautomator2 import UIAutomator2
from src.android.screenshots.droidcast_raw import DroidCastRaw
from src.android.touches.shell_input import ShellInput


class CoreDeviceContainer(containers.DeclarativeContainer):
    serial_address = providers.Object("127.0.0.1:16448")
    driver = providers.Singleton(UIAutomator2, serial_address)
    screenshot = providers.Singleton(DroidCastRaw, driver=driver)
    touch = providers.Singleton(ShellInput, driver=driver)
    device = providers.Factory(
        AndroidDevice, driver=driver, screenshot=screenshot, touch=touch
    )


@given("The driver is uiautomator2", target_fixture="container")
@given("Screenshot method is droidcast raw")
@given("Touch method is shell input")
def container():
    container = CoreDeviceContainer()
    return container
