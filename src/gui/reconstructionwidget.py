#!/usr/bin/python 

from PyQt4 import QtGui
from . import loadUi 


class ReconstructionWidget(QtGui.QWidget):
    """
    """
    def __init__(self, parent=None):
        super(ReconstructionWidget, self).__init__(parent)
        self.__mw = parent
        loadUi(__file__, self)
