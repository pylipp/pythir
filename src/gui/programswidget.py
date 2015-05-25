#!/usr/bin/python 

from PyQt4 import QtGui, QtCore
from ..base.program import Program
from pythirwidget import PythirWidget
from . import loadUi 


class ProgramsWidget(PythirWidget):
    """
    """
    def __init__(self, parent=None):
        super(ProgramsWidget, self).__init__(parent)
        loadUi(__file__, self)

        self.pushButtonNew.clicked.connect(self.onNew)

    def onNew(self):
        program = Program()
        self._mw.addProgram(program)
        text = QtCore.QString("Program " + str(self._mw.nrOfPrograms))
        programItem = QtGui.QListWidgetItem(text, self.listWidgetPrograms)
        self.listWidgetPrograms.setCurrentItem(programItem)
        self._mw.incNrOfPrograms()
