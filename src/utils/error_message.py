from enum import StrEnum


class ErrorMessage(StrEnum):
    def fmt(self, *args) -> str:
        return self.value.format(*args)
