#!/usr/bin/python 

import matplotlib.pyplot as plt 
import numpy as np

from algorithm import Algorithm, Mode
from phantom import Phantom 
from projectionsimulator import ProjectionSimulator


class Program(object):

    def __init__(self, phantom=None):
        if phantom is None:
            self.__phantom = Phantom(size=101) 
            self.__phantom.create() 
        else:
            self.__phantom = phantom

        self.__projectionSimulator = ProjectionSimulator(self.__phantom)
        self.__projectionSimulator.initProjections(self.__phantom.size, 100)
        self.__projectionSimulator.initSystemMatrix(101, 100)
        self.__projectionSimulator.projectAll(self.__phantom.size, 0, 180, 100)

        self.__sinogram = self.__projectionSimulator.projections 
        self.__systemMatrix = self.__projectionSimulator.systemMatrix 

        self.__algorithm = Algorithm(Mode.MULTIPLICATIVE_ART, self.__sinogram,
                self.__systemMatrix, 10)
        self.__result = None
        self.__rmse = None

        self.__figureIndex = 0

    @property 
    def result(self):
        return self.__result 

    @property
    def rmse(self):
        return self.__rmse

    def compute(self):
        self.__algorithm.compute()
        self.__result = self.__algorithm.result

    def computeRmse(self, groundTruth=None):
        if groundTruth is None:
            groundTruth = self.__phantom.data
        iteration = []
        rmse = []
        invNrPixels = 1.0/(np.prod(groundTruth.shape))
        for i, image in enumerate(self.__result):
            if image.shape != groundTruth.shape:
                print "Mismatch in data dimensions. Skipping RMSE computation nr %i.", i
                continue
            iteration.append(i+1)
            difference = image - groundTruth 
            rmse.append(np.sqrt( np.sum(difference*difference) * invNrPixels ))
        self.__rmse = (np.array(iteration), np.array(rmse))

    def plot(self, data):
        #plt.figure(self.__figureIndex)
        self.__figureIndex += 1
        plt.imshow(data, cmap="gray", interpolation="nearest")
        #plt.show()
