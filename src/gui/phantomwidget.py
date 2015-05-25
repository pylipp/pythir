#!/usr/bin/python 

from PyQt4 import QtGui, QtCore
from pythirwidget import PythirWidget
from ..base.phantom import Phantom
from . import loadUi, translate


class PhantomWidget(PythirWidget):
    """
    """
    def __init__(self, parent=None):
        super(PhantomWidget, self).__init__(parent)
        loadUi(__file__, self)

        self.pushButtonLoadFromFile.toggled.connect(self.onLoadFromFile)
        self.pushButtonCreate.toggled.connect(self.onCreate)
        self.pushButtonAddPoissonNoise.clicked.connect(self.showNotImplementedMessage)
        self.pushButtonShow.toggled.connect(self.onShow)

    def onCreate(self, checked):
        if checked:
            self.currentProgram().phantom = Phantom(size=self.spinBoxSize.value())
            self.currentPhantom().create()
            self.updateImageView()

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
            else:
                #FIXME change auto-exclusive button behavior
                self.pushButtonLoadFromFile.setChecked(False)

    def onShow(self, checked):
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

