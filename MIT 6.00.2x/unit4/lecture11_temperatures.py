# -*- coding: utf-8 -*-
"""
based on:
Created on Mon Sep 19 11:45:20 2016

@author: johnguttag
"""
import random

import numpy as np
import matplotlib.pyplot as plt

import plot_params
import lecture10and11


plot_params.plt_params()
SM = lecture10and11.StatisticMethods


class TempDatum:
    """ creates an object from a string with temp and year info """
    def __init__(self, s):
        info = s.split(',')
        self._high = float(info[1])
        self._year = int(info[2][0:4])

    @property
    def high(self):
        return self._high

    @property
    def year(self):
        return self._year


class TempDatumProseccing:

    @staticmethod
    def getTempData():
        """ reads temperatures.csv and returns a list of TempDatum objects """
        with open('temperatures.csv') as inFile:
            data = []
            inFile.readline()
            for l in inFile:
                data.append(TempDatum(l))
        return data

    @staticmethod
    def getYearlyMeans(data):
        """ creates and returns a dict with years as a key and mean temp of that year as a value """
        years = {}
        for d in data:
            try:
                years[d.year].append(d.high)
            except KeyError:
                years[d.year] = [d.high]
        for y in years:
            years[y] = sum(years[y]) / len(years[y])
        return years

    @staticmethod
    def getYearAndTemp():
        """ gets data from a file are return (year, aveYearTemp) pair """
        data = TempDatumProseccing.getTempData()
        years = TempDatumProseccing.getYearlyMeans(data)
        xVals, yVals = [], []
        for e in years:
            xVals.append(e)
            yVals.append(years[e])
        return xVals, yVals

    @staticmethod
    def plotYearlyMeans():
        """ plots yealy temp means """
        xVals, yVals = TempDatumProseccing.getYearAndTemp()
        plt.plot(xVals, yVals)
        plt.xlabel('Year')
        plt.ylabel('Mean Daily High (C)')
        plt.title('Select U.S. Cities')
        plt.show()

    @staticmethod
    def splitData(xVals, yVals):
        """ randomly splits half of the data into Tains and Test pair values """
        # To choose a sample from a range of integers, use a range() object as an argument.
        # This is especially fast and space efficient for sampling from a large population: sample(range(100000), k=60).
        toTrain = random.sample(range(len(xVals)), len(xVals) // 2)
        trainX, trainY, testX, testY = [], [], [], []
        for i in range(len(xVals)):
            if i in toTrain:
                trainX.append(xVals[i])
                trainY.append(yVals[i])
            else:
                testX.append(xVals[i])
                testY.append(yVals[i])
        return trainX, trainY, testX, testY

    @staticmethod
    def testData(printR=True):
        numSubsets = 10
        dimensions = (1, 2, 3)
        rSquares = {}
        for d in dimensions:
            rSquares[d] = []
        xVals, yVals = TempDatumProseccing.getYearAndTemp()

        for f in range(numSubsets):
            trainX, trainY, testX, testY = TDP.splitData(xVals, yVals)
            for d in dimensions:
                model = np.polyfit(trainX, trainY, d)
                estYVals = np.polyval(model, testX)
                rSquares[d].append(SM.rSquared(testY, estYVals))

        print('Mean R-squares for test data')
        for d in dimensions:
            mean = round(sum(rSquares[d]) / len(rSquares[d]), 4)
            sd = round(np.std(rSquares[d]), 4)
            print('For dimensionality', d, 'mean =', mean, 'Std =', sd)

        if printR:
            print(rSquares[1])


if __name__ == "__main__":

    random.seed(0)
    TDP = TempDatumProseccing
    TDP.plotYearlyMeans()

    TDP.testData()
