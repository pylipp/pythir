#!/usr/bin/python 

from PyQt4 import QtGui, QtCore
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

        self.__subWidgets = [self.programsWidget, self.phantomWidget,
                self.projectionsWidget, self.algorithmWidget,
                self.reconstructionWidget]
        self.__programs = []
        self.__nrOfPrograms = 0

        self.setVisibilityAtInit()
        self.setMwToWidgets()

        # CONNECTIONS #

    @property 
    def nrOfPrograms(self):
        return self.__nrOfPrograms 

    def addProgram(self, program):
        self.__programs.append(program)

    def currentPhantom(self):
        if self.currentProgram() is None:
            return 
        return self.currentProgram().phantom 

    def currentProgram(self):
        index = self.programsWidget.listWidgetPrograms.currentRow()
        if index > -1 and index < len(self.__programs):
            return self.__programs[index]
        return 

    @property
    def currentProjectionSimulator(self):
        if self.currentProgram() is None:
            return 
        return self.currentProgram().projectionSimulator 

    @currentProjectionSimulator.setter 
    def currentProjectionSimulator(self, ps):
        self.currentProgram().projectionSimulator = ps

    def incNrOfPrograms(self):
        self.__nrOfPrograms += 1

    def setMwToWidgets(self):
        for w in self.__subWidgets:
            w.setMw(self)

    def setVisibilityAtInit(self):
        self.imageViewPhantom.setVisible(False)
        self.plotWidgetRmse.setVisible(False)
        for w in self.__subWidgets:
            break
            #w.groupBox.setVisible(False)
