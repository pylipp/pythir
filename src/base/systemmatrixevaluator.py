#!/usr/bin/python 

from systemmatrix import SystemMatrix
from . import enum

class SystemMatrixEvaluator(object):
    """
    """
    
    Mode = enum( 
            ROTATIONAL=0, 
            LINE_LENGTH=1 )

    def __init__(self, views, size, mode):
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
        if size is None:
            size = self.size 
        if views is None:
            views = self.views
        self.__systemMatrix = SystemMatrix((views,size,size))

    def evaluate(self, start, stop, phantom=None):
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
