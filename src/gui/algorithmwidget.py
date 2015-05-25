#!/usr/bin/python 

from PyQt4 import QtGui
from pythirwidget import PythirWidget
from ..base.systemmatrixevaluator import SystemMatrixEvaluator
from ..base.algorithm import Algorithm
from . import loadUi, translate


class AlgorithmWidget(PythirWidget):
    """
    """

    SmModeDict = {
            translate("AlgorithmWidget", "Rotational"):
                SystemMatrixEvaluator.Mode.ROTATIONAL, 
            translate("AlgorithmWidget", "Binary"):
                SystemMatrixEvaluator.Mode.BINARY, 
            translate("AlgorithmWidget", "Line length"):
                SystemMatrixEvaluator.Mode.LINE_LENGTH 
            }

    AlgorithmModeDict = {
            translate("AlgorithmWidget", "Additive ART"):
                Algorithm.Mode.ADDITIVE_ART, 
            translate("AlgorithmWidget", "Multiplicative ART"):
                Algorithm.Mode.MULTIPLICATIVE_ART 
            }

    def __init__(self, parent=None):
        super(AlgorithmWidget, self).__init__(parent)
        loadUi(__file__, self)

        self.comboBoxSmMode.addItems(AlgorithmWidget.SmModeDict.keys())
        self.comboBoxAlgorithmMode.addItems(AlgorithmWidget.AlgorithmModeDict.keys())

        self.pushButtonCompute.clicked.connect(self.onCompute)

    def onCompute(self):
        smMode = AlgorithmWidget.SmModeDict[self.comboBoxSmMode.currentText()]
        smEvaluator = SystemMatrixEvaluator(
                #FIXME horribly unsafe! can be changed between PS and SmE
                self._mw.projectionsWidget.spinBoxNrOfViews.value(), 
                self._mw.projectionsWidget.spinBoxNrOfBins.value(), 
                smMode )
        smEvaluator.initSystemMatrix()
        phantom = None 
        if smMode == SystemMatrixEvaluator.Mode.ROTATIONAL:
            phantom = self.currentPhantom()
        smEvaluator.evaluate(
                #FIXME same here 
                self._mw.projectionsWidget.doubleSpinBoxStart.value(), 
                self._mw.projectionsWidget.doubleSpinBoxStop.value(),
                phantom )

        algorithm = Algorithm( 
                AlgorithmWidget.AlgorithmModeDict[self.comboBoxAlgorithmMode.currentText()], 
                #FIXME error PS not callable
                self.currentProjectionSimulator.projections, 
                smEvaluator.systemMatrix,
                self.spinBoxNrOfIterations.value() )

        algorithm.compute()
