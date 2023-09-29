from typing import List, Dict

from src.adapters.driver import DriverAdapter
from src.game.page import Page


class Navigator:
    """Manage the page navigation of the game"""

    pages: Dict[str, Page] = {}
    initial_page: Page

    def __init__(self, driver: DriverAdapter):
        self._driver = driver

    def register(self, initial: Page, pages: List[Page]):
        if initial not in pages:
            raise ValueError("Initial page must be in pages list")

        self.initial_page = initial

        for page in pages:
            self.pages[page.name] = page

    def find_path(self, destination: str) -> List[Page] | None:
        visited = set()
        path = []

        if destination not in self.pages:
            return None

        def dfs_search(current_page):
            visited.add(current_page)
            path.append(current_page)

            if current_page == self.pages[destination]:
                return path.copy()

            for linked_page in current_page.links:
                if linked_page not in visited:
                    result = dfs_search(linked_page)
                    if result:
                        return result
            path.pop()
            return None

        result_path = dfs_search(self.initial_page)

        if result_path:
            return result_path

        return None
