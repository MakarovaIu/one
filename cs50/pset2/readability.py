# Program that computes the approximate grade level needed to comprehend some text
# It uses the Coleman-Liau index readability test.
# The Coleman-Liau index of a text is designed to output what (U.S.) grade level is needed to understand the text.
# The formula is:
# index = 0.0588 * L - 0.296 * S - 15.8
# where L is the average number of letters per 100 words in the text,
# and S is the average number of sentences per 100 words in the text.
# Any sequence of characters that ends with a . or a ! or a ? is considered to be a sentence.
# See text examples at https://cs50.harvard.edu/x/2020/psets/2/readability or in readme

import re


class Readability:
    def __init__(self, text: str):

        self.text = re.sub("[^\w?.! ]", "", text)  # gets rid of everything except letters, digits and '.', '?' or '!'
        self.text_valid = self.text_check()
        if self.text_valid:
            self.sentences = self.split_sentences()
            self.sentences_num = len(self.sentences)
            self.words = self.split_words()
            self.word_num = len(self.words)
            self.letters_num = len(re.sub(r"[\W_]", "", self.text))
            self.L = None
            self.S = None
        else:
            self.sentences = None
            self.sentences_num = 0
            self.words = None
            self.word_num = 0
            self.letters_num = 0
            self.L = None
            self.S = None

    def text_check(self):
        if not self.text:
            return False
        return True

    def split_sentences(self):
        return list(filter(None, re.split(r"[.!?]", self.text)))  # filter gets rid of the last empty string

    def split_words(self):
        return [word for sentence in self.sentences for word in sentence.split()]

    def coleman_liau_index(self):
        if not self.text_valid:
            return None
        # L is the average number of letters per 100 words in the text
        self.L = round(self.letters_num * 100 / self.word_num, 2)
        # S is the average number of sentences per 100 words in the text.
        self.S = round(self.sentences_num * 100 / self.word_num, 2)
        return int(round(0.0588 * self.L - 0.296 * self.S - 15.8, 0))

    def index_output(self):
        if not self.coleman_liau_index():
            return "No text found"
        if self.coleman_liau_index() < 1:
            return "Before Grade 1"
        if self.coleman_liau_index() >= 16:
            return "Grade 16+"
        if 1 <= self.coleman_liau_index() < 16:
            return f"Grade {self.coleman_liau_index()}"
        else:
            return "Something went wrong"

    def text_info(self):
        return f"Text: {self.text}\n" \
               f"Sentences: {self.sentences}\n" \
               f"Sentences number: {self.sentences_num}\n" \
               f"Words: {self.words}\n" \
               f"Words number: {self.word_num}\n" \
               f"Letters number: {self.letters_num}"


if __name__ == "__main__":
    print("Type 'quit' or break to 'quit'")
    while True:
        text = input("Text: ")
        if text == "quit" or text == "break":
            break
        t = Readability(text)
        print(t.text_info())
        print(t.index_output())

