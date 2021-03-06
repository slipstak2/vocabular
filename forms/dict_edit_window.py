# -*- coding: utf-8 -*-

from PySide import QtGui
from PySide.QtGui import QDataWidgetMapper

from forms.base_dialog import BaseDialog
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


class DictEditWindow(BaseDialog):
    def __init__(self, dictModel, mode, *args, **kwargs):
        super(DictEditWindow, self).__init__(*args, **kwargs)
        self.dictModel = dictModel
        self.mode = mode

        self.ui = Ui_DictAddEdit()
        self.ui.setupUi(self)
        self.initUI()

        self.setWindowIcon(iconTitleMap[mode])
        self.mapDictModelFields()

    def mapDictModelFields(self):
        mapper = QDataWidgetMapper()
        mapper.setModel(self.dictModel)
        mapper.addMapping(self.ui.leDictName, self.dictModel.nameFieldName)
        mapper.toFirst()

    def _onCancel(self, *args, **kwargs):
        self.close()

    def _onSave(self, *args, **kwargs):
        self.dictModel.utils.edit(
            self.dictModel.dictId,
            self.ui.leDictName.text()
        )
        self.accept()

    def initUI(self):
        self.setWindowTitle(translateTitleMap[self.mode])

        self.ui.btnCancel.clicked.connect(self._onCancel)
        self.ui.btnSave.clicked.connect(self._onSave)
