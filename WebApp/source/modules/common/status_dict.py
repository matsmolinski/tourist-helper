from enum import Enum


class StatusDict(Enum):
    REQUEST_SENT = "REQUEST_SENT"
    GENERAL_ERROR = "GENERAL_ERROR"

    def __eq__(self, other):
        if isinstance(other, Enum):
            return self.value == other.value
        return self.value == other

    def __str__(self):
        return str(self.value)
