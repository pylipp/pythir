#!/usr/bin/python 

import numpy as np
import time
from scipy.ndimage import interpolation
from algorithm import Algorithm 

class MultiplicativeArtAlgorithm(Algorithm):
    """
    Algorithm subclass using the Multiplicative ART method. 
    See the doc of Algorithm for further details.
    """
    def __init__(self, *args):
        """
        :args       projections | Projections 
                    systemmatrix | SystemMatrix 
                    nrIter | int 
        """
        super(MultiplicativeArtAlgorithm, self).__init__(
                Algorithm.Mode.MULTIPLICATIVE_ART, *args)

    def compute(self):
        self._result = []
        start = time.time()
        for n in range(self._nrIter):
            print "Computing iteration " + str(n)
            self.computeOne(n)
        end = time.time()
        print "Computation time for subtractive ART: " + str(end-start)

    def computeOne(self, n):
        for v in range(self._projections.views):
            currentSm = self._systemMatrix.data[v]
            angle = v*180/float(self._projections.views)
            rotatedEstimate = interpolation.rotate(self._estimate, -angle, reshape=False)
            backprojection = np.sum(currentSm * rotatedEstimate, axis=0)
            update = np.ones_like(backprojection)
            update[backprojection > 0] = self._projections.data[v][backprojection > 0] / backprojection[backprojection > 0]
            updateMatrix = np.tile(update, (currentSm.shape[0], 1))
            self._estimate *= interpolation.rotate(updateMatrix, angle, reshape=False)
        self._result.append(self._estimate.copy())

    def ready(self):
        self._result = []
        self._estimate[:] = 0.1
        return True
