
def fib(n):
    if n == 0 or n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def fastFib(n, memo=None):
    """Assumes n is an int >= 0, memo used only by recursive calls
       Returns Fibonacci of n"""
    if memo is None:
        memo = {}
    if n == 0 or n == 1:
        return 1
    try:
        return memo[n]
    except KeyError:
        result = fastFib(n - 1, memo) + fastFib(n - 2, memo)
        memo[n] = result
        return result


if __name__ == '__main__':

    for i in range(36):
        print('fib(' + str(i) + ') =', fib(i))
    print()
    for i in range(121):
        print('fib(' + str(i) + ') =', fastFib(i))

# ---- Dynamic Programming -----
# * Optimal substructure: a globally optimal solution can be found by combining optimal solutions to local problems
# * Overlapping subproblems: finding an optimal solution involves solving the same problem multiple times
