# -*- coding: utf-8 -*-

from PySide import QtGui

from ui.dict_edit_ui import Ui_DictAddEdit
from forms_utils import DictEditMode


translateTitleMap = {
    DictEditMode.Add: u"Добавление словаря",
    DictEditMode.Edit: u"Редактирование словаря"
}

iconTitleMap = {
    DictEditMode.Add: QtGui.QIcon(":/res/images/add_dict.png"),
    DictEditMode.Edit:   QtGui.QIcon(":/res/images/edit_dict.png")
}


class DictEditWindow(QtGui.QDialog):
    def __init__(self, dictModel, mode, *args, **kwargs):
        super(DictEditWindow, self).__init__(*args, **kwargs)
        self.dictModel = dictModel
        self.mode = mode

        self.ui = Ui_DictAddEdit()
        self.ui.setupUi(self)
        self.initUI()

        self.setWindowIcon(iconTitleMap[mode])

    def _onCancel(self, *args, **kwargs):
        self.close()

    def _onSave(self, *args, **kwargs):
        dictName = self.ui.leDictName.text()
        if self.mode == DictEditMode.Add:
            if self.dictModel.addDict(dictName):
                self.accept()
            else:
                QtGui.QMessageBox.critical(None, u"Ошибка", u"Во время создания словаря {} произошла ошибка".format(dictName))
        elif self.mode == DictEditMode.Edit:
            if self.dictModel.editDict(self.dictModel.currentDictId, dictName):
                self.accept()
            else:
                QtGui.QMessageBox.critical(None, u"Ошибка", u"Во время редактирования словаря {} произошла ошибка".format(dictName))

    def initUI(self):
        self.setWindowTitle(translateTitleMap[self.mode])
        if self.mode == DictEditMode.Edit:
            self.ui.leDictName.setText(self.dictModel.currentDictName)

        self.ui.btnCancel.clicked.connect(self._onCancel)
        self.ui.btnSave.clicked.connect(self._onSave)
