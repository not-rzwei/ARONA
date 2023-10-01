import numpy as np

from src.constants.type import ScreenArea


def random_normal_distribution(number_range: tuple[float, float], std: float) -> float:
    mean = (number_range[0] + number_range[1]) / 2
    return np.random.normal(mean, std)


def random_point_in_area(area: ScreenArea, std: float = 10) -> tuple[int, int]:
    top_left, bottom_right = area
    x = random_normal_distribution((top_left[0], bottom_right[0]), std)
    y = random_normal_distribution((top_left[1], bottom_right[1]), std)
    x = np.clip(x, top_left[0], bottom_right[0])
    y = np.clip(y, top_left[1], bottom_right[1])
    return int(x), int(y)
