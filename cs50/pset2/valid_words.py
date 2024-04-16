# Class of static methods used to read from a file and create a list of valid words.
# Also checks if a word is valid.
# load_words_from_one_string is used to read a file where all words are in one string. Default delimiter is a space.
# File example: words.txt
# load_words reads through a file where each word takes first (by default) place on a new string. I.e. litf-win.txt


class ValidWords:
    @staticmethod
    def load_words_from_one_string(file_name: str, delimiter=" ", printing=True) -> list:
        """ Reads a file where all words are in one string divided by spaces
        and returns a list of valid words - strings of lowercase letters. """
        if printing:
            print('Loading word list from file...')
        with open(file_name, 'r') as in_file:
            line = in_file.readline()
            word_list = line.split(delimiter)
            if printing:
                print('  ', len(word_list), 'words loaded.\n')
        return word_list

    @staticmethod
    def load_words(file_name: str, word_place=0, printing=True) -> list:
        """ Reads a file where one word takes one string and takes 1st place in it,
        and returns a list of valid words - strings of lowercase letters.  """
        if printing:
            print('Loading word list from file...')
        with open(file_name) as in_file:
            word_list = [line.split()[word_place].strip().lower() for line in in_file.readlines()]
            if printing:
                print('  ', len(word_list), 'words loaded.\n')
        return word_list

    @staticmethod
    def is_word(word_list, word) -> bool:
        """ Determines if word is a valid word, ignoring capitalization and punctuation """
        word = word.lower()
        word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
        return word in word_list
