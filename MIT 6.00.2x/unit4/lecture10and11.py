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

plot_params.plt_params()


class DataWork:

    @staticmethod
    def getData(fileName):
        """ get data from a file and returns tuple of 2 """
        dataFile = open(fileName, 'r')
        distances = []
        masses = []
        dataFile.readline()  # discard header
        for line in dataFile:
            d, m = line.split()
            distances.append(float(d))
            masses.append(float(m))
        dataFile.close()
        return masses, distances

    @staticmethod
    def labelPlot():
        """ label spring data """
        plt.title('Measured Displacement of Spring')
        plt.xlabel('|Force| (Newtons)')
        plt.ylabel('Distance (meters)')

    @staticmethod
    def plotData(fileName):
        """ plot spring data """
        xVals, yVals = DataWork.getData(fileName)
        xVals = np.array(xVals)
        yVals = np.array(yVals)
        xVals = xVals * 9.81  # acc. due to gravity
        plt.plot(xVals, yVals, 'bo', label='Measured displacements')
        DataWork.labelPlot()

    @staticmethod
    def fitData(fileName):
        """ fit spring data into a line and plots it """
        xVals, yVals = DataWork.getData(fileName)
        xVals = np.array(xVals)
        yVals = np.array(yVals)
        xVals = xVals * 9.81  # get force
        plt.plot(xVals, yVals, 'bo', label='Measured points')
        DataWork.labelPlot()
        a, b = np.polyfit(xVals, yVals, 1)  # model = np.polyfit(xVals, yVals, 1)
        estYVals = a * xVals + b  # estYVals = np.polyval(model, xVals)
        print('a =', round(a, 5), 'b =', round(b, 5))
        plt.plot(xVals, estYVals, 'r', label='Linear fit, k = ' + str(round(1 / a, 5)))
        plt.legend(loc='best')

    @staticmethod
    def genParabolicData(a, b, c, xVals, fracOutliers=0.0, gauss=1000, inFile=False, fName=None):
        """ generates parabolic data and returns list of y values with set coefficients corresponding to set x's
        can save x and y values to the file """
        yVals = []
        for x in xVals:
            theoreticalVal = a * x ** 2 + b * x + c
            if random.random() > fracOutliers:
                yVals.append(theoreticalVal + random.gauss(0, gauss))
            else:  # generate outlier
                yVals.append(theoreticalVal + random.gauss(0, theoreticalVal * 2))
        if inFile:
            f = open(fName, 'w')
            f.write('x        y\n')
            for i in range(len(yVals)):
                f.write(str(yVals[i]) + ' ' + str(xVals[i]) + '\n')
            f.close()
        return yVals

    @staticmethod
    def genData(xVals, a, b, c, fracOutlier):
        """ generate parabolic data, return tuple of x and y vals. Also plots these points """
        # random.seed(0)
        yVals = DataWork.genParabolicData(a, b, c, xVals, fracOutlier)
        plt.plot(xVals, yVals, 'o', label='Data Points')
        plt.title('Mystery Data')
        return xVals, yVals

    @staticmethod
    def tryModel(xVals=None, yVals=None, plot=True, genData=False, getData=False, file=None, model=None):
        """ helper function to try either linear or quadratic model """
        if genData or not getData:
            xVals, yVals = xVals, yVals
        if getData:
            xVals, yVals = DataWork.getData(file)
            if file == "springData.txt":
                xVals = np.array(xVals)
                yVals = np.array(yVals)
                xVals = xVals * 9.81

        label = None
        if model == 0:
            model = np.polyfit(xVals, yVals, 1)
            label = "Linear Model"
        elif model == 1:
            model = np.polyfit(xVals, yVals, 2)
            label = "Quadratic Model"

        if plot:
            estYVals = np.polyval(model, xVals)
            error = round(StatisticMethods.rSquared(yVals, estYVals), 5)
            plt.plot(xVals, np.polyval(model, xVals), label=f'{label}. R\u00b2={error}')
            plt.legend()
        return model, xVals, yVals

    @staticmethod
    def tryLinearModel(xVals=None, yVals=None, plot=True, genData=False, getData=False, file=None):
        """ applies linear model on generated data or data from file
         plots a graph, displays R squared"""
        model, xVals, yVals = DataWork.tryModel(xVals, yVals, plot, genData, getData, file, model=0)
        return model, xVals, yVals

    @staticmethod
    def tryQuadraticModel(xVals=None, yVals=None, plot=True, genData=False, getData=False, file=None):
        """ applies quadratic model on generated data or data from file
         plots a graph, displays R squared"""
        model, xVals, yVals = DataWork.tryModel(xVals, yVals, plot, genData, getData, file, model=1)
        return model, xVals, yVals


class StatisticMethods:

    @staticmethod
    def aveMeanSquareError(data, predicted):
        """ calculates average mean square error of a data set, compared to predicted values
         returns sum of errors / len of data """
        error = 0.0
        for i in range(len(data)):
            error += (data[i] - predicted[i]) ** 2
        return error / len(data)

    @staticmethod
    def rSquared(observed, predicted):
        error = ((predicted - observed) ** 2).sum()
        meanError = error / len(observed)
        return 1 - (meanError / np.var(observed))

    @staticmethod
    def genFits(xVals, yVals, degrees):
        """ generates and returns a list of np.polyfit models of set degrees """
        models = []
        for d in degrees:
            model = np.polyfit(xVals, yVals, d)
            models.append(model)
        return models

    @staticmethod
    def testFits(models, degrees, xVals, yVals, title):
        """ rests differend degree fits on a data set
        plots data. plots every model with corresponding R squared"""
        plt.plot(xVals, yVals, 'o', label='Data')
        for i in range(len(models)):
            estYVals = np.polyval(models[i], xVals)
            error = StatisticMethods.rSquared(yVals, estYVals)
            plt.plot(xVals, estYVals, label='Fit of degree ' + str(degrees[i]) + ', R2 = ' + str(round(error, 5)))
        plt.legend(loc='best')
        plt.title(title)


class GenerateStuff:

    @staticmethod
    def springData():
        DataWork.fitData('springData.txt')
        plt.show()

    @staticmethod
    def tryLinearAndQuadModels():
        """ generates random data and plots linear and quadratic models for these values with R squared """
        xVals, a, b, c, fracOutlier = range(-50, 51, 5), 3.0, 0.0, 0.0, 0.0
        generatedX, generatedY = DataWork.genData(xVals, a, b, c, fracOutlier)
        DataWork.tryLinearModel(generatedX, generatedY, genData=True)
        DataWork.tryQuadraticModel(generatedX, generatedY, genData=True)
        plt.show()

    @staticmethod
    def tryLinearAndQuadModelsOnSpring():
        """ plot original data from spring data, apply linear and quad models, displays R squared """
        DataWork.plotData("springData.txt")
        DataWork.tryLinearModel(getData=True, file="springData.txt")
        DataWork.tryQuadraticModel(getData=True, file="springData.txt")
        plt.show()

    @staticmethod
    def showAveMeanSqError():
        """ prints average mean square error for linear and quadratic models in absolute values on mystery data """
        linear = list(DataWork.tryLinearModel(plot=False, getData=True, file='mysteryData.txt'))
        estYVals = np.polyval(linear[0], linear[1])
        print('Ave. mean square error for linear model =',
              round(StatisticMethods.aveMeanSquareError(linear[2], estYVals), 2))
        quadratic = list(DataWork.tryQuadraticModel(plot=False, getData=True, file='mysteryData.txt'))
        estYVals = np.polyval(quadratic[0], quadratic[1])
        print('Ave. mean square error for quadratic model =',
              round(StatisticMethods.aveMeanSquareError(quadratic[2], estYVals), 2))

    @staticmethod
    def plotLinearAndQuadOnMysteryData():
        """ gets data from mysteryData.txt and plots 1- and 2-degree polynomials models on it """
        xVals, yVals = DataWork.getData('mysteryData.txt')
        degrees = (1, 2)
        models = StatisticMethods.genFits(xVals, yVals, degrees)
        StatisticMethods.testFits(models, degrees, xVals, yVals, 'Mystery Data')
        plt.figure()
        plt.show()

    @staticmethod
    def compareHigherOrderFits():
        xVals, yVals = DataWork.getData('mysteryData.txt')
        degrees = (2, 4, 8, 16)
        models = StatisticMethods.genFits(xVals, yVals, degrees)
        StatisticMethods.testFits(models, degrees, xVals, yVals, 'Mystery Data')
        plt.show()

    @staticmethod
    def crossCompareModels(randomness=False):
        """
        generates and saves random parabolic data in two files
        builds 2, 4, 8, 16-degree polynomial models and plots them
        then compares these models on data from the other file it was build on
        """
        # parameters for generating data
        xVals = range(-10, 11, 1)
        a, b, c = 3.0, 0.0, 0.0
        degrees = (2, 4, 8, 16)

        # generate data
        if not randomness:
            random.seed(0)
        DataWork.genParabolicData(a, b, c, xVals, gauss=35, inFile=True, fName='Dataset 1.txt')
        DataWork.genParabolicData(a, b, c, xVals, gauss=35, inFile=True, fName='Dataset 2.txt')

        # build and show models for dataset 1
        xVals1, yVals1 = DataWork.getData('Dataset 1.txt')
        models1 = StatisticMethods.genFits(xVals1, yVals1, degrees)
        StatisticMethods.testFits(models1, degrees, xVals1, yVals1, 'DataSet 1.txt')
        plt.show()

        # build and show models for dataset 2
        plt.figure()
        xVals2, yVals2 = DataWork.getData('Dataset 2.txt')
        models2 = StatisticMethods.genFits(xVals2, yVals2, degrees)
        StatisticMethods.testFits(models2, degrees, xVals2, yVals2, 'DataSet 2.txt')
        plt.show()

        # test and show models on different datasets
        StatisticMethods.testFits(models1, degrees, xVals2, yVals2, 'DataSet 2/ Model 1')
        plt.show()
        StatisticMethods.testFits(models2, degrees, xVals1, yVals1, 'DataSet 1/ Model 2')
        plt.show()

    @staticmethod
    def helperOverfit(xVals, yVals, modelDegree, title, printCoeffs=False, func=None, model=None):
        plt.plot(xVals, yVals, label='Actual values')
        if not type(model) == np.ndarray:
            model = np.polyfit(xVals, yVals, modelDegree)
        else:
            model = model
        if printCoeffs:
            if modelDegree == 2:
                print('a =', round(model[0], 4), 'b =', round(model[1], 4), 'c =', round(model[2], 4))
            if modelDegree == 1:
                print(f"a = {round(model[0], 4)} b = {round(model[1], 4)}")

        plt.title(title)
        estYVals = np.polyval(model, xVals)

        if func == 0:
            func = f"f(x)={int(model[0])}x\u00b2 + {'' if int(round(model[1])) == 1 else int(round(model[1]))}x + " \
                   f"{int(model[2])}"
        if func == 1:
            func = f"f(x)={round(model[0], 3)}x\u00b2 + {(round(model[1], 3))}x + {round(model[2], 3)}"
        if func == 2:
            func = f"f(x)={round(model[0], 3)}x + {round(model[1], 3)}"
        plt.plot(xVals, estYVals, 'r--',
                 label=f"Predictive values. R-squared = {round(StatisticMethods.rSquared(yVals, estYVals), 5)}\n {func}")
        plt.legend(loc='best')
        plt.show()
        return model

    @staticmethod
    def overfitting():
        # a line
        xVals = (0, 1, 2, 3)
        yVals = xVals
        GenerateStuff.helperOverfit(xVals, yVals, 2, "y(x)=x", printCoeffs=True, func=0)

        # Extend domain
        xVals = xVals + (20,)
        yVals = xVals
        GenerateStuff.helperOverfit(xVals, yVals, 2, "y(x) = x, extended to x=20", printCoeffs=True, func=0)

        # almost a line
        xVals = (0, 1, 2, 3)
        yVals = (0, 1, 2, 3.1)
        overfitModel = GenerateStuff.helperOverfit(xVals, yVals, 2, "y(x)=x with y(3) = 3.1", printCoeffs=True, func=1)

        # Extend domain
        xVals = xVals + (20,)
        yVals = xVals
        GenerateStuff.helperOverfit(xVals, yVals, 2, "y(x)=x, extended to x=20", printCoeffs=True, func=1,
                                    model=overfitModel)

        # minimizing overfitting
        xVals = (0, 1, 2, 3)
        yVals = (0, 1, 2, 3.1)
        model = np.polyfit(xVals, yVals, 1)
        xVals = xVals + (20,)
        yVals = xVals
        title = "y(x)=x, extended to x=20. \nMinimizing overfitting"
        GenerateStuff.helperOverfit(xVals, yVals, 1, title, printCoeffs=True, func=2, model=model)


if __name__ == "__main__":
    GS = GenerateStuff
    # GS.springData()
    # 
    # GS.tryLinearAndQuadModels()

    GS.tryLinearAndQuadModelsOnSpring()
    #
    # GS.showAveMeanSqError()
    #
    # GS.plotLinearAndQuadOnMysteryData()
    # GS.compareHigherOrderFits()
    #
    # GS.crossCompareModels()
    #
    # GS.overfitting()
