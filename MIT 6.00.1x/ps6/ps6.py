import string
import abc

WORDLIST_FILENAME = 'words.txt'


def load_words(file_name: str) -> list:
    """ Reads a file and returns a list of valid words - strings of lowercase letters. """
    print('Loading word list from file...')
    with open(file_name, 'r') as in_file:
        line = in_file.readline()
        word_list = line.split()
        print('  ', len(word_list), 'words loaded.')
    return word_list


def is_word(word_list, word) -> bool:
    """ Determines if word is a valid word, ignoring capitalization and punctuation """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


def get_story_string() -> str:
    """ Returns a joke in encrypted text. """
    with open("story.txt", "r") as f:
        story = str(f.read())
    return story


VALID_WORDS = load_words(WORDLIST_FILENAME)


class Message(metaclass=abc.ABCMeta):
    def __init__(self, text: str):
        """
        a Message object has three attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words
            self.shift_dict (dictionary created depending on the key. Initially set to None)
        """
        self.message_text = text
        self._valid_words = VALID_WORDS
        self._shift_dict = None

    @property
    def message_text(self):
        return self._message_text

    @message_text.setter
    def message_text(self, text: str):
        self._message_text = text

    @property
    def valid_words(self) -> list:
        """ Returns: a copy of self.valid_words """
        return self._valid_words[:]

    @property
    def shift(self):
        return self._shift

    @shift.setter
    @abc.abstractmethod
    def shift(self, shift):
        self._shift = shift

    @property
    def shift_dict(self):
        return self._shift_dict.copy()

    @abc.abstractmethod
    def build_shift_dict(self, shift):
        raise NotImplementedError

    @abc.abstractmethod
    def apply_shift(self, shift):
        raise NotImplementedError

    def helper_apply_shift(self) -> str:
        """ Returns the message text (string) in which every character is shifted corresponding to the shift """
        new_message = ''.join(
            (self.shift_dict[char] if char in self.shift_dict.keys() else char for char in self.message_text))
        return new_message


class CaesarPlaintextMessage(Message):
    def __init__(self, text: str, shift=None):
        """
        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encrypting_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)
        """
        Message.__init__(self, text)
        self.shift = shift
        self.build_shift_dict(self.shift)
        self._message_text_encrypted = self.apply_shift(self.shift)

    @property
    def shift(self):
        return self._shift

    @shift.setter
    def shift(self, shift):
        if shift is None:
            self._shift = 0
        elif type(shift) == int:
            if abs(shift) >= 26:
                shift %= 26
            if shift < 0:
                shift = 26 - abs(shift)
            self._shift = shift
        else:
            raise ValueError  # Shift should be an int

    @property
    def message_text_encrypted(self):
        return self._message_text_encrypted

    def build_message_text_encrypted(self, shift):
        self.shift = shift
        self._message_text_encrypted = self.apply_shift(self.shift)

    def build_shift_dict(self, shift):
        """
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift.
        """
        self.shift = shift
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        self._shift_dict = {char: lowercase[(lowercase.find(char) + shift) % len(lowercase)] for char in lowercase}
        self._shift_dict.update(
            {char: uppercase[(uppercase.find(char) + shift) % len(uppercase)] for char in uppercase})

    def apply_shift(self, shift):
        self.shift = shift
        self.build_shift_dict(self.shift)
        return self.helper_apply_shift()

    def change_shift(self, shift):
        """
        Changes self.shift and updates other attributes determined by shift
        (ie. self.shift_dict and message_text_encrypted).
        """
        self.shift = shift
        self.build_shift_dict(self.shift)
        self.build_message_text_encrypted(self.shift)


class SubstitutionPlaintextMessage(Message):
    def __init__(self, text: str, shift: str):
        Message.__init__(self, text)
        self.shift = shift
        self.build_shift_dict(self.shift)
        self.encrypting_dict = self.shift_dict
        self._message_text_encrypted = self.apply_shift(self.shift)

    @property
    def shift(self):
        return self._shift

    @shift.setter
    def shift(self, shift: str):
        if len(shift) == 26 and type(shift) is str:
            self._shift = shift
        else:
            raise ValueError  # shift should be a string 26 symbols long

    @property
    def message_text_encrypted(self):
        return self._message_text_encrypted

    def build_message_text_encrypted(self, shift):
        self.shift = shift
        self._message_text_encrypted = self.apply_shift(self.shift)

    # substitution cypher
    def build_shift_dict(self, in_dict: str):
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        self._shift_dict = {char: in_dict[i].lower() for char, i in zip(lowercase, range(26))}
        self._shift_dict.update({char: in_dict[i] for char, i in zip(uppercase, range(26))})

    def apply_shift(self, shift):
        self.shift = shift
        self.build_shift_dict(self.shift)
        return self.helper_apply_shift()

    def change_shift(self, shift):
        """
        Changes self.shift and updates other attributes determined by shift
        (ie. self.shift_dict and message_text_encrypted).
        """
        self.shift = shift
        self.build_shift_dict(self.shift)
        self.build_message_text_encrypted(self.shift)


class CiphertextMessage(CaesarPlaintextMessage):
    def __init__(self, text):
        """
        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        """
        Message.__init__(self, text)

    def decrypt_message(self):
        """
        Returns: a tuple of the first best shift value used to decrypt the message
        and the decrypted message text using that shift value
        """
        key_guessed_counter = {}
        for key in range(26):
            try_message = self.apply_shift(26 - key)
            message_list = try_message.split(' ')
            for word in message_list:
                if is_word(self.valid_words, word):
                    key_guessed_counter[key] = key_guessed_counter.get(key, 0) + 1
        right_key = max(key_guessed_counter, key=key_guessed_counter.get)
        return right_key, self.apply_shift(26 - right_key)


mes = CaesarPlaintextMessage("Hello, world!")
print(mes.apply_shift(27))


# Example test case (CaesarPlaintextMessage)
plaintext = CaesarPlaintextMessage('hello', 2)
print('Expected Output: jgnnq')
print('Actual Output:', plaintext.message_text_encrypted)
print()

# Example test case (CiphertextMessage)
ciphertext = CiphertextMessage('vgzq')
print('Expected Output:', (12, 'june'))
print('Actual Output:', ciphertext.decrypt_message())

# Example test case (SubstitutionMessage)
substitutiontext = SubstitutionPlaintextMessage("Hello", "JTREKYAVOGDXPSNCUIZLFBMWHQ")
print("Expected Output:", "VKXXN".title())
print("Actual Output:", substitutiontext.message_text_encrypted)


def decrypt_story():
    story = CiphertextMessage(get_story_string())
    return story.decrypt_message()
