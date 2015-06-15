#!/usr/bin/python 

from PyQt4 import QtCore, QtGui 
from . import translate

class ProjectionSimulatorHandler(QtCore.QObject):
    """
    Wrapper class around a ProjectionSimulator instance. 
    Prepares the ProjectionSimulator. In process() it calls the
    ProjectionSimulator.projectOne() method and emits a signal about the
    current progress after each iteration.

    :signal     updateProgress[int]
                finished
    """
    updateProgress = QtCore.pyqtSignal(int)
    finished = QtCore.pyqtSignal()

    def __init__(self, projSimulator=None, parent=None):
        """
        :param      projSimulator | ProjectionSimulator 
        """
        super(ProjectionSimulatorHandler, self).__init__(parent)
        self._projSimulator = projSimulator 
        self._projSimulator.initProjections()

    def process(self):
        """
        Main entry for computation. 
        Connecting between the progressbar of the GUI and the ProjectionSimulator
        instance of the backend.
        """
        if self._projSimulator is not None:
            if self._projSimulator.readyForProjecting():
                views = self._projSimulator.views
                for v in range(views):
                    self._projSimulator.projectOne(v)
                    self.updateProgress.emit(v+1)
                self.finished.emit()
        else:
            QtGui.QMessageBox.information(None, 
                    translate("ProjectionSimulatorHandler", "An error occured"),
                    translate("ProjectionSimulatorHandler",
                        "The projection of the phantom is not performed."))
