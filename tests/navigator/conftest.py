from dependency_injector import containers, providers
from pytest_bdd import given, parsers

from src.android.device import AndroidDevice
from src.android.drivers.uiautomator2 import UIAutomator2
from src.android.screenshots.droidcast_raw import DroidCastRaw
from src.android.touches.shell_input import ShellInput
from src.game.game_controller import GameController
from src.game.navigator import Navigator
from src.game.page import Page
from src.game.resource import ButtonResource


class CoreDeviceContainer(containers.DeclarativeContainer):
    serial_address = providers.Object("127.0.0.1:16448")
    driver = providers.Singleton(UIAutomator2, serial_address)
    screenshot = providers.Singleton(DroidCastRaw, driver=driver)
    touch = providers.Singleton(ShellInput, driver=driver)
    device = providers.Factory(
        AndroidDevice, driver=driver, screenshot=screenshot, touch=touch
    )


@given("Navigator is initialized", target_fixture="navigator")
def container():
    device_container = CoreDeviceContainer()
    device = device_container.device()
    device.connect()

    game_controller = GameController(device)
    navigator = Navigator(game_controller)

    back_button = ButtonResource("common/NAVIGATION_BACK.png")
    navigator.set_back_button(back_button)
    yield navigator

    device.disconnect()


@given(parsers.parse("Pages are loaded\n{content}"))
def pages(navigator):
    lobby = Page("Lobby")
    campaign = Page("Campaign")
    mission = Page("Mission")
    bounty = Page("Bounty")
    club = Page("Club")
    lobby.link(campaign, club)
    campaign.link(mission, bounty)
    navigator.register(lobby, campaign, mission, bounty, club)
