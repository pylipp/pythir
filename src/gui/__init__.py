#!/usr/bin/python

""" Sub-package containing all user interface components for PythIR. """

# define authorship information
__authors__     = ['Philipp Metzner']
__author__      = ','.join(__authors__)
__credits__     = [
        ('Momenticons', 'Matte: Basic Icon Pack, CCA')
        ]
__copyright__   = 'Copyright (c) 2015'
__license__     = 'GPL'

# maintanence information
__maintainer__  = 'Philipp Metzner'
__email__       = 'beth.aleph@yahoo.de'


import os.path

import PyQt4.uic 
from PyQt4 import QtCore


def loadUi(modpath, widget):
    """
    Uses the PyQt4.uic.loadUi method to lead the input ui file associated
    with the given module path and widget class information on the input widget.
    
    :param modpath | str
    :param widget  | QWidget
    """
    # generate the uifile path
    basepath = os.path.dirname(modpath)
    basename = widget.__class__.__name__.lower()
    uifile   = os.path.join(basepath, 'ui/%s.ui' % basename)
    uipath   = os.path.dirname(uifile)

    # swap the current path to use the ui file's path
    currdir = QtCore.QDir.currentPath()
    QtCore.QDir.setCurrent(uipath)

    # load the ui
    PyQt4.uic.loadUi(uifile, widget)

    # reset the current QDir path
    QtCore.QDir.setCurrent(currdir)
