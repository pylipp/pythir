#!/usr/bin/python 

import sys
from PyQt4 import QtGui 
from src.gui.pythirmainwindow import PythirMainWindow

app = QtGui.QApplication(sys.argv)
mw = PythirMainWindow(app)
mw.show()
sys.exit(app.exec_())
