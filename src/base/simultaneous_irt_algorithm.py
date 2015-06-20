#!/usr/bin/python 

import numpy as np
import time
from scipy.ndimage import interpolation
from algorithm import Algorithm 

class SimultaneousIrtAlgorithm(Algorithm):
    """
    Algorithm subclass using the simultaneous iterative reconstruction
    technique.
    """
    def __init__(self, *args, **kwargs):
        """
        :args       projections | Projections 
                    systemmatrix | SystemMatrix 
                    nrIter | int 
        :kwargs     relaxation | float
        """
        super(SimultaneousIrtAlgorithm, self).__init__(
                Algorithm.Mode.SIRT, *args)
        self._relaxation = kwargs.get('relaxation')

    def compute(self):
        self._result = []
        start = time.time()
        for n in range(self._nrIter):
            print "Computing iteration " + str(n)
            self.computeOne(n)
        end = time.time()
        print "Computation time for subtractive ART: " + str(end-start)

    def computeOne(self, n):
        update = np.zeros_like(self._estimate)
        for v in range(self._projections.views):
            currentSm = self._systemMatrix.data[v]
            angle = v*180/float(self._projections.views)
            rotatedEstimate = interpolation.rotate(self._estimate, -angle, reshape=False)
            backprojection = np.sum(currentSm * rotatedEstimate, axis=0)
            normalization = np.sum(currentSm * currentSm, axis=0)
            normalization[normalization == 0] = 1.0 #avoid division by zero 
            fraction = currentSm * (self._projections.data[v] - backprojection) / normalization 
            update += interpolation.rotate(fraction, angle, reshape=False)
        update *= self._relaxation
        self._estimate += update 
        self._estimate[self._estimate < 0] = 0.0
        self._result.append(self._estimate.copy())

    def ready(self):
        if self._relaxation is None:
            self._relaxation = 1.4
        self._result = []
        self._relaxation /= float(self._projections.views)
        return True
