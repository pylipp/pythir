#!/usr/bin/python 

import numpy as np 
import time

class Algorithm(object):

    def __init__(self, mode, projections, systemMatrix, nrIter):
        self.__mode = mode
        self.__projections = projections 
        self.__systemMatrix = systemMatrix 
        self.__nrIter = nrIter
        self.__result = None 

    @property 
    def result(self):
        return self.__result 

    def compute(self):
        if self.__mode == Mode.ART:
            self.computeART(self.__nrIter, self.__projections, self.__systemMatrix, self.__result)

    def computeART(self, nrIter, projections, systemMatrix, result):
        estimate = np.zeros_like(systemMatrix.data[0])
        start = time.time()
        for n in range(nrIter):
            print "Computing iteration " + str(n)
            for v in range(projections.views):
                try:
                    currentSm = systemMatrix.data[v]
                    currentProjections = projections.data[v]
                    backprojection = np.sum(currentSm * estimate, axis=0)
                    normalization = np.sum(currentSm * currentSm, axis=0)
                    normalization[normalization == 0] = 1.0
                    update = currentSm * (currentProjections - backprojection) / normalization 
                    estimate += update
                except ValueError:
                    import pdb; pdb.set_trace()
        end = time.time()
        print "Computation time for ART: " + str(end-start)
        self.__result = estimate

class Mode:
    ART = 0
