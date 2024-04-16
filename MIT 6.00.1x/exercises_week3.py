def odd_tuples(a_tup):
    """
    a_tup: a tuple
    returns: tuple, every other element of a_tup.
    """
    new_tuple = a_tup[::2]
    return new_tuple


test_tuple = ('I', 'am', 'a', 'test', 'tuple',)
print(odd_tuples(test_tuple))


def apply_to_each(list_to_change, function_on_list):
    """ applies function on every element of the list, mutating original list """
    for i in range(len(list_to_change)):
        list_to_change[i] = function_on_list(list_to_change[i])


test_list = [1, -4, 8, -9]
apply_to_each(test_list, lambda x: x + 1)
print(test_list)

new = test_list.sort()
print(new, test_list)


def remove_dups(list_1, list_2):
    for elem in list_1:
        if elem in list_2:
            list_1.remove(elem)


L1 = [1, 2, 3]
L2 = [0, 1, 2]
remove_dups(L1, L2)
print(L1)
# it didn't remove 2 for L1 cause python was iterating over an object that changed its size
# after the first iteration second object became the first

a = range(2)
print(list(a))
print(type(a))


def print_min_between_lists(list_1, list_2):
    list_of_min = []
    for elem in map(min, list_1, list_2):
        list_of_min.append(elem)
    print(list_of_min)


print_min_between_lists([1, 2, 3], [0, 1, 2])
print(tuple(test_list) + test_tuple)


animals = {'a': ['aardvark'], 'b': ['baboon'], 'c': ['coati']}
animals['d'] = ['donkey']
animals['d'].append('dog')
animals['d'].append('dingo')


def how_many(in_dict):
    """
    aDict: A dictionary, where all the values are lists.
    returns: int, how many values are in the dictionary.
    """
    counter = 0
    for animal in in_dict.values():
        counter += len(animal)
    return counter


def key_with_biggest_value(in_dict):
    """
    aDict: A dictionary, where all the values are lists.
    returns: The key with the largest number of values associated with it
    """
    biggest_animal_count = 0
    answer = None
    for key, animal in in_dict.items():
        if len(animal) >= biggest_animal_count:
            biggest_animal_count = len(animal)
            answer = key
    return answer


print(how_many(animals))
print(key_with_biggest_value(animals))


def fibonacci_with_dicts(num, in_dict):
    if num in in_dict:
        return in_dict[num]
    else:
        ans = fibonacci_with_dicts(num-1, in_dict) + fibonacci_with_dicts(num-2, in_dict)
        in_dict[num] = ans
        return ans


fibonacci_dict = {0: 1, 1: 1, 2: 2}
print(fibonacci_with_dicts(256, fibonacci_dict), fibonacci_dict)
print(fibonacci_with_dicts(5, fibonacci_dict), fibonacci_dict)