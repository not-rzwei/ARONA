from collections import deque
from typing import List, Dict

from src.game.game_controller import GameController
from src.game.page import Page
from src.game.resource import ButtonResource


class Navigator:
    """Manage the page navigation of the game"""

    def __init__(self, controller: GameController):
        self._controller = controller
        self.pages: Dict[str, Page] = {}
        self.current_page = Page("")
        self.history: List[Page] = []
        self.back_button = ButtonResource("")

    def register(self, *pages: Page):
        for page in pages:
            self.pages[page.name] = page

    def set_back_button(self, back_button: ButtonResource):
        self.back_button = back_button

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

    def ancestor_count(self, page: Page) -> int:
        if page.parent is None:
            return 0
        return 1 + self.ancestor_count(page.parent)

    def navigate_to(self, destination: str) -> bool:
        path = self.find_path(destination)

        if not path:
            return False

        # If the current page is the root page, tap the center of the screen
        # to dismiss the root page idle screen
        if not self.current_page.parent:
            self._controller.tap_center_screen()
            self._controller.until_image_is_on_screen(
                self.current_page.cue, timeout=1, delay=0.3
            )

        if not self.match_current_page():
            return False

        cur_page_ancestor_count = self.ancestor_count(self.current_page)
        dest_page_ancestor_count = self.ancestor_count(self.pages[destination])
        if (
            cur_page_ancestor_count >= dest_page_ancestor_count
            and len(path) >= cur_page_ancestor_count + dest_page_ancestor_count
        ):
            for _ in range(self.ancestor_count(self.current_page)):
                path.popleft()
        else:
            path.popleft()

        for page in path:
            entrypoint = page.entrypoint

            if self.back_button and self.current_page.parent == page:
                entrypoint = self.back_button

            if not self._controller.tap_button(entrypoint, cache=True):
                return False

            if not self._controller.until_image_is_on_screen(page.cue, timeout=10):
                return False

            self.current_page = page
            self.history.append(page)

        return True
