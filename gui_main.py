#!/usr/bin/python 

import sys
from PyQt4 import QtGui, QtCore 
from src.gui.pythirmainwindow import PythirMainWindow

app = QtGui.QApplication(sys.argv)
app.setStyle("Plastique")
"""
qtTranslator = QtCore.QTranslator()
if qtTranslator.load("qt_de",
        QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)):
    app.installTranslator(qtTranslator)
deTranslator = QtCore.QTranslator()
if qtTranslator.load("pythir_de", "src/i18n"):
    app.installTranslator(qtTranslator)
"""
mw = PythirMainWindow(app)
mw.show()
sys.exit(app.exec_())
