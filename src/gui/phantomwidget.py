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
        self.pushButtonShow.toggled.connect(self.onShow)

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
                self._mw.currentProgram().phantom = Phantom(fileName=fileName)
                self._mw.currentPhantom().create()
                self.lineEditPath.setText(fileName)

    def onShow(self, checked):
        self._mw.imageViewPhantom.setVisible(checked)
        if checked:
            self._mw.imageViewPhantom.setImage(self._mw.currentPhantom().data)

