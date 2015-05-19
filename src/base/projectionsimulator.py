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
        """ Initialize the projections object. """
        self.__projections = Projections(self.__views, self.__nrBins)

    def projectAll(self, start, stop):
        """ 
        Simulate a parallel-beam x-ray projection by summing up the phantom
        data matrix column wise, yielding a sinogram line. 
        To this end, the number of bins (that the phantom is projected onto)
        and the phantom pixel size should be equal. Otherwise, the phantom
        needs to be reshaped.
        """
        if self.phantom is None or self.projections is None: 
            return 
        if self.__nrBins != self.phantom.size:
            pass #TODO resize phantom

        #project first view
        self.__projections.project(0, self.phantom)
        views = self.__views
        angleInc = (stop-start)/float(views)
        for a in range(1, views):
            if a%25==0:
                print "Projecting view " + str(a)
            rotPhantom = self.phantom.rotate(-a*angleInc)
            self.__projections.project(a, rotPhantom)
