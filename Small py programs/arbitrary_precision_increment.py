""" The program shows a way to implement an arbitrary precision increment
 As an input data two lists representing numbers are used.
 As an output there are two list representing resulting numbers. """

A1 = [1, 4, 9]
A2 = [9, 9, 9]


def add_one(array):
    array = array.copy()
    array[-1] += 1
    for i in reversed(range(1, len(array))):
        if array[i] != 10:
            break
        else:
            array[i] = 0
            array[i-1] += 1
    if array[0] == 10:
        array[0] = 1
        array.append(0)
    return array


print(add_one(A1))
print(add_one(A2))
