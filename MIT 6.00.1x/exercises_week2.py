from math import pi, tan

x = 2
y = 3
print(type((x, y)))

print("There are <", 2**32, "> possibilities!", sep="")


def square(x):
    return x * x


def foo(x):
    def bar(z, x=0):
        return z + x
    return bar(3, x)


print(foo(2))


def foo(x, y=5):
    def bar(x):
        return x + 1
    return bar(y * 2)


print(foo(3, 0))

str1 = 'exterminate!'
s = str1.upper
str1.upper()
print(str1.index('e'))
print(s)
str2 = 'number one - the larch'
str2 = str2.capitalize()
str2.swapcase()
str2.find('n')
str1 = str1.replace('e', '*')
str2.replace('one', 'seven')


def fourthPower(x):
    return square(square(x))


print(fourthPower(3))


def odd(x):
    """ returns True if x is odd, False otherwise """
    if type(x) != int:
        print("Not an integer")
    else:
        return x % 2 == 1


print("Is the number odd?", odd(4))


def iterPower(base, exp):
    """
    base: int or float.
    exp: int >= 0
    returns: int or float, base^exp
    """
    res = 1
    while exp > 0:
        res *= base
        exp -= 1
    return res


def recurPower(base, exp):
    """
    base: int or float.
    exp: int >= 0
    """
    return 1 if exp == 0 else base * recurPower(base, exp-1)


print(iterPower(2,5))
print(recurPower(2,5))


def gcdIter(a, b):
    """
    a, b: positive integers
    returns: a positive integer, the greatest common divisor of a & b.
    """
    gcd = a if a < b else b
    while not(a % gcd == 0 and b % gcd == 0):
        gcd -= 1
    return gcd


print(gcdIter(6,12),
      gcdIter(9,12),
      gcdIter(17,12))


def gcdRecur(a: int, b: int) -> int:
    """
    a, b: positive integers
    returns: a positive integer, the greatest common divisor of a & b.
    """
    return a if b == 0 else gcdRecur(b, a % b)


print(gcdRecur(6, 12),
      gcdRecur(9, 12),
      gcdRecur(17, 12))


def isIn(char, aStr):
    """
    char: a single character
    aStr: an alphabetized string
    returns: True if char is in aStr; False otherwise
    """
    char = char.lower()
    mid = len(aStr)//2
    if len(aStr) == 0:
        return False
    if char == aStr[mid]:
        return True
    elif char < aStr[mid]:
        return isIn(char, aStr[:mid])
    elif char > aStr[mid]:
        return isIn(char, aStr[mid+1:])


aStr = 'abcdefghijklmnopqrstuvwxyz'
print('\n',
      isIn('b', 'bdgghhikkkklmmpqsvwx'),
      isIn('f', 'bcceehhhjkotttvxyyzz'),
      isIn('v', 'qs'))


def polysum(n, s):
    """
    :param n: numder of sides of a polygon
    :param s: length of its side
    :return: sum of the area and square of the perimeter of the regular polygon, rounded to 4 decimal places
    """
    area = (0.25*n*s*s)/(tan(pi/n))
    perimeter = n * s
    square_of_perimeter = perimeter * perimeter
    result_sum = area + square_of_perimeter
    result_sum = round(result_sum, 4)
    return result_sum


print(polysum(5, 1))


def guess_a_number():
    # At the start the highest the number could be is 100 and the lowest is 0.
    start = 0
    end = 100
    guessed = False
    print("Please think of a number between 0 and 100!")

    # Loop until we guess it correctly
    while not guessed:
        # Bisection search: guess the midpoint between our current high and low guesses
        current_value = (start+end)//2
        print("Is your secret number " + str(current_value) + "?")
        user_answer = input("Enter 'h' to indicate the guess is too high. "
                            "Enter 'l' to indicate the guess is too low. Enter 'c' to indicate I guessed correctly. ")
        if user_answer == 'c':
            # We got it!
            guessed = True
        elif user_answer == 'h':
            # Guess was too high. So make the current guess the highest possible guess.
            end = current_value
        elif user_answer == 'l':
            # Guess was too low. So make the current guess the lowest possible guess.
            start = current_value
        else:
            print("Sorry, I did not understand your input.")

    print("Game over. Your secret number was: ", current_value)


guess_a_number()
