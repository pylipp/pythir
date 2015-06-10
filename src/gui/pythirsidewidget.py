#!/usr/bin/python 

from PyQt4 import QtGui, QtCore
import numpy as np
from pythirwidget import PythirWidget
from ..base.program import Program, Phantom, ProjectionSimulator 
from ..base.algorithm import Algorithm 
from ..base.systemmatrixevaluator import SystemMatrixEvaluator
from . import loadUi, translate


class PythirSideWidget(PythirWidget):
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
                Algorithm.Mode.MULTIPLICATIVE_ART, 
            translate("AlgorithmWidget", "SIRT"):
                Algorithm.Mode.SIRT 
            }

    def __init__(self, parent=None):
        super(PythirSideWidget, self).__init__(parent)
        loadUi(__file__, self)

        self.comboBoxSmMode.addItems(self.__class__.SmModeDict.keys())
        self.comboBoxAlgorithmMode.addItems(self.__class__.AlgorithmModeDict.keys())

        # Programs
        self.pushButtonNew.clicked.connect(self.onNew)
        self.pushButtonDelete.clicked.connect(self.onDelete)
        # Phantom
        self.pushButtonLoadFromFile.toggled.connect(self.onLoadFromFile)
        self.pushButtonCreate.toggled.connect(self.onCreate)
        self.pushButtonAddPoissonNoise.clicked.connect(self.showNotImplementedMessage)
        self.pushButtonShow.toggled.connect(self.onShow)
        # Projections
        self.pushButtonProjectPhantom.clicked.connect(self.onProjectPhantom)
        self.pushButtonShowSinogram.clicked.connect(self.onShowSinogram)
        self.spinBoxNrOfViews.valueChanged.connect(self.progressBarProjecting.setMaximum)
        # Algorithm 
        self.pushButtonCompute.clicked.connect(self.onCompute)
        self.comboBoxAlgorithmMode.currentIndexChanged.connect(self.onCompute)
        # Reconstruction
        self.pushButtonPlotResult.clicked.connect(self.onPlotResult)
        self.pushButtonComputeRmse.clicked.connect(self.onComputeRmse)
        self.pushButtonPlotRmse.clicked.connect(self.onPlotRmse)
        

    # # # # # # # # # #
    # PROGRAMSGROUPBOX
    # # # # # # # # # #
    def onDelete(self):
        print self.sizeHint().width()
        print self.minimumSizeHint().width()

    def onNew(self):
        program = Program()
        self._mw.addProgram(program)
        text = QtCore.QString("Program " + str(self._mw.nrOfPrograms))
        programItem = QtGui.QListWidgetItem(text, self.listWidgetPrograms)
        self.listWidgetPrograms.setCurrentItem(programItem)
        self._mw.incNrOfPrograms()

    # # # # # # # # # #
    # PHANTOMGROUPBOX
    # # # # # # # # # #
    def onCreate(self, checked):
        if checked:
            if self.currentProgram() is None:
                return
            self.currentProgram().phantom = Phantom(size=self.spinBoxSize.value())
            self.currentPhantom().create()
            self.updateImageView()
            # Hack
            self.spinBoxNrOfBins.setValue(self.spinBoxSize.value())

    def onLoadFromFile(self, checked):
        if checked:
            dir = QtCore.QDir.current()
            if not dir.cd("src/images"):
                print "PhantomWidget.onLoadFromFile(): could not change dir"
            fileName = QtGui.QFileDialog.getOpenFileName(self,
                    translate("PhantomWidget", "Load phantom"),
                    dir.path(), translate("PhantomWidget", "Images (*.png *.xpm *.jpg)"))
            if not fileName.isNull():
                fileName = unicode(fileName)
                self.currentProgram().phantom = Phantom(fileName=fileName)
                self.currentPhantom().create()
                self.lineEditPath.setText(fileName)
                self.updateImageView()
                self.spinBoxNrOfBins.setValue(self.currentProgram().phantom.size)
            else:
                #FIXME change auto-exclusive button behavior
                self.pushButtonLoadFromFile.setChecked(False)

    def onShow(self, checked):
        #TODO rename this slot
        if checked and self.currentPhantom() is not None:
            self._mw.imageViewPhantom.setImage(self.currentPhantom().data)
            self._mw.imageViewPhantom.setVisible(True)
        else:
            self._mw.imageViewPhantom.setVisible(False)

    def updateImageView(self):
        if not self.pushButtonShow.isChecked():
            return 
        if not self._mw.imageViewPhantom.isVisible():
            return 
        self.onShow(True)

    # # # # # # # # # #
    # PROJECTIONSGROUPBOX
    # # # # # # # # # #
    def onProjectPhantom(self):
        if self.currentPhantom() is None:
            return
        projSimulator = ProjectionSimulator( self.spinBoxNrOfViews.value(),
                self.spinBoxNrOfBins.value(), self.currentPhantom() )
        projSimulator.initProjections()
        projSimulator.projectAll(self.doubleSpinBoxStart.value(),
                self.doubleSpinBoxStop.value())
        self.currentProjectionSimulator = projSimulator

    def onShowSinogram(self):
        if self.currentProjectionSimulator is None:
            return 
        self._mw.imageViewPhantom.setImage(self.currentProjectionSimulator.projections.data)

    # # # # # # # # # #
    # ALGORITHMGROUPBOX
    # # # # # # # # # #
    def onCompute(self, temp):
        smMode = self.__class__.SmModeDict[self.comboBoxSmMode.currentText()]
        smEvaluator = SystemMatrixEvaluator(
                #FIXME horribly unsafe! can be changed between PS and SmE
                self.spinBoxNrOfViews.value(), 
                self.spinBoxNrOfBins.value(), 
                smMode )
        smEvaluator.initSystemMatrix()
        phantom = None 
        if smMode == SystemMatrixEvaluator.Mode.ROTATIONAL:
            phantom = self.currentPhantom()
        smEvaluator.evaluate(
                #FIXME same here 
                self.doubleSpinBoxStart.value(), 
                self.doubleSpinBoxStop.value(),
                phantom )

        algorithm = Algorithm( 
                self.__class__.AlgorithmModeDict[self.comboBoxAlgorithmMode.currentText()], 
                self._mw.currentProjectionSimulator.projections, 
                smEvaluator.systemMatrix,
                self.spinBoxNrOfIterations.value() )

        #import pdb; QtCore.pyqtRemoveInputHook();  pdb.set_trace()
        self._mw.currentProgram()._Program__algorithm = algorithm 
        self._mw.currentProgram().compute()
        #algorithm.compute()

    # # # # # # # # # #
    # RECONSTRUCTIONGROUPBOX
    # # # # # # # # # #
    def onPlotResult(self):
        if self._mw.currentProgram().result is None:
            return
        self._mw.imageViewResults.clear()
        self._mw.imageViewResults.setImage(np.array(self._mw.currentProgram().result))

    def onComputeRmse(self):
        if self._mw.currentProgram().result is None:
            return
        self._mw.currentProgram().computeRmse()

    def onPlotRmse(self, checked):
        if self._mw.currentProgram().rmse is None:
            return 
        if checked:
            self._mw.plotWidgetRmse.clear()
            x, y = self._mw.currentProgram().rmse
            self._mw.plotWidgetRmse.plot(np.array(x), np.array(y))
        self._mw.plotWidgetRmse.setVisible(checked)
