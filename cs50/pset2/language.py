# class used to choose parameters for Message and it's subclasses

from errors import ShiftError


class Language:

    def __init__(self, lowercase, uppercase):
        self.lowercase = lowercase
        self.uppercase = uppercase
        if len(self.lowercase) == len(self.uppercase):
            self.shift_len = len(self.lowercase)
        else:
            raise ShiftError("Lowercase and uppercase should be the same length")

