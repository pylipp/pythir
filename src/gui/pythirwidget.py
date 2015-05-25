#!/usr/bin/python 

from PyQt4 import QtGui 

class PythirWidget(QtGui.QWidget):
    """
    """
    def __init__(self, parent=None):
        super(PythirWidget, self).__init__(parent)
        self._mw = None 

    def setMw(self, mw):
        self._mw = mw
