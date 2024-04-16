# Here are some examples

# -*- coding: utf-8 -*-

import string

from valid_words import ValidWords
from language import Language
from caesar import CaesarPlaintextMessage, CiphertextMessage
from substitution import SubstitutionPlaintextMessage

# creating lists of valid words and language objects
VALID_WORDS = ValidWords.load_words_from_one_string('words.txt')
english = Language(string.ascii_lowercase, string.ascii_uppercase)

russian_alphabet = "абвгдеёжзийклмнопрстуфхцчшщьыъэюя"
russian = Language(russian_alphabet, russian_alphabet.upper())
VALID_WORDS_RU = ValidWords.load_words("pldf-win.txt")
VALID_WORDS_RU.append(ValidWords.load_words("litf-win.txt"))

# create a message without a key
mes = CaesarPlaintextMessage("AbcdefG!", english)
print(f"Here is an original message:", mes.message_text)
# apply key = -1
mes.build_message_text_encrypted(-1)
print(f"Same message after applying key -1:", mes.message_text_encrypted, "\n")


print("Example test case for CaesarPlaintextMessage")
plaintext = CaesarPlaintextMessage('Hi, my name is Jhon', english, shift=8)
print("Input:", plaintext.message_text, "\n key:", plaintext.shift)
print('Output:', plaintext.message_text_encrypted, "\n")

print("Пример для русского языка")
plaintext_ru = CaesarPlaintextMessage("Привет, я пример на русском языке", russian, shift=1)
print("Ввод:", plaintext_ru.message_text, "\n ключ: ", plaintext_ru.shift)
print("Вывод:", plaintext_ru.message_text_encrypted, "\n")

print("Example test case for CiphertextMessage")
ciphertext = CiphertextMessage('Pq, ug vium qa Uqwv', english, VALID_WORDS)
print("Input:", ciphertext.message_text)
ciphertext_decrypted = ciphertext.decrypt_message()
print('Output:', ciphertext_decrypted[1], "\n key:", ciphertext_decrypted[0], "\n")

print("Пример дешифровки")
ciphertext_ru = CiphertextMessage("Рсйгёу, а рсйнёс об сфттлпн аиълё", russian, VALID_WORDS_RU)
print("Input:", ciphertext_ru.message_text)
ciphertext_decrypted_ru = ciphertext_ru.decrypt_message()
print('Output:', ciphertext_decrypted_ru[1], "\n key:", ciphertext_decrypted_ru[0], "\n")


print("Example test case SubstitutionMessage")
substitutiontext = SubstitutionPlaintextMessage("Hello", english, "JTREKYAVOGDXPSNCUIZLFBMWHQ")
print("Input:", substitutiontext.message_text, "\n key:", substitutiontext.shift)
print('Output:', substitutiontext.message_text_encrypted, "\n")

print("Example test case SubstitutionMessage with different keys for lower and uppercases")
subs = SubstitutionPlaintextMessage("Abcde", english, ("JTREKYAVOGDXPSNCUIZLFBMWHQ".lower(), "ZAQWSXCDERFVBGTYHNMJUIKLOP"))
print("Input:", subs.message_text, "\n key:", subs.shift)
print('Output:', subs.message_text_encrypted, "\n")


def get_story_string() -> str:
    """ Returns a joke in encrypted text. """
    with open("story.txt", "r") as f:
        story = str(f.read())
    return story


def decrypt_story(story):
    story = CiphertextMessage(story, english, VALID_WORDS)
    return story.decrypt_message()


story = get_story_string()
decrypted_story = decrypt_story(story)
print(f"Here is an encrypted story:\n", story)
print(f"Here is a decrypted story:\n", decrypted_story[1], "\n", "The key to encrypt it was", decrypted_story[0], "\n")
