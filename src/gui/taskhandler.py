#!/usr/bin/python 

from PyQt4 import QtCore, QtGui 
import time
from . import translate

class TaskHandler(QtCore.QObject):
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

    def __init__(self, task=None, parent=None):
        """
        :param      task | ProjectionSimulator or Algorithm
        """
        super(TaskHandler, self).__init__(parent)
        self._task = task

    def process(self):
        """
        Main entry for computation. 
        Connecting between the progressbar of the GUI and the ProjectionSimulator
        instance of the backend.
        """
        if self._task is not None:
            if self._task.ready():
                start = time.time()
                for i in range(self._task.loadSize):
                    self._task.computeOne(i)
                    self.updateProgress.emit(i+1)
                print "Processing time: {0}".format(time.time()-start)
                self.finished.emit()
        else:
            QtGui.QMessageBox.information(None, 
                    translate("ProjectionSimulatorHandler", "An error occured"),
                    translate("ProjectionSimulatorHandler",
                        "The projection of the phantom is not performed."))
