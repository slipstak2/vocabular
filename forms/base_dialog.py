# -*- coding: utf-8 -*-

from PySide import QtGui


class BaseDialog(QtGui.QDialog):
    def __init__(self, *args, **kwargs):
        super(BaseDialog, self).__init__(*args, **kwargs)
        self.models = []

    def onCloseDialog(self):
        pass

    def reject(self, *args, **kwargs):
        super(BaseDialog, self).reject(*args, **kwargs)
        self.onCloseDialog()

    def accept(self, *args, **kwargs):
        super(BaseDialog, self).accept(*args, **kwargs)
        self.onCloseDialog()
