# Implements class for substitution cypher.
# To create a cyphertext create an object of SubstitutionPlaintextMessage, parsing text, language object and shift
# either as a string or list of the same length as Language.shift_len or as a list or tuple of two strings/lists.
# Each of these two strings/lists should be of the same length as Language.shift_len.
# Then access the message_text_encrypted attribute of an object to get the cyphertext.


from message import Message
from errors import ShiftError


class SubstitutionPlaintextMessage(Message):
    def __init__(self, text: str, language, shift=None):
        Message.__init__(self, text, language)
        if shift is None:
            raise ShiftError
        self.shift = shift
        if self._shift_type == "case_non_sensitive":
            self.build_shift_dict(self.shift)
            self.build_message_text_encrypted(self.shift)
        if self._shift_type == "case_sensitive":
            self.build_case_sensitive_shift_dict(self.shift)
            self.build_message_text_encrypted(self.shift)

    @property
    def shift(self):
        return self._shift

    @shift.setter
    def shift(self, shift: str):
        if (type(shift) is str or type(shift) is list) and len(shift) == self.SHIFT_MAX:
            self._shift = shift
            self._shift_type = "case_non_sensitive"
        elif type(shift) is tuple or type(shift) is list:
            if len(shift[0]) == self.SHIFT_MAX and type(shift[0]) is str and type(shift[1]) is str:
                self._shift = shift
                self._shift_type = "case_sensitive"
        else:
            raise ShiftError(f"Shift should be a one or two string/list {self.SHIFT_MAX} symbols long")

    def build_message_text_encrypted(self, shift):
        if self._shift_type == "case_non_sensitive":
            self._message_text_encrypted = self.apply_shift(shift)
        if self._shift_type == "case_sensitive":
            self._message_text_encrypted = self.apply_case_sensitive_shift(shift)

    def build_shift_dict(self, shift: str):
        lowercase = self.language.lowercase
        uppercase = self.language.uppercase
        self._shift_dict = {char: shift[i].lower() for char, i in zip(lowercase, range(self.SHIFT_MAX))}
        self._shift_dict.update({char: shift[i].upper() for char, i in zip(uppercase, range(self.SHIFT_MAX))})

    def build_case_sensitive_shift_dict(self, shift):
        lowercase = self.language.lowercase
        uppercase = self.language.uppercase
        self._shift_dict = {char: shift[0][i] for char, i in zip(lowercase, range(self.SHIFT_MAX))}
        self._shift_dict.update({char: shift[1][i] for char, i in zip(uppercase, range(self.SHIFT_MAX))})

    def apply_case_sensitive_shift(self, shift) -> str:
        """ Returns the message text (string) in which every character is shifted corresponding to the shift """
        self.shift = shift
        self.build_case_sensitive_shift_dict(self.shift)
        new_message = ''.join(
            (self.shift_dict[char] if char in self.shift_dict.keys() else char for char in self.message_text))
        return new_message


