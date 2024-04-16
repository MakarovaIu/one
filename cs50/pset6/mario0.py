# import timeit

# prompt for the input until it's a positive number less than 10
while True:
    height = input("Height: ")
    if height.isdigit() and 0 < int(height) <= 10:
        break


# make height an int
height = int(height)


# print out the pyramid
def pyramid0():
    """slower pyramid"""
    pyramid = ''
    for i in range(height):
        pyramid += ((' ' * (height - (i+1))) + ('#' * (i+1)) + '  ' + ('#' * (i+1)) + '\n')
    return pyramid


def pyramid1():
    """faster pyramid"""
    pyramid = ''
    for i in range(height+1):
        if i == 0:
            continue
        pyramid += ((' ' * (height - i)) + ('#' * i) + '  ' + ('#' * i) + '\n')
    return pyramid


if __name__ == '__main__':
    print(pyramid1())


# if __name__ == '__main__':
#     print("Pyramid one: ", timeit.timeit("pyramid0()", setup="from __main__ import pyramid0, height", number=10000))
#     print("Pyramid two: ", timeit.timeit('pyramid1()', globals=globals(), number=10000))
