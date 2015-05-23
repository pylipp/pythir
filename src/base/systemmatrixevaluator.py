#!/usr/bin/python 

import numpy as np
from systemmatrix import SystemMatrix
from . import enum

class SystemMatrixEvaluator(object):
    """
    This class evaluates the matrix that holds the information about the
    imaging process of the current system. 
    Description of Modes:
    - ROTATIONAL: For each view, a system matrix slice is defined as the binary
      mask of the given phantom. This is somehow cheating because it assumes
      the shape of the phantom to be given. Note that this also requires
      rotating the estimate in the later computation of the algorithm.
    - LINE_LENGTH: For each view and each ray that is cast from the parallel
      beam source to the detector beyond the phanom/object, an entry in a
      system matrix slice is defined as the sum of ray segments in the
      corresponding pixel. Not implemented yet.
    """
    #TODO refine ROTATIONAL mode
    
    Mode = enum( 
            ROTATIONAL=0, 
            BINARY=1,
            LINE_LENGTH=2 )

    def __init__(self, views, size, mode):
        """
        size is the (quadratic) system matrix' pixel size.
        :param      views | int 
                    size | int 
                    mode | SystemMatrixEvaluator.Mode
        :attrib     __systemMatrix | SystemMatrix 
        """
        self.__size = size 
        self.__views = views 
        self.__mode = mode
        self.__systemMatrix = None 

    @property 
    def mode(self):
        return self.__mode 

    @property 
    def size(self):
        return self.__size 

    @property 
    def views(self):
        return self.__views 

    @property 
    def systemMatrix(self):
        return self.__systemMatrix

    def initSystemMatrix(self, size=None, views=None):
        """ 
        The system matrix is initialized with either the values given at class
        initialization or new arguments. 

        :param      size, views | int 
        """
        if size is None:
            size = self.size 
        if views is None:
            views = self.views
        self.__systemMatrix = SystemMatrix((views,size,size))

    def evaluate(self, start, stop, phantom=None):
        """ 
        The actual computation is performed. 
        The phantom argument is only required for ROTATIONAL mode.
        The angular range (start, stop) should be given in degrees.

        :param      start, stop | int 
                    phantom | Phantom or None
        """
        if self.__systemMatrix is None:
            return 

        if self.mode == SystemMatrixEvaluator.Mode.ROTATIONAL:
            if phantom is None:
                return
            #FIXME phantom may need to be shrinked
            if self.size != phantom.size:
                print "SME.evaluate(): Non-matching sizes"
                return 
            self.systemMatrix.add(0, phantom.data > 0.01)
            angleInc = (stop-start)/float(self.views)
            for a in range(1, self.views):
                if a%25 == 0:
                    print "Evaluating system matrix for view " + str(a)
                rotPhantom = phantom.rotate(-a*angleInc)
                self.systemMatrix.add(a, rotPhantom > 0.01)

        elif self.mode == SystemMatrixEvaluator.Mode.BINARY:
            if phantom is None:
                return
            #FIXME phantom may need to be shrinked
            if self.size != phantom.size:
                print "SME.evaluate(): Non-matching sizes"
                return 
            radius = (self.size-1)*0.5
            mask = phantom.createCircularMask((self.size,self.size),
                    (radius,radius), radius)
            for a in range(self.views):
                self.systemMatrix.add(a, mask.astype(np.float16))

        elif self.mode == SystemMatrixEvaluator.Mode.LINE_LENGTH:
            angleInc = (stop-start)/float(self.views)
            # this mode has a custom number of views 
            start = -45 
            stop = 45
            views = (stop-start)/angleInc
            delta = 1.0
            pixelsize = 1.0
            systemMatrix = SystemMatrix(self.size, self.size, views)
            nrBins = self.size
            yIndices = 0.5*self.size - np.arange(self.size+1)
            yIndices *= pixelsize
            for v in range(views):
                alpha = start + v*angleInc
                invCosAlpha = 1.0/np.cos(alpha)
                sinAlpha = np.sin(alpha)
                for m in range(nrBins):
                    mOffset = -0.5*delta*(nrBins - 2*m - 1)
                    xIndices = invCosAlpha * (yIndices * sinAlpha + mOffset)
                    inside = np.abs(xIndices) < 0.5*self.size
                    deltaX = xIndices[1:] - xIndices[:-1]
                    deltaY = yIndices[1:] - yIndices[:-1]
                    intersectionLengths = np.sqrt( deltaX*delta + deltaY*deltaY )



