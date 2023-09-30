from typing import List, Dict

import numpy.typing as npt

from src.adapters.driver import DriverAdapter
from src.game.page import Page


class Navigator:
    """Manage the page navigation of the game"""

    pages: Dict[str, Page] = {}
    current_page: Page

    def __init__(self, device: DriverAdapter):
        self._device = device

    def register(self, pages: List[Page]):
        for page in pages:
            self.pages[page.name] = page

    def set_current_page(self, page: str):
        if page in self.pages:
            self.current_page = self.pages[page]

    def find_path(self, destination: str) -> List[Page] | None:
        visited = set()
        path = []

        if destination not in self.pages:
            return None

        def dfs_search(current_page) -> List[Page] | None:
            visited.add(current_page.name)
            path.append(current_page)

            if current_page.name == self.pages[destination].name:
                return path.copy()

            for linked_page in current_page.children:
                if linked_page.name not in visited:
                    result = dfs_search(linked_page)
                    if result:
                        return result
            path.pop()
            return None

        result_path = dfs_search(self.current_page)

        if result_path:
            return result_path

        return None

    def detect_page(self, screenshot: npt.NDArray) -> Page | None:
        try:
            for page in self.pages.values():
                if page.cue.appear_in(screenshot):
                    return page
            return None
        except (AttributeError, FileNotFoundError, ValueError):
            return None
