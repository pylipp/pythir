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
    def __init__(self, views, nrBins, phantom=None, start=0, stop=180):
        self.__phantom = phantom 
        self.__nrBins = nrBins
        self._views = views
        self._start = start 
        self._stop = stop
        self._angleInc = (stop-start)/float(views)
        self.__projections = None

    @property 
    def loadSize(self):
        return self._views

    @property 
    def phantom(self):
        return self.__phantom 

    @property 
    def projections(self):
        return self.__projections

    @property 
    def views(self):
        return self._views 

    def initProjections(self):
        """ Initialize the projections object. """
        self.__projections = Projections(self._views, self.__nrBins)

    def projectAll(self, start=0, stop=180):
        """ 
        Simulate a parallel-beam x-ray projection by summing up the phantom
        data matrix column wise, yielding a sinogram line. 
        To this end, the number of bins (that the phantom is projected onto)
        and the phantom pixel size should be equal. Otherwise, the phantom
        needs to be reshaped.
        """
        if self.readyForProjecting():
            for a in range(0, self._views):
                if a%25==0:
                    print "Projecting view " + str(a)
                self.computeOne(a)

    def computeOne(self, view):
        """
        Helper function. Performs a single projection.
        Required in ProjectionSimulatorHandler.process() to signal progress
        after a single projection. 

        :param      view | int 
        """
        rotPhantom = self.phantom.rotate(self._start - view*self._angleInc)
        self.__projections.project(view, rotPhantom)

    def ready(self):
        """
        Convenience method for checking prerequisites for projecting.

        :return     isReady | bool 
        """
        if self.phantom is None or self.projections is None: 
            return False
        if self.__nrBins != self.phantom.size:
            pass #TODO resize phantom
        return True
