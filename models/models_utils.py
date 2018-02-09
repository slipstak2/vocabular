# -*- coding: utf-8 -*-

from PySide import QtCore

def setStartGeometry(parentWindow, dialog):
    parentGeom = parentWindow.geometry()
    geom = QtCore.QRect(parentGeom.left() + 8, parentGeom.top() + 30, dialog.width(), dialog.height())
    dialog.setGeometry(geom)
