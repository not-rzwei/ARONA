import time

import cv2
import numpy as np

from src.android.device import AndroidDevice
from src.constants.type import ScreenArea
from src.game.resource import ImageResource, ButtonResource
from src.utils.number import random_point_in_area


class GameController:
    """Emulate behaviour of human player."""

    def __init__(self, device: AndroidDevice):
        self._device = device

    def _match_image_resource_with_screen(self, image: ImageResource):
        """Match ImageResource with game screen.

        Before matching, convert both images to grayscale.

        Args:
            image: ImageResource

        Return:
            Matching template result and shape of template
        """
        screenshot = self._device.screenshot()
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
        template = cv2.cvtColor(image.load(), cv2.COLOR_RGB2GRAY)

        return (
            cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED),
            template.shape[::-1],
        )

    def is_image_on_screen(
        self, image: ImageResource, threshold: float = 0.969
    ) -> bool:
        """Check if image is on screen."""
        result, _ = self._match_image_resource_with_screen(image)
        locations = np.where(result >= threshold)

        return len(locations) > 0

    def until_image_is_on_screen(
        self,
        image: ImageResource,
        threshold: float = 0.969,
        delay: float = 0.5,
        timeout: int = 10,
    ) -> bool:
        """Wait until image is on screen."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.is_image_on_screen(image, threshold):
                return True
            time.sleep(delay)
        return False

    def find_image_on_screen(
        self, image: ImageResource, threshold: float = 0.969, cache: bool = False
    ) -> ScreenArea:
        """Find image resource on game screen.

        Args:
            image: ImageResource
            threshold: Matching threshold (default: 0.969)
            cache: Cache matching result (default: False)

        Return:
            top-left and bottom-right coordinates
        """
        if cache and image.area != ((0, 0), (0, 0)):
            return image.area

        result, shape = self._match_image_resource_with_screen(image)
        locations = np.where(result >= threshold)

        for pt in zip(*locations[::-1]):
            area: ScreenArea = pt[::-1], (
                pt[0] + shape[0],
                pt[1] + shape[1],
            )  # type: ignore

            if cache:
                image.area = area

            return area

        return (0, 0), (0, 0)

    def tap_button(self, button: ButtonResource) -> bool:
        point = random_point_in_area(button.area)

        if point == (0, 0):
            area = self.find_image_on_screen(button)
            point = random_point_in_area(area)

        button.is_tapped = False
        if self._device.tap(point):
            button.is_tapped = True
            return True
        return False
