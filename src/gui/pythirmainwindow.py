#!/usr/bin/python 

from __future__ import print_function
from PyQt4 import QtGui, QtCore
from . import loadUi 


class PythirMainWindow(QtGui.QMainWindow):
    """
    """
    def __init__(self, app=None):
        super(PythirMainWindow, self).__init__()
        self.__app = app 
        loadUi(__file__, self)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        #FIXME adjust the width of the sideWidget
        #self.splitter_2.setStretchFactor(0, 0)
        #sh = self.splitter_2.sizeHint()
        #print( sh.width(), sh.height())
        #print(self.splitter_2.sizes())
        #self.splitter_2.splitterMoved.connect(lambda:
                #print(self.splitter_2.widget(0).widget().width() ))
        #self.splitter_2.widget(0).resize(354, 
                #self.splitter_2.widget(0).widget().height())

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
        index = self.sideWidget.listWidgetPrograms.currentRow()
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
        self.sideWidget.setMw(self)

    def setVisibilityAtInit(self):
        self.imageViewPhantom.setVisible(False)
        self.plotWidgetRmse.setVisible(False)
