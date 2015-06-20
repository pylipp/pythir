#!/usr/bin/python 

import numpy as np
import time
from scipy.ndimage import interpolation
from algorithm import Algorithm 

class AdditiveArtAlgorithm(Algorithm):
    """
    Algorithm subclass using the Additive ART method. 
    See the doc of Algorithm for further details.
    """
    def __init__(self, *args):
        """
        :args       projections | Projections 
                    systemmatrix | SystemMatrix 
                    nrIter | int 
        """
        #from PyQt4 import QtCore; QtCore.pyqtRemoveInputHook(); import pdb; pdb.set_trace()
        super(AdditiveArtAlgorithm, self).__init__(Algorithm.Mode.ADDITIVE_ART, *args)

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
            normalization = np.sum(currentSm * currentSm, axis=0)
            normalization[normalization == 0] = 1.0 #avoid division by zero 
            update = currentSm * (self._projections.data[v] - backprojection) / normalization 
            self._estimate += interpolation.rotate(update, angle, reshape=False)
        self._result.append(self._estimate.copy())

    def ready(self):
        self._result = []
        return True
