class Page:
    """A Navigable Page in the Game"""

    links: list["Page"] = []

    def __repr__(self):
        return f"Page({self.name})"

    def __init__(self, name: str):
        self.name = name

    def link(self, page: "Page"):
        if page not in self.links:
            self.links.append(page)
