import timeit

# prompt for the input until it's a positive number less than 10
while True:
    height = input("Height: ")
    if height.isdigit() and 0 < int(height) <= 10:
        break


# make height an int
height = int(height)


# print out the pyramid
def pyramid0():
    for i in range(height):
        print((' ' * (height - (i+1))) + ('#' * (i+1)) + '  ' + ('#' * (i+1)))


def pyramid1():
    for i in range(height+1):
        if i == 0:
            continue
        print((' ' * (height - i)) + ('#' * i) + '  ' + ('#' * i))


if __name__ == '__main__':
    pyramid1()


# if __name__ == '__main__':
#     print(timeit.timeit("pyramid0()", setup="from __main__ import pyramid0, height", number=1000))
#     print(timeit.timeit('pyramid1()', globals=globals(), number=1000))
