import regex
import re

s = "abababa"
t = "aba"


def find_occurrence(main_string, sub):
    """ Finds all occurrences of a substring in the main_string string, including overlapping. """
    counter = 0
    for i in range(len(main_string)):
        if main_string.startswith(sub, i):
            counter += 1
    return counter


def count_overlapping(text, search_for):
    return len(regex.findall(search_for, text, overlapped=True))


def substring_replacement_counter(main_string: str, old: str, new: str):
    """ Returns number of cycles it takes to replace all old substrings with new substrings.
     If it's more than 1000 then returns 'Impossible'. """
    counter = 0
    while counter < 1000:
        if old in main_string:
            main_string = main_string.replace(old, new)
            counter += 1
        else:
            return counter
    else:
        return "Impossible"


two_cats_exp = r".*(cat).*\1"
cat_as_a_word = r".*\b(cat)\b.*"
z_3symbols_z = r".*z.{3}z"
backslash = r".*\\"
tandem_repeat = r".*\b(.+)\1\b"
old_word = "human"
new_word = "computer"
old_pattern = r"\ba+\b"
new_pattern = "argh"
switch_first_two_letters_old = r"\b(\w)(\w)(\w*)\b"
switch_first_two_letters_new = r"\2\1\3"
duplicate_letters = r"(\w)(\1+)"
duplicate_letters_new = r"\1"


def re_exercises(func):
    """ Decorator. Takes user input until an empty string is entered.
     Uses func to work with the input and to append strings to res list.
     Returns res list. """
    def inner(*args, **kwargs):
        res = []
        while True:
            line = input()
            line = line.rstrip()
            func(*args, line, res, **kwargs)
            if not line:
                break
        return res
    return inner


@re_exercises
def find_pattern(pattern, line, res):
    """ Finds given pattern and returns list of lines where pattern was found. """
    if re.match(pattern, line):
        res.append(line)


@re_exercises
def replace_pattern(old, new, line, res, **kwargs):
    """ Returns list of string with old to new substitution. """
    new_string = re.sub(old, new, line, **kwargs)
    res.append(new_string)


def result_output(func, *args, **kwargs):
    for result in func(*args, **kwargs):
        print(result)


if __name__ == '__main__':

    # print(find_occurrence(s, t))
    # print(count_overlapping(s, t))
    #
    # main, sub, new = input(), input(), input()
    # print(substring_replacement_counter(main, sub, new))

    # result_output(find_pattern, tandem_repeat)

    # result_output(replace_pattern, old_word, new_word)

    # result_output(replace_pattern, old_pattern, new_pattern, count=1, flags=re.IGNORECASE)

    # result_output(replace_pattern, switch_first_two_letters_old, switch_first_two_letters_new)

    result_output(replace_pattern, duplicate_letters, duplicate_letters_new)

    pass
