#!/usr/bin/python 

from PyQt4 import QtGui
from . import loadUi 


class PhantomWidget(QtGui.QWidget):
    """
    """
    def __init__(self, parent=None):
        super(PhantomWidget, self).__init__(parent)
        self.__mw = parent
        loadUi(__file__, self)
