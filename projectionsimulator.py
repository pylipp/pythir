#!/usr/bin/python 

import numpy as np 

from phantom import Phantom

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
        self.__systemMatrix.add(0, self.phantom.data > 0)

        angleInc = (stop-start)/float(views)
        for a in range(1, views):
            if a%10==0:
                print "Projecting view " + str(a)
            rotPhantom = self.phantom.rotate(a*angleInc)
            self.__systemMatrix.add(a, rotPhantom > 0)
            self.__projections.project(a, rotPhantom)


class Projections(object):

    def __init__(self, views, nrBins):
        self.__views = views 
        self.__nrBins = nrBins 
        self.__data = np.zeros((views, nrBins))

    @property
    def data(self):
        return self.__data

    def project(self, view, phantom):
        if isinstance(phantom, Phantom):
            phantom = phantom.data
        self.__data[view, :] = np.sum(phantom, axis=0)


class SystemMatrix(object):

    def __init__(self, dimensions):
        self.__dimensions = dimensions 
        self.__data = np.zeros(dimensions)

    @property
    def data(self):
        return self.__data

    def add(self, view, data):
        self.data[view,:,:] = data

    def reshape(self, shape):
        assert(np.product(shape) == np.product(self.__dimensions))
        return np.reshape(self.data, shape).copy()
