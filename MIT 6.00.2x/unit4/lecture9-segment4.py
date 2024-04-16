# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 11:45:20 2016

@author: johnguttag
"""

import random, pylab, numpy
import plot_params

plot_params.plt_params()


def makeHist(data, title, xlabel, ylabel, bins=20):
    pylab.hist(data, bins=bins)
    pylab.title(title)
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)


def getHighs():
    inFile = open('temperatures.csv')
    population = []
    for l in inFile:
        try:
            tempC = float(l.split(',')[1])
            population.append(tempC)
        except:
            continue
    return population


def getMeansAndSDs(population, sample, verbose=False):
    popMean = sum(population) / len(population)
    sampleMean = sum(sample) / len(sample)
    if verbose:
        makeHist(population,
                 'Daily High 1961-2015, Population\n' + \
                 '(mean = ' + str(round(popMean, 2)) + ')',
                 'Degrees C', 'Number Days')
        pylab.figure()
        makeHist(sample, 'Daily High 1961-2015, Sample\n' + \
                 '(mean = ' + str(round(sampleMean, 2)) + ')',
                 'Degrees C', 'Number Days')
        print('Population mean =', popMean)
        print('Standard deviation of population =',
              numpy.std(population))
        print('Sample mean =', sampleMean)
        print('Standard deviation of sample =',
              numpy.std(sample))
    return popMean, sampleMean, numpy.std(population), numpy.std(sample)


random.seed(0)
temps = getHighs()
popMean = sum(temps) / len(temps)
sampleSize = 200
numTrials = 10000
numBad = 0
for t in range(numTrials):
    sample = random.sample(temps, sampleSize)
    sampleMean = sum(sample) / sampleSize
    se = numpy.std(sample) / sampleSize ** 0.5
    if abs(popMean - sampleMean) > 1.96 * se:
        numBad += 1
print('Fraction outside 95% confidence interval =',
      numBad / numTrials)

for t in range(numTrials):
    posStartingPts = range(0, len(temps) - sampleSize)
    start = random.choice(posStartingPts)
    sample = temps[start:start + sampleSize]
    sampleMean = sum(sample) / sampleSize
    se = numpy.std(sample) / sampleSize ** 0.5
    if abs(popMean - sampleMean) > 1.96 * se:
        numBad += 1
print('Fraction outside 95% confidence interval =',
      numBad / numTrials)
