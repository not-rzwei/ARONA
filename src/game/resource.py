from abc import abstractmethod, ABC

import cv2
import numpy.typing as npt

from src.constants.path import RES_FOLDER


class Resource(ABC):
    @abstractmethod
    def load(self):
        pass


class ImageResource(Resource):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"ImageResource({self.name})"

    def load(self) -> npt.NDArray:
        """Load RGB image from resource folder"""
        filename = RES_FOLDER / self.name
        if not filename.exists():
            raise FileNotFoundError(f"File {filename} not found")
        return cv2.imread(str(filename))[..., ::-1]  # type: ignore


class ImageCue(ImageResource):
    def __init__(self, name: str, threshold: float = 0.969):
        super().__init__(name)
        self.threshold = threshold

    def __repr__(self):
        return f"ImageCue({self.name}, {self.threshold})"

    def is_appeared_in(self, screenshot: npt.NDArray) -> bool:
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
        template = cv2.cvtColor(self.load(), cv2.COLOR_RGB2GRAY)
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        return max_val >= self.threshold
