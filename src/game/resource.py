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
        self.area = ((0, 0), (0, 0))

    def __repr__(self):
        return f"ImageResource({self.name})"

    def load(self) -> npt.NDArray:
        """Load RGB image from resource folder"""
        filename = RES_FOLDER / self.name
        if not filename.exists():
            raise FileNotFoundError(f"File {filename} not found")
        return cv2.imread(str(filename))[..., ::-1]  # type: ignore


class ButtonResource(ImageResource):
    def __init__(self, name: str):
        super().__init__(name)
        self.is_tapped = False
