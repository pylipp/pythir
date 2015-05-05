#!/usr/bin/python 

import matplotlib.pyplot as plt 

from algorithm import Algorithm, Mode
from phantom import Phantom 
from projectionsimulator import ProjectionSimulator


class Program(object):

    def __init__(self, phantom=None):
        if phantom is None:
            self.__phantom = Phantom(101) 
            self.__phantom.create() 
        else:
            self.__phantom = phantom

        self.__projectionSimulator = ProjectionSimulator(self.__phantom)
        self.__projectionSimulator.projectAll(self.__phantom.size, 0, 180, 100)

        self.__sinogram = self.__projectionSimulator.projections 
        self.__systemMatrix = self.__projectionSimulator.systemMatrix 

        self.__algorithm = Algorithm(Mode.SUBTRACTIVE_ART, self.__sinogram, self.__systemMatrix, 1)
        self.__result = None

        self.__figureIndex = 0

    @property 
    def result(self):
        return self.__result 

    def compute(self):
        self.__algorithm.compute()
        self.__result = self.__algorithm.result

    def plot(self, data):
        #plt.figure(self.__figureIndex)
        self.__figureIndex += 1
        plt.imshow(data, cmap="gray", interpolation="nearest")
        #plt.show()
