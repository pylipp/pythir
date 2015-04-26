#!/usr/bin/python 

import numpy as np 
from scipy.ndimage import interpolation

class ProjectionSimulator(object):

    def __init__(self, slice=None):
        self.__slice = slice 
        self.__bins = None

    @property 
    def slice(self):
        return self.__slice 

    def project(self, nrBins, start, stop, angles):
        if self.slice is None:
            return 
        assert(nrBins == self.slice.size)

        # initialize bins 
        self.__bins = np.zeros((angles, nrBins))

        #fill first bin 
        self.__bins[0,:] = np.sum(self.slice, axis=0)

        slice = self.slice.copy()
        angle = (stop-start)/float(angles)
        for a in range(1, angles):
            slice = interpolation.rotate(slice, angle)
            self.__bins[a,:] = np.sum(slice, axis=0)
