from enum import Enum


class ErrorMessage(Enum):
    def fmt(self, *args) -> str:
        return self.value.format(*args)
