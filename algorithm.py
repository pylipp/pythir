#!/usr/bin/python 

import numpy as np 

class Algorithm(object):

    def __init__(self, mode, projections, systemMatrix, nrIter):
        self.__mode = mode
        self.__projections = projections 
        self.__systemMatrix = systemMatrix 
        self.__nrIter = nrIter
        self.__result = None 

    def compute(self):
        self.__result = np.zeros(self.__systemMatrix.shape[1:3])
        if self.__mode == Mode.ART:
            self.computeART(self.__nrIter, self.__projections, self.__systemMatrix, self.__result)

    def computeART(self, nrIter, projections, systemMatrix, result):
        pass

class Mode:
    ART = 0
