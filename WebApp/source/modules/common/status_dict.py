from enum import Enum


class StatusDict(Enum):
    TRANSLATION_FETCHED = "TRANSLATION_FETCHED"
    REQUEST_SENT = "REQUEST_SENT"
    GENERAL_ERROR = "GENERAL_ERROR"
    INCORRECT_CREDENTIALS = "INCORRECT_CREDENTIALS"
    LOGGED_OUT = "LOGGED_OUT"
    REPEAT_PASSWORD = "REPEAT_PASSWORD"
    LOGIN_EXISTS = "LOGIN_EXISTS"
    ACCOUNT_CREATED = "ACCOUNT_CREATED"
    INCORRECT_TOKEN = "INCORRECT_TOKEN"

    def __eq__(self, other):
        if isinstance(other, Enum):
            return self.value == other.value
        return self.value == other

    def __str__(self):
        return str(self.value)


class TranslationStatusDict(Enum):
    READY = "READY"
    IN_PROGRESS = "IN_PROGRESS"

    def __str__(self):
        return str(self.value)
