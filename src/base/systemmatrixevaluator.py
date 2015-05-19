#!/usr/bin/python 

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
            LINE_LENGTH=1 )

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
