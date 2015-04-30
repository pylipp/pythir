#!/usr/bin/python 

import matplotlib.pyplot as plt 

from algorithm import Algorithm, Mode
from phantom import Phantom 
from projectionsimulator import ProjectionSimulator


class Program(object):

    def __init__(self):
        size = 101
        self.__phantom = Phantom(size)
        self.__phantom.create() 

        self.__projectionSimulator = ProjectionSimulator(self.__phantom)
        self.__projectionSimulator.projectAll(size, 0, 360, 400)

        self.__sinogram = self.__projectionSimulator.projections 
        self.__systemMatrix = self.__projectionSimulator.systemMatrix 

        self.__algorithm = Algorithm(Mode.ART, self.__sinogram, self.__systemMatrix, 10)
        self.__result = None

    def compute(self):
        self.__algorithm.compute()
        #self.__result = self.__algorithm.result

    def plot(self, data):
        plt.figure()
        plt.imshow(data, cmap="gray")
        plt.show()
