#!/usr/bin/python 

import matplotlib.pyplot as plt 
import numpy as np

from algorithm import Algorithm
from phantom import Phantom 
from projectionsimulator import ProjectionSimulator
from systemmatrixevaluator import SystemMatrixEvaluator


class Program(object):
    """
    Main class that wraps all object initializations and the subsequent
    computations.
    """
    def __init__(self, phantom=None):
        self.__phantom = phantom
        self.__projectionSimulator = None 
        self.__systemMatrix = None 
        self.__systemMatrixEvaluator = None 
        self.__algorithm = None
        self.__sinogram = None
        self.__result = None
        self.__rmse = None
        self.__figureIndex = 0

    @property 
    def phantom(self):
        return self.__phantom

    @property 
    def result(self):
        return self.__result 

    @property
    def rmse(self):
        return self.__rmse

    @property 
    def sinogram(self):
        return self.__sinogram 

    @property 
    def systemMatrix(self):
        return self.__systemMatrix 

    def compute(self):
        """ Starts the computation in the algorithm and stores the result. """
        if self.__algorithm is None:
            return
        self.__algorithm.compute()
        self.__result = self.__algorithm.result

    def computeRmse(self, groundTruth=None):
        """
        Evaluates the quality of a reconstructed slice (after a certain number
        of iterations) using the Root Mean Square Error w.r.t. the ground truth
        phantom. 

        :param      groundTruth | np.2darray or None 
        """
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
        """ Plot routine for convenience. """
        #plt.figure(self.__figureIndex)
        self.__figureIndex += 1
        plt.imshow(data, cmap="gray", interpolation="nearest")
        #plt.show()

    def setUp(self, views=100, start=0, stop=180, nrIter=10,
            mode=Algorithm.Mode.ADDITIVE_ART):
        """
        Subsequently sets up the phantom, simulated projections, system matrix.
        Eventually creates the algorithm. 

        :param      view, start, stop, nrIter | int 
                    mode | Algorithm.Mode 
        """
        if self.phantom is None:
            self.__phantom = Phantom(size=101) 
            self.__phantom.create() 

        if self.phantom is None:
            return 
        if self.phantom.size is None: #error prone
            return 
        self.__projectionSimulator = ProjectionSimulator(views,
                self.phantom.size, self.phantom)
        self.__projectionSimulator.initProjections()
        self.__projectionSimulator.projectAll(start, stop)

        self.__sinogram = self.__projectionSimulator.projections 

        self.__systemMatrixEvaluator = SystemMatrixEvaluator(views,
                self.phantom.size, SystemMatrixEvaluator.Mode.ROTATIONAL)
        self.__systemMatrixEvaluator.initSystemMatrix(self.phantom.size, views)
        self.__systemMatrixEvaluator.evaluate(start, stop, self.phantom)
        self.__systemMatrix = self.__systemMatrixEvaluator.systemMatrix 

        if self.systemMatrix is None or self.sinogram is None:
            return
        self.__algorithm = Algorithm(mode, self.sinogram, self.systemMatrix, nrIter)
