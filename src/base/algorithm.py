#!/usr/bin/python 

import numpy as np 
import time
from abc import ABCMeta, abstractmethod
from scipy.ndimage import interpolation 
from . import enum

class Algorithm(object):
    """
    Abstract class performing the essential numerical computations.
    Appends the result of each iteration to a result list. 
    Description of Modes:
    - ADDITIVE_ART: The difference of the (measured/simulated) projections and
      the current forward-projected estimate is back-projected in direction of
      the current view. The resulting update is added to the current estimate. 
      Using SystemMatrixEvaluator.ROTATIONAL mode, one iteration already yields
      sufficient results.
    - MULTIPLICATIVE_ART: The current forward-projected estimate is
      multiplicated with the current estimate. The performance of this method
      heavily depends on the initial estimate. MART automatically enforces
      pixels to be nonnegative (if the initial value is nonnegative).
    - SIMULTANEOUS_IRT/SIRT: The update is performed for one pixel at a time
      using all equations that contribute to that pixel. 

    References: Parts of the description above is adapted from Lalush's chapter
    about iterative image reconstruction (2004).

    :classattrib    Mode | enum
    """

    __metaclass__ = ABCMeta

    Mode = enum(
            ADDITIVE_ART=0, 
            MULTIPLICATIVE_ART=1,
            SIRT=2 )

    def __init__(self, mode, *args): 
        """ 
        :param      mode | Algorithm.Mode 
        :args       projections | Projections 
                    systemmatrix | SystemMatrix 
                    nrIter | int 
        :attrib     _result | list[np.2darray]
                    _estimate | np.2darray
        """
        self._mode = mode
        self._projections = args[0] 
        self._systemMatrix = args[1] 
        self._nrIter = args[2]
        self._estimate = np.zeros_like(self._systemMatrix.data[0])
        self._result = []

    @property 
    def result(self):
        return self._result 

    @property 
    def loadSize(self):
        return self._nrIter

    @abstractmethod
    def compute(self):
        """ 
        Performs the complete computation of all iterations.
        Measures runtime using a timer. Prints updates to the console.
        """
        pass
        #TODO unify the argument structure of the compute submethods
        if self._mode == Algorithm.Mode.ADDITIVE_ART:
            self.computeAdditiveART(self._nrIter, self._projections, self._systemMatrix)
        elif self._mode == Algorithm.Mode.MULTIPLICATIVE_ART:
            self.computeMultiplicativeART()
        elif self._mode == Algorithm.Mode.SIRT:
            self.computeSirt()

    @abstractmethod 
    def computeOne(self, n):
        """
        Performs the computation of a single iteration.
        Contains the core of the computation. Can be called as Task from a
        TaskHandler. 
        """
        pass 

    #######################################
    #TODO Deprecate these computing methods
    #######################################
    def computeAdditiveART(self, nrIter, projections, systemMatrix):
        """
        Computes the algebraic reconstruction using an additive update method
        as described above. 
        """
        estimate = np.zeros_like(systemMatrix.data[0])
        self._result = []
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
            self._result.append(estimate.copy())
        end = time.time()
        print "Computation time for subtractive ART: " + str(end-start)

    def computeMultiplicativeART(self):
        """
        Computes the algebraic reconstruction using a multiplicative update method
        as described above. 
        NOT STABLE.
        """
        nrIter = self._nrIter 
        projections = self._projections 
        systemMatrix = self._systemMatrix
        estimate = 50*np.ones_like(systemMatrix.data[0])
        self._result = []
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
            self._result.append(estimate.copy())
        end = time.time()
        print "Computation time for multiplicative ART: " + str(end-start)

    def computeSirt(self):
        nrIter = self._nrIter 
        projections = self._projections 
        systemMatrix = self._systemMatrix
        estimate = np.zeros_like(systemMatrix.data[0])
        self._result = []
        start = time.time()
        relaxation = 1.4/float(projections.views)
        for n in range(nrIter):
            update = np.zeros_like(estimate)
            print "Computing iteration " + str(n)
            for v in range(projections.views):
                try:
                    currentSm = systemMatrix.data[v]
                    angle = v*180/float(projections.views)
                    rotatedEstimate = interpolation.rotate(estimate, -angle, reshape=False)
                    backprojection = np.sum(currentSm * rotatedEstimate, axis=0)
                    normalization = np.sum(currentSm * currentSm, axis=0)
                    normalization[normalization == 0] = 1.0 #avoid division by zero 
                    fraction = currentSm * (projections.data[v] - backprojection) / normalization 
                    update += interpolation.rotate(fraction, angle, reshape=False)
                except (ValueError, IndexError):
                    import pdb; pdb.set_trace()
            update *= relaxation 
            estimate += update 
            estimate[estimate < 0] = 0.0
            self._result.append(estimate.copy())
        end = time.time()
        print "Computation time for SIRT: " + str(end-start)
