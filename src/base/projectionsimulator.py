#!/usr/bin/python 

from projections import Projections

class ProjectionSimulator(object):
    """
    Simple class to simulate parallel-beam x-ray projections of a phantom. 
    Since the projections are usually obtained from a phantom, it's preferred
    (for convenience) to match the number of bins to the pixel size of the
    phantom. Otherwise, the phantom needs to be resized before being projected.
    If the reconstruction is performed using a binary system matrix, that
    matrix can be evaluated during the projection. 
    """
    def __init__(self, views, nrBins, phantom=None):
        self.__phantom = phantom 
        self.__nrBins = nrBins
        self.__views = views
        self.__projections = None

    @property 
    def phantom(self):
        return self.__phantom 

    @property 
    def projections(self):
        return self.__projections

    def initProjections(self):
        self.__projections = Projections(self.__views, self.__nrBins)

    def projectAll(self, start, stop):
        if self.phantom is None or self.projections is None: 
            return 
        if self.__nrBins != self.phantom.size:
            pass #resize phantom

        #project first view
        self.__projections.project(0, self.phantom)
        views = self.__views
        angleInc = (stop-start)/float(views)
        for a in range(1, views):
            if a%25==0:
                print "Projecting view " + str(a)
            rotPhantom = self.phantom.rotate(-a*angleInc)
            self.__projections.project(a, rotPhantom)
