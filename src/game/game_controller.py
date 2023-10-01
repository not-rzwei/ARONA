import cv2

from src.android.device import AndroidDevice
from src.game.resource import ImageResource


class GameController:
    """Emulate behaviour of human player."""

    def __init__(self, device: AndroidDevice):
        self._device = device

    def is_image_on_screen(
        self, image: ImageResource, threshold: float = 0.969
    ) -> bool:
        """Check if image is on screen."""
        screenshot = self._device.screenshot()
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
        template = cv2.cvtColor(image.load(), cv2.COLOR_RGB2GRAY)
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        return max_val >= threshold
