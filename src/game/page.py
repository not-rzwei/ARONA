from typing import Optional

from src.game.resource import ImageCue


class Page:
    """A Navigable Page in the Game"""

    parent: Optional["Page"] = None
    children: list["Page"] = []

    def __repr__(self):
        return f"Page({self.name})"

    def __init__(self, name: str):
        self.name = name

    def link(self, *pages: "Page"):
        for page in pages:
            if page not in self.children:
                page.parent = self
                self.children.append(page)

    @property
    def cue(self) -> ImageCue:
        return ImageCue(f"pages/{self.name.lower()}/LANDMARK.png")
