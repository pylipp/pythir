#!/usr/bin/python 

from PyQt4 import QtGui, QtCore
from pythirwidget import PythirWidget
from ..base.projectionsimulator import ProjectionSimulator
from . import loadUi 


class ProjectionsWidget(PythirWidget):
    """
    """
    def __init__(self, parent=None):
        super(ProjectionsWidget, self).__init__(parent)
        loadUi(__file__, self)
        self.__projectionSimulator = None

        self.pushButtonProjectPhantom.clicked.connect(self.onProjectPhantom)
        self.pushButtonShowSinogram.clicked.connect(self.onShowSinogram)
        self.spinBoxNrOfViews.valueChanged.connect(self.progressBarProjecting.setMaximum)

    def onProjectPhantom(self):
        projSimulator = ProjectionSimulator( self.spinBoxNrOfViews.value(),
                self.spinBoxNrOfBins.value(), self.currentPhantom() )
        projSimulator.initProjections()
        projSimulator.projectAll(self.doubleSpinBoxStart.value(),
                self.doubleSpinBoxStop.value())
        self.__projectionSimulator = projSimulator 
        self.currentProjectionSimulator = projSimulator

    def onShowSinogram(self):
        if self.__projectionSimulator is None:
            return 
        self._mw.imageViewPhantom.setImage(self.__projectionSimulator.projections.data)
