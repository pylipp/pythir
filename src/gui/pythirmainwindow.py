#!/usr/bin/python 

from PyQt4 import QtGui
import numpy as np
from . import loadUi 


class PythirMainWindow(QtGui.QMainWindow):
    """
    """
    def __init__(self, app=None):
        super(PythirMainWindow, self).__init__()
        self.__app = app 
        loadUi(__file__, self)
        # add 3D data for demonstration purpose
        self.r = np.random.rand(10,100,100)
        self.graphicsViewResults.setImage(self.r)
