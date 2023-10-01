from typing import Optional

from src.game.resource import ImageResource


class Page:
    """A Navigable Page in the Game"""

    def __init__(self, name: str):
        self.name = name
        self.links: list["Page"] = []
        self.parent: Optional["Page"] = None

    def __repr__(self):
        return f"Page({self.name})"

    def link(self, *pages: "Page"):
        for page in pages:
            if page not in self.links:
                page.parent = self
                page.links.append(self)
                self.links.append(page)

    @property
    def cue(self):
        return ImageResource(f"pages/{self.name.lower()}/LANDMARK.png")
