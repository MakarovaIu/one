"""
Power set of a set S is the set of all subsets of S, including the empty set and S itself.
S = {x, y, z} <=> P(S) = {{}, {x}, {y}, {z}, {x, y}, {x, z}, {y, z}, {x, y, z}}
|S| = n <=> |P(S)| = 2**n
"""
from pprint import pprint


def get_all_subsets_with_prints(some_list, toPrint=False):
    """
    Returns all subsets of size 0 - len(some_list) for some_list.
    This version of a function has prints and comments for understanding the algorythm.
    The number of subsets is 2**(len(some_list))
    """
    if len(some_list) == 0:
        # If the list is empty, return the empty list
        return [[]]
    subsets = []
    first_elt = some_list[0]
    rest_list = some_list[1:]
    if toPrint: print(f"{rest_list = }")
    # Strategy: Get all the subsets of rest_list. For each of those subsets, a full subset list will contain both
    # the original subset as well as a version of the subset that contains first_elt.
    # As far as we go to the base case we retrieve an empty list.
    # Then we clear subsets, retrieve first_elt of the prelast recursion cycle (which is the -1 elt of some_list).
    # We append empy list to subsets and append (in this case) -1 elt of some_list.
    # Then the next recursion step starts: we get -2 elt as first_elt, and we append it to each elt in previous
    # recursion cycle subset list. So we do until we get to elt 0 and so we get all the subsets.
    for partial_subset in get_all_subsets_with_prints(rest_list):
        subsets.append(partial_subset)
        if toPrint: print(f"Partial Subset: {partial_subset}")
        next_subset = partial_subset[:] + [first_elt]
        if toPrint: print(f"Next Subset: {next_subset}")
        subsets.append(next_subset)
        if toPrint: print(f"Subsets: {subsets}")
    if toPrint: print(f"Returning subsets: {subsets} \n")
    return subsets


def getAllSubsets(some_list):
    """
    The code is from MIT 6.00.2x.

    Returns all subsets of size 0 - len(some_list) for some_list.
    Same function as one above but more clear with no print and comments.
    The number of subsets is 2**(len(some_list))
    """
    if len(some_list) == 0:
        return [[]]
    subsets = []
    first_elt = some_list[0]
    rest_list = some_list[1:]
    for partial_subset in getAllSubsets(rest_list):
        subsets.append(partial_subset)
        next_subset = partial_subset[:] + [first_elt]
        subsets.append(next_subset)
    return subsets


def powerSet(items):
    """
    Generate all combinations of N items.
    Here we represent if we include an item or not as a binary number. As we need 2**N unique combinations
    we can take numbers from 0 to 2**N-1 to represent each combination.
    """
    N = len(items)
    # enumerate the 2**N possible combinations
    for i in range(2 ** N):
        combo = []
        # Iterate through each digit of a binary integer. If the bit is 1 we include the corresponding item.
        # As i is an integer we need to convert it to a binary one. By dividing it by all powers of 2 from 0 to N
        # and then getting the remainder we get digits of binary representation from right to left.
        for j in range(N):
            # test bit jth of integer i
            # i >> j is equivalent of i // 2**j
            if (i >> j) % 2 == 1:
                combo.append(items[j])
        yield combo


def power_set(items):
    """ Oneliner version of previous function. Found somewhere on the Internet. """
    for i in range(2 ** len(items)):
        # x >> y: returns x with the bits shifted to the right by y places. This is the same as //'ing x by 2**y.
        yield tuple(items[j] for j in range(len(items)) if (i >> j) % 2 == 1)


def yield_all_combos(items):
    """
    There is a list of items. Function yields all combos of how items can be distributed among two bags.
    The item can either go in one bag or another or none at all.
    """
    N = len(items)
    # enumerate the 3**N possible combinations
    for i in range(3 ** N):
        bag1, bag2 = [], []
        # get the representation of an integer as a trinary number as it depicts all possible combinations of items
        # going in either bag1, bag2 or none of the above.
        for j in range(N):
            # test bit jth of integer i
            if (i // 3 ** j) % 3 == 1:
                bag1.append(items[j])
            if (i // 3 ** j) % 3 == 2:
                bag2.append(items[j])
        yield bag1, bag2


def yieldAllCombos(items):
    """ Does the same as yield_all_combos, found somewhere on the Internet"""
    for bag1 in power_set(items):
        # produce a power set based on the objects from set that weren't in b1
        for bag2 in power_set([elem for elem in items if elem not in bag1]):
            yield bag1, bag2


def yieldAllCombosAnyBags(items, n_bags=2):
    """
    Does the same as yield_all_combos but on any number of bags (two be default).
    """
    for i in range((n_bags + 1) ** len(items)):
        bags = [[] for _ in range(n_bags + 1)]
        for j in range(len(items)):
            bags[(i // (n_bags + 1) ** j) % (n_bags + 1)].append(items[j])
        yield tuple(bags[1:])


if __name__ == '__main__':
    testList = [1, 3, 5]
    testLen = len(testList)
    test = get_all_subsets_with_prints(testList, toPrint=True)
    # print(f"{getAllSubsets(testList) = }")
    # print(f"{list(powerSet(testList)) = }")
    # print(f"{list(power_set(testList)) = }")
    #
    # print("yield_all_combos(testList) = ")
    # pprint(list(yield_all_combos(testList)))
    # print("yieldAllCombos(testList) = ")
    # pprint(list(yieldAllCombos(testList)))
    # print("yieldAllCombosAnyBags(testList) = ")
    # pprint(list(yieldAllCombosAnyBags(testList, n_bags=4)))

