# -*- coding: utf-8 -*-

from PySide import QtGui

from ui.dict_edit_ui import Ui_DictAddEdit
from forms_utils import EditMode


translateTitleMap = {
    EditMode.AddNew: u"Добавление словаря",
    EditMode.Edit: u"Редактирование словаря"
}

iconTitleMap = {
    EditMode.AddNew: QtGui.QIcon(":/res/images/add_dict.png"),
    EditMode.Edit:   QtGui.QIcon(":/res/images/edit_dict.png")
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
        if self.mode == EditMode.AddNew:
            if self.dictModel.addDict(dictName):
                self.accept()
            else:
                QtGui.QMessageBox.critical(None, u"Ошибка", u"Во время создания словаря {} произошла ошибка".format(dictName))
        elif self.mode == EditMode.Edit:
            if self.dictModel.editDict(self.dictModel.currentDictId, dictName):
                self.accept()
            else:
                QtGui.QMessageBox.critical(None, u"Ошибка", u"Во время редактирования словаря {} произошла ошибка".format(dictName))

    def initUI(self):
        self.setWindowTitle(translateTitleMap[self.mode])
        if self.mode == EditMode.Edit:
            self.ui.leDictName.setText(self.dictModel.currentDictName)

        self.ui.btnCancel.clicked.connect(self._onCancel)
        self.ui.btnSave.clicked.connect(self._onSave)
