#!/usr/bin/python 

import numpy as np 
import time
from scipy.ndimage import interpolation 
from . import enum

class Algorithm(object):
    """
    Class performing the essential numerical computations.
    Appends the result of each iteration to a list. 
    Description of Modes:
    - ADDITIVE_ART: The difference of the (measured/simulated) projections and
      the current forward-projected estimate is back-projected in direction of
      the current view. The resulting update is added to the current estimate. 
      Using SystemMatrixEvaluator.ROTATIONAL mode, one iteration already yields
      sufficient results.
    - MULTIPLICATIVE_ART: The current forward-projected estimate is
      multiplicated with the current estimate. Currently, the implementation
      diverges. 
    """
    Mode = enum(
            ADDITIVE_ART=0, 
            MULTIPLICATIVE_ART=1 )

    def __init__(self, mode, projections, systemMatrix, nrIter):
        """ 
        :param      mode | Algorithm.Mode 
                    projections | Projections 
                    systemmatrix | SystemMatrix 
                    nrIter | int 
        :attrib     __result | list[np.2darray]
        """
        self.__mode = mode
        self.__projections = projections 
        self.__systemMatrix = systemMatrix 
        self.__nrIter = nrIter
        self.__result = []

    @property 
    def result(self):
        return self.__result 

    def compute(self):
        """ 
        Calls computation method according to mode. 

        :param      mode | Algorithm.mode 
        """
        if self.__mode == Algorithm.Mode.ADDITIVE_ART:
            self.computeAdditiveART(self.__nrIter, self.__projections, self.__systemMatrix)
        elif self.__mode == Algorithm.Mode.MULTIPLICATIVE_ART:
            self.computeMultiplicativeART()

    def computeAdditiveART(self, nrIter, projections, systemMatrix):
        """
        Computes the algebraic reconstruction using an additive update method
        as described above. 
        """
        estimate = np.zeros_like(systemMatrix.data[0])
        self.__result = []
        start = time.time()
        for n in range(nrIter):
            print "Computing iteration " + str(n)
            for v in range(projections.views):
                try:
                    currentSm = systemMatrix.data[v]
                    angle = v*180/float(projections.views)
                    rotatedEstimate = interpolation.rotate(estimate, -angle, reshape=False)
                    backprojection = np.sum(currentSm * rotatedEstimate, axis=0)
                    normalization = np.sum(currentSm * currentSm, axis=0)
                    normalization[normalization == 0] = 1.0 #avoid division by zero 
                    update = currentSm * (projections.data[v] - backprojection) / normalization 
                    estimate += interpolation.rotate(update, angle, reshape=False)
                    estimate[estimate < 0] = 0.0 #nonnegativity constraint
                except ValueError:
                    import pdb; pdb.set_trace()
            self.__result.append(estimate.copy())
        end = time.time()
        print "Computation time for subtractive ART: " + str(end-start)

    def computeMultiplicativeART(self):
        """
        Computes the algebraic reconstruction using a multiplicative update method
        as described above. 
        NOT STABLE.
        """
        nrIter = self.__nrIter 
        projections = self.__projections 
        systemMatrix = self.__systemMatrix
        estimate = 50*np.ones_like(systemMatrix.data[0])
        self.__result = []
        start = time.time()
        for n in range(nrIter):
            print "Computing iteration " + str(n)
            for v in range(projections.views):
                try:
                    currentSm = systemMatrix.data[v]
                    angle = v*180/float(projections.views)
                    rotatedEstimate = interpolation.rotate(estimate, -angle, reshape=False)
                    backprojection = np.sum(currentSm * rotatedEstimate, axis=0)
                    update = np.ones_like(backprojection)
                    update[backprojection > 0] = projections.data[v][backprojection > 0] / backprojection[backprojection > 0]
                    updateMatrix = np.tile(update, (currentSm.shape[0], 1))
                    estimate *= interpolation.rotate(updateMatrix, angle, reshape=False)
                except (ValueError, IndexError):
                    import pdb; pdb.set_trace()
            self.__result.append(estimate.copy())
        end = time.time()
        print "Computation time for multiplicative ART: " + str(end-start)
