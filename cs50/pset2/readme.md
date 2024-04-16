# cipher
### About
This is a set of programs one can use to cipher a message. 
It has implementation for caesar and substitution ciphers.

------
## Caesar
#### About
Supposedly, Caesar (yes, that Caesar) used to “encrypt” (i.e., conceal in a reversible way) 
confidential messages by shifting each letter therein by some number of places. 
For instance, he might write A as B, B as C, C as D, …, and, wrapping around alphabetically,
 Z as A. And so, to say HELLO to someone, Caesar might write IFMMP. 
 Upon receiving such messages from Caesar, recipients would have to “decrypt” 
 them by shifting letters in the opposite direction by the same number of places.

Unencrypted text is generally called plaintext. Encrypted text is generally called ciphertext. And the secret used is called a key.

| Plaintext | H | E | L | L | O |
| ------ | ------ | ------ | ------ | ------ | ------ |
| + key |	1	| 1 |	1 |	1 |	1 |
| = ciphertext |	I |	F |	M |	M |	P |

#### To use
To create a ciphertext create an object of `CaesarPlaintextMessage`, parsing text, language object and shift as int.
Then access the `message_text_encrypted` attribute of an object to get the ciphertext. 
If the shift is not an int `ShiftError` will be raised.

Also has implementation to decipher caesar ciphered message.
Create an object of `CiphertextMessage`, parsing text, language object and list of valid words.
Method `decrypt_message()` returns the tuple of key used to cipher and original text.
> english = Language(string.ascii_lowercase, string.ascii_uppercase)
>
> plaintext = CaesarPlaintextMessage('Hi, my name is Jhon', english, shift=8)
>
> print(plaintext.message_text_encrypted)

The output will be `Pq, ug vium qa Uqwv`

> VALID_WORDS = ValidWords.load_words_from_one_string('words.txt')
>
>ciphertext = CiphertextMessage('Pq, ug vium qa Uqwv', english, VALID_WORDS)
>
>print(ciphertext.decrypt_message()))

The output will be `(8, 'Hi, my name is Mion')`
____
## Substitution cipher
#### About
In a substitution cipher, we “encrypt” (i.e., conceal in a reversible way) a message 
by replacing every letter with another letter. 
To do so, we use a key: in this case, a mapping of each of the letters of the alphabet 
to the letter it should correspond to when we encrypt it. 
To “decrypt” the message, the receiver of the message would need to know the key, 
so that they can reverse the process: translating the encrypt text (generally called ciphertext) 
back into the original message (generally called plaintext).

A key, for example, might be the string NQXPOMAFTRHLZGECYJIUWSKDVB. 
This 26-character key means that A (the first letter of the alphabet) should be converted into N 
(the first character of the key), B (the second letter of the alphabet) should be converted into Q 
(the second character of the key), and so forth.

A message like HELLO, then, would be encrypted as FOLLE, replacing each of the letters 
according to the mapping determined by the key.

#### To use
To create a ciphertext create an object of `SubstitutionPlaintextMessage`, parsing text, language object and shift
either as a string or list of the same length as `Language.shift_len`, otherwise a `ShiftError` will be raised.
Then access the `message_text_encrypted` attribute of an object to get the ciphertext.

If you want different shift keys for lower and upper letters - parse a list or a tuple of two keys of the same length.
> substitutiontext = SubstitutionPlaintextMessage("Hello", english, "JTREKYAVOGDXPSNCUIZLFBMWHQ")
> 
>print(substitutiontext.message_text_encrypted)

The output will be `Vkxxn`
____
### Examples
Shows the usage of cipher classes

### Needed imports
`from valid_words import ValidWords`

`from language import Language`

`from caesar import CaesarPlaintextMessage, CiphertextMessage`

`from substitution import SubstitutionPlaintextMessage`

### Language module
Language object is used to determine letters in plaintext message and max shift length for this language.
Lowercase and uppercase letters can be either a string or a list. If length of lowercase letters differs from that of uppercase letters, one needs to provide shift and max shift length. 
Otherwise the ShiftError will be raised.

Example:
>import string 
>
> english = Language(string.ascii_lowercase, string.ascii_uppercase)

### Valid_words module
Class of static methods used to read from a file and create a list of valid words.
Also checks if a word is valid.
`load_words_from_one_string` is used to read a file where all words are in one string. Default delimiter is a space.
File example: _words.txt_. `load_words` reads through a file where each word takes first 
(by default, can be parsed as an argument) place on a new string. I.e. _litf-win.txt_

### Message
Message is an abstract class used by Caesar and Substitution modules.

