class Coordinate():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        # Getter method for a Coordinate object's x coordinate.
        # Getter methods are better practice than just accessing an attribute directly
        return self.x

    def getY(self):
        # Getter method for a Coordinate object's y coordinate
        return self.y

    def __str__(self):
        return '<' + str(self.getX()) + ',' + str(self.getY()) + '>'

    def __eq__(self, other):
        return self.getX() == other.getX() and self.getY() == other.getY()

    def __repr__(self):
        # calling str on a method will eventually use the __repr__ of the class
        # That last bit in there, Coordinate(10,9), is the __repr__ representation of the object itself,
        # so you know which object the method belongs to.
        # Since this happens in the __repr__ of your object, calling that __repr__ will call the __repr__ again
        # via that str(self.getX) and that new __repr__ call will call __repr__ again
        # and that will call __repr__ again... until you hit the recursion limit Python has.

        # return "Coordinate({}, {})".format(self.getX(), self.getY())
        # return "Coordinate (%s, %s)" % (self.getX(), self.getY())
        return f"Coordinate({self.getX()}, {self.getY()})"


first = Coordinate(1, 2)
print(first)
print(first.getX)
print(repr(first))
print()

class intSet(object):
    """An intSet is a set of integers
    The value is represented by a list of ints, self.vals.
    Each int in the set occurs in self.vals exactly once."""

    def __init__(self):
        """Create an empty set of integers"""
        self.vals = []

    def insert(self, *values):
        """Assumes e is an integer and inserts e into self"""
        for e in values:
            if e not in self.vals:
                self.vals.append(e)

    def member(self, e):
        """Assumes e is an integer
           Returns True if e is in self, and False otherwise"""
        return e in self.vals

    def remove(self, e):
        """Assumes e is an integer and removes e from self
           Raises ValueError if e is not in self"""
        try:
            self.vals.remove(e)
        except:
            raise ValueError(str(e) + ' not found')

    def __str__(self):
        """Returns a string representation of self"""
        self.vals.sort()
        return '{' + ', '.join([str(e) for e in self.vals]) + '}'

    def intersect(self, other):
        res = intSet()
        elements = (elem for elem in self.vals if other.member(elem))
        for elem in elements:
            res.insert(elem)
        return res

    def __len__(self):
        return len(self.vals)


s1 = intSet()
s2 = intSet()
s1.insert(1, 2, 3, 5)
s1.insert(3, 4, 6)
s2.insert(3, 8, 8, 10)
print(s1, s2)
s3 = s1.intersect(s2)
print(s3)
print()


class Spell(object):
    def __init__(self, incantation, name):
        self.name = name
        self.incantation = incantation

    def __str__(self):
        return self.name + ' ' + self.incantation + '\n' + self.getDescription()

    def getDescription(self):
        return 'No description'

    def execute(self):
        print(self.incantation)


class Accio(Spell):
    def __init__(self):
        Spell.__init__(self, 'Accio', 'Summoning Charm')


class Confundo(Spell):
    def __init__(self):
        Spell.__init__(self, 'Confundo', 'Confundus Charm')

    def getDescription(self):
        return 'Causes the victim to become confused and befuddled.'


def studySpell(spell):
    print(spell)


spell = Accio()
spell.execute()
studySpell(spell)
studySpell(Confundo())
print()


class A(object):
    def __init__(self):
        self.a = 1
    def x(self):
        print("A.x")
    def y(self):
        print("A.y")
    def z(self):
        print("A.z")

class B(A):
    def __init__(self):
        A.__init__(self)
        self.a = 2
        self.b = 3
    def x(self):
        print("B.x")
    def y(self):
        print("B.y")
    def z(self):
        print("B.z")

class C(A):
    def __init__(self):
        A.__init__(self)
        self.a = 4
        self.c = 5
    def y(self):
        print("C.y")
    def z(self):
        print("C.z")

class D(C, B):
    def __init__(self):
        C.__init__(self)
        B.__init__(self)
        self.d = 6
    def z(self):
        print("D.z")


# Sieve of Eratosthenes
# Code by David Eppstein, UC Irvine, 28 Feb 2002
# http://code.activestate.com/recipes/117119/
def gen_primes():
    """ Generate an infinite sequence of prime numbers.
    """
    # Maps composites to primes witnessing their compositeness.
    # This is memory efficient, as the sieve is not "run forward"
    # indefinitely, but only as long as required by the current
    # number being tested.
    #
    D = {}

    # The running integer that's checked for primeness
    q = 2

    while True:
        if q not in D:
            # q is a new prime.
            # Yield it and mark its first multiple that isn't
            # already marked in previous iterations
            #
            yield q
            # print(f"q yielded: {q}")
            D[q * q] = [q]  # create a key equal to the cube of our prime number
            # print(f"D: {D}")
        else:
            # q is composite. D[q] is the list of primes that
            # divide it. Since we've reached q, we no longer
            # need it in the map, but we'll mark the next
            # multiples of its witnesses to prepare for larger
            # numbers
            #
            for p in D[q]:  # iterate over divisors of q
                # print(f"p: {p}, D[q]: {D[q]}")
                D.setdefault(p + q, []).append(p)  # create a number q + its divisor p key and set p as its divisor
                # print(f"D: {D}")
            del D[q]
        # print(f"q: {q}\n")
        q += 1


spam = gen_primes()


class Primes:
    def __init__(self):
        self.primes = set()
        self.prime = None

    def genPrimes(self):
        self.primes = set()
        self.prime = 2
        while True:
            for num in self.primes:
                if not self.prime % num:
                    break
            else:
                self.primes.add(self.prime)
                yield self.prime
            self.prime += 1


spam = Primes()
eggs = spam.genPrimes()
for i in range(10):
    print(eggs.__next__())
print(spam.primes)
