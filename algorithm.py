#!/usr/bin/python 

import numpy as np 

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
        self.__result = np.zeros(self.__systemMatrix.shape[1])
        if self.__mode == Mode.ART:
            self.computeART(self.__nrIter, self.__projections, self.__systemMatrix, self.__result)

    def computeART(self, nrIter, projections, systemMatrix, result):
        result = np.zeros(systemMatrix.shape[1])
        for n in range(nrIter):
            print "Computing iteration " + str(n)
            for j in range(projections.totalSize):
                try:
                    view = j/projections.nrBins
                    ravProjections = projections.data1d
                    currentSmLine = systemMatrix.data[view, :, j%projections.nrBins]
                    currentResultLine = result[j%projections.nrBins::projections.nrBins]
                    backprojection = ravProjections[j] - np.sum(currentSmLine * currentResultLine)
                    normalization = np.sum(currentSmLine * currentSmLine)
                    update = currentSmLine * backprojection / normalization if normalization > 0 else 0.0
                    currentResultLine += update
                except ValueError:
                    import pdb; pdb.set_trace()
        self.__result = result

class Mode:
    ART = 0
