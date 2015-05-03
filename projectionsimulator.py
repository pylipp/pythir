#!/usr/bin/python 

import numpy as np 

from projections import Projections
from systemmatrix import SystemMatrix

class ProjectionSimulator(object):

    def __init__(self, phantom=None):
        self.__phantom = phantom 
        self.__projections = None
        self.__systemMatrix = None

    @property 
    def phantom(self):
        return self.__phantom 

    @property 
    def projections(self):
        return self.__projections

    @property 
    def systemMatrix(self):
        return self.__systemMatrix

    def projectAll(self, nrBins, start, stop, views):
        if self.phantom is None:
            return 
        assert(nrBins == self.phantom.size)

        # initialize bins 
        self.__projections = Projections(views, nrBins)
        size = self.phantom.size 
        self.__systemMatrix = SystemMatrix((views,size,size))

        #project first view
        self.__projections.project(0, self.phantom)
        #FIXME this is not correct. adjust add() or data to be added
        self.__systemMatrix.add(0, self.phantom.data > 0)

        angleInc = (stop-start)/float(views)
        for a in range(1, views):
            if a%25==0:
                print "Projecting view " + str(a)
            rotPhantom = self.phantom.rotate(a*angleInc)
            self.__systemMatrix.add(a, rotPhantom > 0)
            self.__projections.project(a, rotPhantom)
