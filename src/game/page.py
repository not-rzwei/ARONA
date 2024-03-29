from typing import Optional

from src.game.resource import ImageResource, ButtonResource


class Page:
    """A Navigable Page in the Game"""

    def __init__(self, name: str):
        self.name = name
        self.links: list["Page"] = []
        self.parent: Optional["Page"] = None

        self.cue = ImageResource(f"pages/{self.name.lower()}/LANDMARK.png")
        self.entrypoint = ButtonResource(f"pages/{self.name.lower()}/ENTRYPOINT.png")

    def __repr__(self):
        return f"Page({self.name})"

    def link(self, *pages: "Page"):
        for page in pages:
            if page not in self.links:
                page.parent = self
                page.links.append(self)
                self.links.append(page)
