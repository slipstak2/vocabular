from PySide import QtSql, QtCore, QtGui
from PySide.QtCore import Slot as pyqtSlot
from forms.utils import onBtnLeave, onBtnEnter

import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)


class ButtonDelegate(QtGui.QItemDelegate):
    def __init__(self, parentWindow, parent, model):
        QtGui.QItemDelegate.__init__(self, parent)
        self.parentWindow = parentWindow
        self.model = model
        self.iconPath = ":/res/images/unknown.png"

    def createEditor(self, parent, option, index):
        btn = QtGui.QPushButton(str(index.data()), parent)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.iconPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        btn.setIcon(icon)
        btn.setIconSize(QtCore.QSize(24, 24))
        btn.setFlat(True)
        btn.clicked.connect(lambda: self.onBtnClicked(index.row()))

        btn.enterEvent = lambda event: onBtnEnter(btn, event)
        btn.leaveEvent = lambda event: onBtnLeave(btn, event)

        return btn

    @pyqtSlot()
    def onBtnClicked(self, recordIndex):
        raise NotImplementedError("pure virtual method 'onBtnClicked' must be implemented")


class EditButtonDelegate(ButtonDelegate):
    def __init__(self, parentWindow, parent, model):
        ButtonDelegate.__init__(self, parentWindow, parent, model)
        self.iconPath = ":/res/images/edit_word.png"


class PlayButtonDelegate(ButtonDelegate):
    def __init__(self, parentWindow, parent, model):
        ButtonDelegate.__init__(self, parentWindow, parent, model)
        self.iconPath = ":/res/images/media_play.png"


class RemoveButtonDelegate(ButtonDelegate):
    def __init__(self, parentWindow, parent, model):
        ButtonDelegate.__init__(self, parentWindow, parent, model)
        self.iconPath = ":/res/images/delete_word.png"
