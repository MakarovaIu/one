import math
import random
import numpy
import pylab

def mean(data):
    return sum(data) / len(data)


def variance(data):
    m = mean(data)
    return sum(((x - m)**2 for x in data))/len(data)


def stdDevOfLengths(data):
    """
    data: a list of strings

    returns: float, the standard deviation of the lengths of the strings,
      or NaN if L is empty.
    """
    if not data:
        return float('NaN')
    data = [len(word) for word in data]
    return math.sqrt(variance(data))


def stdDev(data):
    return math.sqrt(variance(data))


# print(variance([3, 3, 5, 7, 7]))
# print(variance([1, 5, 5, 5, 9]))
# print(stdDevOfLengths(['a', 'z', 'p']))
# print(stdDevOfLengths(['apples', 'oranges', 'kiwis', 'pineapples']))
# L = [10, 4, 12, 15, 20, 5]
# print(stdDev(L)/mean(L))


def noReplacementSimulation(numTrials):
    """
    Runs numTrials trials of a Monte Carlo simulation
    of drawing 3 balls out of a bucket containing
    3 red and 3 green balls. Balls are not replaced once
    drawn. Returns the a decimal - the fraction of times 3
    balls of the same color were drawn.
    """
    counter = 0
    for _ in range(numTrials):
        balls = list(3*'r' + 3*'g')
        balls_drawn = [balls.pop(random.randrange(0, len(balls)-1)) for _ in range(3)]
        if balls_drawn[0] == balls_drawn[1] == balls_drawn[2]:
            counter += 1
    return counter / numTrials


print(noReplacementSimulation(500))


def loadFile():
    inFile = open('julytemp.txt')
    high = []
    low = []
    for line in inFile:
        fields = line.split()
        if len(fields) < 3 or not fields[0].isdigit():
            continue
        else:
            high.append(int(fields[1]))
            low.append(int(fields[2]))
    return low, high


lowTemps, highTemps = loadFile()
diffTemps = list(numpy.array(highTemps) - numpy.array(lowTemps))
pylab.plot(range(1, 32), diffTemps)
