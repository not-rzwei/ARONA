from typing import List, Dict

from src.game.game_controller import GameController
from src.game.page import Page


class Navigator:
    """Manage the page navigation of the game"""

    def __init__(self, controller: GameController):
        self._controller = controller
        self.pages: Dict[str, Page] = {}
        self.current_page = Page("")

    def register(self, *pages: Page):
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
