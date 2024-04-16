import random


def genEven():
    """
    Returns a random even number x, where 0 <= x < 100
    """
    return random.randrange(0, 100, 2)


def stochasticNumber():
    """
    Stochastically generates and returns a uniformly distributed even number between 9 and 21
    """
    return random.randrange(10, 21, 2)


print(genEven())
print(stochasticNumber())


# ===== Three Facts of Probability =====
# Probability if always between 0 and 1
# If the probability of event occurring is p, then the probability of it not occurring is 1-p
# When events are independent, the probability of all of the events occurring is equal to product of probabilities

