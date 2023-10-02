from collections import deque
from typing import List, Dict

from src.game.game_controller import GameController
from src.game.page import Page


class Navigator:
    """Manage the page navigation of the game"""

    def __init__(self, controller: GameController):
        self._controller = controller
        self.pages: Dict[str, Page] = {}
        self.current_page = Page("")
        self.history: List[Page] = []

    def register(self, *pages: Page):
        for page in pages:
            self.pages[page.name] = page

    def set_current_page(self, page: str):
        if page in self.pages:
            self.current_page = self.pages[page]

    def find_path(self, destination: str) -> deque[Page] | None:
        visited = set()
        path: deque[Page] = deque()

        if destination not in self.pages:
            return None

        def dfs_search(current_page) -> deque[Page] | None:
            visited.add(current_page.name)
            path.append(current_page)

            if current_page.name == self.pages[destination].name:
                return path.copy()

            for linked_page in current_page.links:
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

    def detect_page(self) -> Page | None:
        try:
            for page in self.pages.values():
                if self._controller.is_image_on_screen(page.cue):
                    return page
            return None
        except (AttributeError, FileNotFoundError, ValueError):
            return None

    def match_current_page(self) -> bool:
        try:
            return self._controller.is_image_on_screen(self.current_page.cue)
        except (AttributeError, FileNotFoundError, ValueError):
            return False

    def navigate_to(self, destination: str) -> bool:
        path = self.find_path(destination)

        if not path:
            return False

        if not self.match_current_page():
            return False

        path.popleft()

        for page in path:
            if not self._controller.tap_button(page.entrypoint, cache=True):
                return False

            if not self._controller.until_image_is_on_screen(page.cue, timeout=10):
                return False

            self.current_page = page
            self.history.append(page)

        return True
