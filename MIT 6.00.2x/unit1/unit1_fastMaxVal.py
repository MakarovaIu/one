from unit1_food import Food, buildMenu
from unit1_maxVal import maxVal
import random


def buildLargeMenu(numItems, maxVal, maxCost):
    items = []
    for i in range(numItems):
        items.append(Food(str(i),
                          random.randint(1, maxVal),
                          random.randint(1, maxCost)))
    return items


def fastMaxVal(toConsider, avail, memo={}, toPrint=False):
    """
    Assumes toConsider a list of subjects, avail a weight, memo is supplied by recursive calls
    Key of memo is a tuple:
    ◦ (items left to be considered, available weight)
    ◦ Items left to be considered represented by len(toConsider)
    Returns a tuple of the total value of a solution to the 0/1 knapsack problem and the subjects of that solution

    We can represent finding maxVal as a binary tree where each node consist of decision to take or not take an item.
    So we get an info: items taken, items left, value, remaining calories.
    When we get the same items left (represented as len) and remaining calories, we run into a situation where
    we went through the same conditions but may have gotten different values. We choose max value we could get
    for (len(toConsider), avail) and store remaining calories and items taken as value in memo.
    """
    if (len(toConsider), avail) in memo:
        result = memo[(len(toConsider), avail)]
        if toPrint: print(f"{toConsider, (len(toConsider), avail)} accessed memo")
    elif toConsider == [] or avail == 0:
        result = (0, ())
        if toPrint: print("Zero recursion lvl")
    elif toConsider[0].getCost() > avail:
        # Explore right branch only
        if toPrint: print(f"Can't take {toConsider[0]} cause {avail=}")
        result = fastMaxVal(toConsider[1:], avail, memo, toPrint)
    else:
        nextItem = toConsider[0]
        if toPrint: print(f"toConsider={[i.name for i in toConsider]}, {avail=}\n"
                          f"Adding {nextItem}, avail={avail-nextItem.getCost()}")
        # Explore left branch
        withVal, withToTake = fastMaxVal(toConsider[1:], avail - nextItem.getCost(), memo, toPrint)
        withVal += nextItem.getValue()
        # Explore right branch
        withoutVal, withoutToTake = fastMaxVal(toConsider[1:], avail, memo, toPrint)
        if toPrint: print(
            f"Considering '{nextItem.name}' \n {withVal=} {[i.name for i in withToTake] + [nextItem.name]} |"
            f" {withoutVal=} {[i.name for i in withoutToTake]}")
        # Choose better branch
        if withVal > withoutVal:
            if toPrint: print(f"memo updated ({len(toConsider), avail}) = {withVal, withToTake + (nextItem,)}")
            result = (withVal, withToTake + (nextItem,))
        else:
            result = (withoutVal, withoutToTake)
    memo[(len(toConsider), avail)] = result
    if toPrint: print(f"{memo=}")
    return result


def testMaxVal(foods, maxUnits, algorithm, toPrint=False, printItems=False):
    print('Menu contains', len(foods), 'items')
    print('Use search tree to allocate', maxUnits, 'calories')
    val, taken = algorithm(foods, maxUnits, toPrint=toPrint)
    if printItems:
        print('Total value of items taken =', val)
        for item in taken:
            print('   ', item)


# Change code to keep track of number of calls
def countingFastMaxVal(toConsider, avail, memo={}):
    """Assumes toConsider a list of subjects, avail a weight
         memo supplied by recursive calls
       Returns a tuple of the total value of a solution to the
         0/1 knapsack problem and the subjects of that solution"""
    global numCalls
    numCalls += 1

    if (len(toConsider), avail) in memo:
        result = memo[(len(toConsider), avail)]
    elif toConsider == [] or avail == 0:
        result = (0, ())
    elif toConsider[0].getCost() > avail:
        result = countingFastMaxVal(toConsider[1:], avail, memo)
    else:
        nextItem = toConsider[0]
        withVal, withToTake = countingFastMaxVal(toConsider[1:], avail - nextItem.getCost(), memo)
        withVal += nextItem.getValue()
        withoutVal, withoutToTake = countingFastMaxVal(toConsider[1:], avail, memo)
        if withVal > withoutVal:
            result = (withVal, withToTake + (nextItem,))
        else:
            result = (withoutVal, withoutToTake)
    memo[(len(toConsider), avail)] = result
    return result


def test_4_item_menu(toPrint=False, toPrintItems=False):
    names = ['a', 'b', 'c', 'd']
    values = [6, 7, 8, 9]
    calories = [3, 3, 2, 5]
    foods = buildMenu(names, values, calories)
    print(f"The menu is: {foods}")
    testMaxVal(foods, 5, fastMaxVal, toPrint, toPrintItems)


if __name__ == '__main__':
    # for numItems in (5, 10, 15, 20, 25, 30, 35):
    #    print('Try a menu with', numItems, 'items')
    #    items = buildLargeMenu(numItems, 90, 250)
    #    testMaxVal(items, 750, maxVal, False)
    #
    # for numItems in (5, 10, 15, 20, 25, 30, 35, 40, 45, 50):
    #    items = buildLargeMenu(numItems, 90, 250)
    #    testMaxVal(items, 750, fastMaxVal, False)
    #
    # for numItems in (2, 4, 8, 16, 32, 64, 128, 256, 512, 1024):
    #     numCalls = 0
    #     items = buildLargeMenu(numItems, 90, 250)
    #     testMaxVal(items, 750, countingFastMaxVal, False)
    #     print('Number of calls =', numCalls, '\n')

    test_4_item_menu(True, True)


