""" Дана строка s.
Ищет в ней подстроку, где наибольшее количество подряд идущих одинаковых символов.
Выводит символ и длину последовательности.
Если таких несколько – выводит последнюю."""

from itertools import groupby

data = "aaabbccccaaaab"


def split_as_groups(iterable):
    groups = []
    for k, g in groupby(iterable):
        groups.append(list(g))      # Store group iterator as a list
    return groups


def find_max_len_sublist(iterable):
    max_list = max(reversed(iterable), key=len)  # reversed as we need last occurrence, otherwise we get 1st occurrence
    max_list_len = len(max_list)
    return max_list, max_list_len


if __name__ == '__main__':
    user_input = input()
    # can use variable 'data' instead of user_input
    iter_groups = split_as_groups(user_input)
    max_list, max_list_len = find_max_len_sublist(iter_groups)
    max_symbol = max_list[0]
    print(max_symbol)
    print(max_list_len)
