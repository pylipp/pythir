#!/usr/bin/python 

from PyQt4 import QtGui
from pythirwidget import PythirWidget
from . import loadUi 


class AlgorithmWidget(PythirWidget):
    """
    """
    def __init__(self, parent=None):
        super(AlgorithmWidget, self).__init__(parent)
        self.__mw = parent
        loadUi(__file__, self)
