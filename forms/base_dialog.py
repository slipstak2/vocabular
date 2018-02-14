# -*- coding: utf-8 -*-

from PySide import QtGui


class BaseDialog(QtGui.QDialog):
    def __init__(self, *args, **kwargs):
        super(BaseDialog, self).__init__(*args, **kwargs)
        self.models = []

    def registerModel(self, model):
        self.models.append(model)
        return model

    def releaseModels(self):
        for model in reversed(self.models):
            model.release()

    def reject(self, *args, **kwargs):
        self.releaseModels()
        print 'reject'
        super(BaseDialog, self).reject(*args, **kwargs)

    def accept(self, *args, **kwargs):
        self.releaseModels()
        print 'accept'
        super(BaseDialog, self).accept(*args, **kwargs)
