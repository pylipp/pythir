#!/usr/bin/python 

from PyQt4 import QtGui, QtCore
import numpy as np
from pythirwidget import PythirWidget
from ..base.program import Program, Phantom, ProjectionSimulator 
from ..base.algorithm import Algorithm 
from ..base.additive_art_algorithm import AdditiveArtAlgorithm
from ..base.multiplicative_art_algorithm import MultiplicativeArtAlgorithm
from ..base.simultaneous_irt_algorithm import SimultaneousIrtAlgorithm
from ..base.systemmatrixevaluator import SystemMatrixEvaluator
from taskhandler import TaskHandler
from . import loadUi, translate


class PythirSideWidget(PythirWidget):
    """
    """

    SmModeDict = {
            translate("PythirSideWidget", "Rotational"):
                SystemMatrixEvaluator.Mode.ROTATIONAL, 
            translate("PythirSideWidget", "Binary"):
                SystemMatrixEvaluator.Mode.BINARY, 
            translate("PythirSideWidget", "Line length"):
                SystemMatrixEvaluator.Mode.LINE_LENGTH 
            }

    AlgorithmModeDict = {
            translate("PythirSideWidget", "Additive ART"):
                Algorithm.Mode.ADDITIVE_ART, 
            translate("PythirSideWidget", "Multiplicative ART"):
                Algorithm.Mode.MULTIPLICATIVE_ART, 
            translate("PythirSideWidget", "SIRT"):
                Algorithm.Mode.SIRT 
            }

    def __init__(self, parent=None):
        super(PythirSideWidget, self).__init__(parent)
        loadUi(__file__, self)

        self._threads = []

        # Layout adjustments
        self.comboBoxSmMode.addItems(self.__class__.SmModeDict.keys())
        self.comboBoxAlgorithmMode.addItems(self.__class__.AlgorithmModeDict.keys())
        self.progressBarProjecting.hide()
        self.progressBarComputing.hide()

        # Programs
        self.pushButtonNew.clicked.connect(self.onNew)
        self.pushButtonDelete.clicked.connect(self.onDelete)
        # Phantom
        self.pushButtonLoadFromFile.toggled.connect(self.onLoadFromFile)
        self.pushButtonCreate.toggled.connect(self.onCreate)
        self.pushButtonAddPoissonNoise.clicked.connect(self.onTogglePoissonNoise)
        self.pushButtonShow.toggled.connect(self.onShow)
        # Projections
        self.pushButtonProjectPhantom.clicked.connect(self.onProjectPhantom)
        self.pushButtonShowSinogram.clicked.connect(self.onShowSinogram)
        self.spinBoxNrOfViews.valueChanged.connect(self.progressBarProjecting.setMaximum)
        # Algorithm 
        self.pushButtonCompute.clicked.connect(self.onCompute)
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

    def onTogglePoissonNoise(self, checked):
        if self.currentPhantom() is None:
            return 
        self.currentPhantom().toggleNoise(checked, self.spinBoxMaxPhotons.value())
        self.updateImageView()

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
        self.progressBarProjecting.setVisible(True)
        self.progressBarProjecting.setRange(0, self.spinBoxNrOfViews.value())
        projSimulator = ProjectionSimulator( self.spinBoxNrOfViews.value(),
                self.spinBoxNrOfBins.value(), self.currentPhantom(),
                self.doubleSpinBoxStart.value(), self.doubleSpinBoxStop.value())
        projSimulator.initProjections()
        self.currentProjectionSimulator = projSimulator
        self._handler = TaskHandler(projSimulator)
        self.setupHandlerAndThread(self._handler, self.progressBarProjecting)

    def setupHandlerAndThread(self, handler, progressBar):
        self._threads.append(QtCore.QThread())
        thread = self._threads[-1]
        handler.moveToThread(thread)
        thread.started.connect(handler.process)
        handler.updateProgress.connect(progressBar.setValue)
        #TODO move all this into separate function
        handler.finished.connect(lambda: progressBar.setValue(progressBar.maximum()))
        handler.finished.connect(handler.deleteLater)
        handler.finished.connect(progressBar.hide)
        thread.finished.connect(thread.deleteLater)
        thread.start()

    def onShowSinogram(self):
        #TODO make this handle toggle behavior?
        #if self.currentProjectionSimulator is None:
            #return 
        self._mw.imageViewPhantom.setVisible(True)
        self._mw.imageViewPhantom.setImage(self._mw.currentProjectionSimulator.projections.data)

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

        algorithmMode = PythirSideWidget.AlgorithmModeDict[self.comboBoxAlgorithmMode.currentText()]
        args = (self._mw.currentProjectionSimulator.projections, 
                smEvaluator.systemMatrix,
                self.spinBoxNrOfIterations.value() )
        if algorithmMode == Algorithm.Mode.ADDITIVE_ART:
            self._mw.currentProgram()._Program__algorithm = AdditiveArtAlgorithm(*args)
        elif algorithmMode == Algorithm.Mode.MULTIPLICATIVE_ART:
            self._mw.currentProgram()._Program__algorithm = MultiplicativeArtAlgorithm(*args)
        elif algorithmMode == Algorithm.Mode.SIRT:
            self._mw.currentProgram()._Program__algorithm = SimultaneousIrtAlgorithm(
                *args, relaxation=1.4) #TODO turn this into user definable parameter
        else:
            pass
            self._mw.currentProgram()._Program__algorithm = None #algorithm 
        # def current('algorithm')
        algorithm = self._mw.currentProgram()._Program__algorithm 
        self.progressBarComputing.setVisible(True)
        self.progressBarComputing.setRange(0, self.spinBoxNrOfIterations.value())
        self.progressBarComputing.setValue(self.progressBarComputing.minimum())
        self._handler = TaskHandler(algorithm)
        self.setupHandlerAndThread(self._handler, self.progressBarComputing)


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
