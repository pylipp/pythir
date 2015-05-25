#!/usr/bin/python 

from PyQt4 import QtGui 

class PythirWidget(QtGui.QWidget):
    """
    """
    def __init__(self, parent=None):
        super(PythirWidget, self).__init__(parent)
        self._mw = None 

    def currentPhantom(self):
        return self._mw.currentPhantom()

    def currentProgram(self):
        return self._mw.currentProgram() 

    @property
    def currentProjectionSimulator(self):
        return self._mw.currentProjectionSimulator() 

    @currentProjectionSimulator.setter 
    def currentProjectionSimulator(self, ps):
        self._mw.currentProjectionSimulator = ps

    def setMw(self, mw):
        self._mw = mw

    def showNotImplementedMessage(self):
        self._mw.statusBar().showMessage("Not implemented yet :(", 3000)
