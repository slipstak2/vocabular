# -*- coding: utf-8 -*-

from PySide import QtGui


class BaseDialog(QtGui.QDialog):
    def __init__(self, *args, **kwargs):
        super(BaseDialog, self).__init__(*args, **kwargs)
        self.models = []

    def reject(self, *args, **kwargs):
        print 'reject'
        super(BaseDialog, self).reject(*args, **kwargs)

    def accept(self, *args, **kwargs):
        print 'accept'
        super(BaseDialog, self).accept(*args, **kwargs)
