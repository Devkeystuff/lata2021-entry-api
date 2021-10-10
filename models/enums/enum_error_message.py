from enum import Enum


class ErrorMessage(Enum):
    OK = ''
    WRONG_API_KEY = 'wrong api key'
    WRONG_FILE_FORMAT = 'wrong file format'

    def __str__(self):
        return self.value

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))