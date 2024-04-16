def count_vowels(in_string):
    """ counts up the number of vowels contained in the string """
    i = 0
    for char in in_string:
        if char in ["a", "e", 'i', "o", "u"]:
            i += 1

    print("Number of vowels: ", i)


def count_a_bob(in_string):
    """ prints the number of times the string 'bob' occurs in the string """
    counter = 0
    for i in range(0, len(in_string) - 2):
        if 'bob' == in_string[i:i + 3]:
            counter += 1
    print("Number of times bob occurs is: ", counter)


def longest_alphabetical_ordered_substring(in_string):
    """ returns the longest substring of the string in which the letters occur in alphabetical order """
    prev_value = ""
    prev_substr = ""
    substr = ""

    for i in range(0, len(in_string)):
        current_value = in_string[i]
        if current_value >= prev_value:
            substr += current_value
        else:
            substr = current_value
        if len(substr) > len(prev_substr):
            prev_substr = substr
        prev_value = current_value
    return prev_substr


str_ps1 = type('string_subclass_4_ps1', (str,), {
    'vowels': property(lambda s: sum(c in 'aeiou' for c in s)),
    'bobs': property(lambda s: s.replace('b', 'bb').count('bob')),
    'alpha_up': property(lambda s: max((''.join(j + ' ' * (i < j) for i, j in zip(s[1:] + s, s))).split(), key=len))
})

aStr = 'abcdefghijklmnopqrstuvwxyz'

if __name__ == '__main__':

    print("Longest substring in alphabetical order is:", longest_alphabetical_ordered_substring(aStr))

    s = str_ps1(aStr)
    print("Number of vowels:", s.vowels)
    print("Longest substring in alphabetical order is:", s.alpha_up)
    s = "alpha"
    print(f"{list(zip(s, s[1:] + s)) = }")
    # for i, j in zip(s, s[1:] + s):
    #     print(f"{i, j, i > j=}")
    #     print(''.join(i + '_' * (i > j)))
