#!/usr/bin/python 

from projections import Projections
from systemmatrix import SystemMatrix

class ProjectionSimulator(object):
    """
    Simple class to simulate parallel-beam x-ray projections of a phantom. 
    Since the projections are usually obtained from a phantom, it's preferred
    (for convenience) to match the number of bins to the pixel size of the
    phantom. Otherwise, the phantom needs to be resized before being projected.
    If the reconstruction is performed using a binary system matrix, that
    matrix can be evaluated during the projection. 
    """
    #FIXME The system matrix evaluation should be handled separately, with an
    #accordingly sampled phantom

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

    def initProjections(self, nrBins, views):
        self.__projections = Projections(views, nrBins)

    def initSystemMatrix(self, size=None, views=None):
        #FIXME phantom needs to be shrinked
        self.__systemMatrix = SystemMatrix((views,size,size))

    def projectAll(self, nrBins, start, stop, views):
        if self.phantom is None or self.projections is None or \
                self.systemMatrix is None:
            return 
        if nrBins != self.phantom.size:
            pass #resize phantom

        #project first view
        self.__projections.project(0, self.phantom)
        #FIXME this is not correct. adjust add() or data to be added
        self.__systemMatrix.add(0, self.phantom.data > 0.01)

        angleInc = (stop-start)/float(views)
        for a in range(1, views):
            if a%25==0:
                print "Projecting view " + str(a)
            rotPhantom = self.phantom.rotate(-a*angleInc)
            self.__systemMatrix.add(a, rotPhantom > 0)
            self.__projections.project(a, rotPhantom)
