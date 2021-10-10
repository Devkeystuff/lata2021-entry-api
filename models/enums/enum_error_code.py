from enum import Enum


class ErrorCode(Enum):
    OK = 0
    WRONG_API_KEY = 400
    WRONG_FILE_FORMAT = 401

    def __str__(self):
        return self.value

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))