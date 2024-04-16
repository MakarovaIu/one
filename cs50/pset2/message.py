# base class Message for other cypher classes

import abc


class Message(metaclass=abc.ABCMeta):

    def __init__(self, text: str, language):
        self.message_text = text

        self.language = language
        self.lowercase = self.language.lowercase
        self.uppercase = self.language.uppercase
        self.SHIFT_MAX = self.language.shift_len

        self._shift = None
        self._shift_dict = None
        self._message_text_encrypted = None

    @property
    def message_text(self):
        return self._message_text

    @message_text.setter
    def message_text(self, text: str):
        self._message_text = text

    @property
    def shift(self):
        return self._shift

    @shift.setter
    @abc.abstractmethod
    def shift(self, shift):
        self._shift = shift

    @property
    def message_text_encrypted(self):
        """ is used to get the message text after applying the shift in self.build_message_text_encrypted"""
        return self._message_text_encrypted

    def build_message_text_encrypted(self, shift):
        self._message_text_encrypted = self.apply_shift(shift)

    @property
    def shift_dict(self):
        return self._shift_dict.copy()

    @abc.abstractmethod
    def build_shift_dict(self, shift):
        raise NotImplementedError

    def apply_shift(self, shift) -> str:
        """ Returns the message text (string) in which every character is shifted corresponding to the shift """
        self.shift = shift
        self.build_shift_dict(self.shift)
        new_message = ''.join(
            (self.shift_dict[char] if char in self.shift_dict.keys() else char for char in self.message_text))
        return new_message

    def change_shift(self, shift):
        """
        Changes self.shift and updates other attributes determined by shift
        (ie. self.shift_dict and message_text_encrypted).
        """
        self.shift = shift
        self.build_shift_dict(self.shift)
        self.build_message_text_encrypted(self.shift)
