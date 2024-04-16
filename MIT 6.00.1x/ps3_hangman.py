# Hangman game

import random, string, os

WORDLIST_FILENAME = "words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.\n")
    return wordlist

def chooseWord(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = loadWords()

def isWordGuessed(secretWord, lettersGuessed):
    """
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: boolean, True if all the letters of secretWord are in lettersGuessed; False otherwise

    Takes every element in set of secretWord and return True if it's in lettersGuessed.
    Then returns True if all element of secretWord are in lettersGuessed
    """
    return all(elem in lettersGuessed for elem in set(secretWord))

def getGuessedWord(secretWord, lettersGuessed):
    """
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters and underscores that represents
      what letters in secretWord have been guessed so far.
    """
    return ''.join(char if char in lettersGuessed else '_ ' for char in secretWord)

def getAvailableLetters(lettersGuessed):
    """
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters that represents what letters have not
      yet been guessed.
    """
    return ''.join((char + ' ') for char in string.ascii_lowercase if char not in lettersGuessed)
    

def hangman(secretWord):
    """
    secretWord: string, the secret word to guess.
    Starts up an interactive game of Hangman.
    """
    print("\nWelcome to the game Hangman!\n"
          "I am thinking of a word that is", len(secretWord), "letters long."
          "\n------------"
          "\nTo exit print 'quit'")
    guess_counter = 8
    turn_counter = "*"
    lettersGuessed = []
    flag_positive = True

    while flag_positive:
        print("-----", turn_counter, "-----")
        print("You have", guess_counter, "guesses left")
        print("Available letters: ", getAvailableLetters(lettersGuessed))
        turn_counter += '*'
        user_guess = input("Please guess a letter: ").lower()
        if user_guess == 'quit':
            print("Quitting")
            quit()
        if user_guess in lettersGuessed:
            print("Oops! You've already guessed that letter:", user_guess)
            continue
        if user_guess not in string.ascii_lowercase or len(user_guess) > 1:
            print("One letter per turn. Try again.")
            continue
        if user_guess in secretWord:
            lettersGuessed.append(user_guess)
            print("Good guess:", getGuessedWord(secretWord, lettersGuessed))
            if isWordGuessed(secretWord, lettersGuessed):
                print("------------", "\nCongratulations, you won!")
                good_end()
                flag_positive = False
        else:
            guess_counter -= 1
            lettersGuessed.append(user_guess)
            print("Oops! That letter is not in my word:", getGuessedWord(secretWord, lettersGuessed))
        if guess_counter == 0:
            print("------------", "\nSorry, you ran out of guesses. The word was", secretWord)
            bad_end()
            flag_positive = False

def bad_end():
    print("\n  _______"
          "\n |/      |"
          "\n |      (_)"
          "\n |      \\|/"
          "\n |       |"
          "\n |      / \\"
          "\n |"
          "\n_|___"
          "\n")

def good_end():
    print("\n                                 .''."
          "\n       .''.             *''*    :_\\/_:     . "
          "\n      :_\\/_:   .    .:.*_\\/_*   : /\\ :  .'.:.'."
          "\n  .''.: /\\ : _\\(/_  ':'* /\\ *  : '..'.  -=:o:=-"
          "\n :_\\/_:'.:::. /)\\*''*  .|.* '.\\'/.'_\\(/_'.':'.'"
          "\n : /\\ : :::::  '*_\\/_* | |  -= o =- /)\\    '  *"
          "\n  '..'  ':::'   * /\\ * |'|  .'/.\\'.  '._____"
          "\n      *        __*..* |  |     :      |.   |' .---\"|"
          "\n       _*   .-'   '-. |  |     .--'|  ||   | _|    |"
          "\n    .-'|  _.|  |    ||   '-__  |   |  |    ||      |"
          "\n    |' | |.    |    ||       | |   |  |    ||      |"
          "\n ___|  '-'     '    \"\"       '-'   '-.'    '`      |____"
          "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
          "\n")


user_ready = True
if __name__ == "__main__":
    while user_ready:
        secretWord = chooseWord(wordlist).lower()
        hangman(secretWord)
        ask_if_rdy = input("If you want to exit print 'quit' at any step."
                           "\nPress enter to continue\n")
        if ask_if_rdy == 'quit':
            user_ready = False
