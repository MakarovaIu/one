# Implementation class for Caesar cypher.
# To create a cyphertext create an object of CaesarPlaintextMessage, parsing text, language object and shift as int.
# Then access the message_text_encrypted attribute of an object to get the cyphertext.
#
# Also has implementation to decypher caesar cyphered message.
# Create an object of CiphertextMessage, parsing text, language object and list of valid words.
# Method decrypt_message() returns the tuple of key used to cypher and original text.


from message import Message
from valid_words import ValidWords
from errors import ShiftError


class CaesarPlaintextMessage(Message):
    def __init__(self, text: str, language, shift=None):
        """
        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encrypting_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)
        """
        Message.__init__(self, text, language)

        self.shift = shift
        self.build_shift_dict(self.shift)
        self.build_message_text_encrypted(self.shift)

    @property
    def shift(self):
        return self._shift

    @shift.setter
    def shift(self, shift):
        if shift is None:
            self._shift = 0
        elif type(shift) == int:
            if abs(shift) >= self.SHIFT_MAX:
                shift %= self.SHIFT_MAX
            if shift < 0:
                shift = self.SHIFT_MAX - abs(shift)
            self._shift = shift
        else:
            raise ShiftError("Shift should be an int")

    def build_shift_dict(self, shift):
        """
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift.
        """
        lowercase = self.language.lowercase
        uppercase = self.language.uppercase
        self._shift_dict = {char: lowercase[(lowercase.find(char) + shift) % self.SHIFT_MAX] for char in lowercase}
        self._shift_dict.update(
            {char: uppercase[(uppercase.find(char) + shift) % self.SHIFT_MAX] for char in uppercase})


class CiphertextMessage(CaesarPlaintextMessage):
    def __init__(self, text, language, valid_words: list):
        """
        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        """
        super().__init__(text, language)
        self._valid_words = valid_words

    @property
    def valid_words(self) -> list:
        """ Returns: a copy of self.valid_words """
        return self._valid_words[:]

    def decrypt_message(self):
        """
        Returns: a tuple of the first best shift value used to decrypt the message
        and the decrypted message text using that shift value
        """
        key_guessed_counter = {}
        for key in range(self.SHIFT_MAX):
            try_message = self.apply_shift(self.SHIFT_MAX - key)
            message_list = try_message.split(' ')
            for word in message_list:
                if ValidWords.is_word(self.valid_words, word):
                    key_guessed_counter[key] = key_guessed_counter.get(key, 0) + 1
        right_key = max(key_guessed_counter, key=key_guessed_counter.get)
        return right_key, self.apply_shift(self.SHIFT_MAX - right_key)

