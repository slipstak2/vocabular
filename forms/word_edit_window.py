# -*- coding: utf-8 -*-

from PySide import QtGui
from PySide.QtGui import QDataWidgetMapper, QRegExpValidator
from PySide.QtCore import QRegExp

import utils
from forms.base_dialog import BaseDialog
from forms_utils import WordEditMode
from models.word_model import WordModel, WordModelInfo, WordModelUtils
from models.word_translate_model import WordTranslateModel
from ui.word_edit_ui import Ui_WordAddEdit

from models.word_translate_model import PlayButtonWordTranslateDelegate, EditButtonWordTranslateDelegate, RemoveButtonWordTranslateDelegate

from models import models_utils as models_utils

translateTitleMap = {
    WordEditMode.AddWord: u'Добавление слова',
    WordEditMode.EditWord: u'Редактирование слова',
    WordEditMode.AddTranslate: u'Добавление перевода',
    WordEditMode.EditTranslate: u'Редактирование перевода'
}

iconTitleMap = {
    WordEditMode.AddWord:         QtGui.QIcon(":/res/images/add_word.png"),
    WordEditMode.EditWord:           QtGui.QIcon(":/res/images/edit_word.png"),
    WordEditMode.AddTranslate:   QtGui.QIcon(":/res/images/add_translate.png"),
    WordEditMode.EditTranslate:  QtGui.QIcon(":/res/images/edit_word.png"),
}


class WordEditContext(object):
    def __init__(self):
        self.wordIds = []

    def addWordId(self, wordId, srcLang):
        item = (wordId, srcLang)
        self.wordIds.append(item)

    def removeWordId(self, wordId, srcLang):
        item = (wordId, srcLang)
        assert item == self.wordIds[-1]
        self.wordIds.pop()

    def inContext(self, wordId, srcLang):
        item = (wordId, srcLang)
        return item in self.wordIds

class WordEditWindow(BaseDialog):
    def __init__(self, wordModelInfo, mode, wordEditContext, *args, **kwargs):
        super(WordEditWindow, self).__init__(*args, **kwargs)

        self.wordModelInfo = wordModelInfo
        self.wordModelUtils = wordModelInfo.utils
        self.mode = mode

        self.wordEditContext = wordEditContext
        self.wordEditContext.addWordId(self.wordModelInfo.wordId, self.wordModelInfo.srcLang)

        self.wordModel = WordModel(
            self.wordModelInfo.wordId,
            wordModelInfo.srcLang,
            wordModelInfo.dstLang
        )

        self.wordTranslateModel = WordTranslateModel(
            self.wordModelInfo.wordId,
            wordModelInfo.srcLang,
            wordModelInfo.dstLang
        )

        self.ui = Ui_WordAddEdit()
        self.ui.setupUi(self)
        self.initUI()
        self.setWindowIcon(iconTitleMap[mode])
        self.mapWordModelFields()

    def onCloseDialog(self):
        self.wordEditContext.removeWordId(
            self.wordModelInfo.wordId,
            self.wordModelInfo.srcLang
        )

    def mapWordModelFields(self):
        mapper = QDataWidgetMapper()
        mapper.setModel(self.wordModel)
        mapper.addMapping(self.ui.leWord, self.wordModel.valueFieldNum)
        mapper.addMapping(self.ui.teMeaning, self.wordModel.meaningFieldNum)
        mapper.toFirst()

    def _onTranslateChanged(self, selected, deselected):
        row = self.ui.tvTranslate.currentIndex().row()
        self.ui.actDownOrder.setEnabled(row != self.wordTranslateModel.rowCount() - 1)
        self.ui.actUpOrder.setEnabled(row != 0)

    def initUI(self):
        self.initHandlers()
        self.initModels()

    def _onCancel(self, *args, **kwargs):
        self.close()

    def _onOK(self, *args, **kwargs):
        word = self.ui.leWord.text()
        meaning = self.ui.teMeaning.toPlainText()
        self.wordModelUtils.edit(self.wordModelInfo.wordId, word, meaning)

        self.accept()

    def _onDownOrder(self, *args, **kwargs):
        currentRow = self.ui.tvTranslate.currentIndex().row()
        self.wordTranslateModel.downOrder(currentRow)
        self.ui.tvTranslate.selectRow(currentRow + 1)

    def _onUpOrder(self, *args, **kwargs):
        currentRow = self.ui.tvTranslate.currentIndex().row()
        self.wordTranslateModel.upOrder(currentRow)
        self.ui.tvTranslate.selectRow(currentRow - 1)

    def _onAddTranslate(self, *args, **kwargs):
        translateWordId = self.wordTranslateModel.addEmptyTranslate()
        assert isinstance(translateWordId, long)

        wordModelInfo = WordModelInfo(translateWordId, srcLang=self.wordModelInfo.dstLang, dstLang=self.wordModelInfo.srcLang)
        addTranslateDialog = WordEditWindow(
            wordModelInfo=wordModelInfo,
            mode=WordEditMode.AddTranslate,
            wordEditContext=self.wordEditContext
        )
        models_utils.setStartGeometry(self, addTranslateDialog)
        addTranslateDialog.exec_()
        if addTranslateDialog.result() != 1:
            self.wordTranslateModel.removeTranslate(translateWordId, silent=True)
        self.wordTranslateModel.refresh()

    def initHandlers(self):
        self.setWindowTitle(translateTitleMap[self.mode])
        self.ui.cbLang.setCurrentIndex(self.wordModelInfo.srcLang.value)
        if self.wordModel.srcLang == utils.Lang.Eng:
            self.ui.leWord.setValidator(QRegExpValidator(QRegExp(utils.rxEng), self))
        if self.wordModel.srcLang == utils.Lang.Rus:
            self.ui.leWord.setValidator(QRegExpValidator(QRegExp(utils.rxRus), self))

        self.ui.leWord.setText(self.wordModel.wordValue)
        self.ui.teMeaning.setText(self.wordModel.wordMeaning)

        self.ui.btnCancel.clicked.connect(self._onCancel)
        self.ui.btnSave.clicked.connect(self._onOK)
        self.ui.actDownOrder.triggered.connect(self._onDownOrder)
        self.ui.actUpOrder.triggered.connect(self._onUpOrder)
        self.ui.actAddTranslate.triggered.connect(self._onAddTranslate)

    def _onTvTranslateDataChanged(self, *args, **kwargs):
        for row in range(0, self.wordTranslateModel.rowCount()):
            self.ui.tvTranslate.openPersistentEditor(self.wordTranslateModel.index(row, self.wordTranslateModel.playFieldNum))
            if not self.wordEditContext.inContext(
                    self.wordTranslateModel.wordTranslateId(row),
                    self.wordModel.dstLang
            ):
                self.ui.tvTranslate.openPersistentEditor(self.wordTranslateModel.index(row, self.wordTranslateModel.editFieldNum))
                self.ui.tvTranslate.openPersistentEditor(self.wordTranslateModel.index(row, self.wordTranslateModel.removeFieldNum))

        self.ui.tvTranslate.resizeColumnsToContents()

    def initModels(self):
        self.ui.tvTranslate.setModel(self.wordTranslateModel)
        self.ui.tvTranslate.hideColumn(0)
        self.ui.tvTranslate.hideColumn(2)
        self.ui.tvTranslate.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.ui.tvTranslate.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

        selectionModel = self.ui.tvTranslate.selectionModel()
        selectionModel.selectionChanged.connect(self._onTranslateChanged)

        self.ui.tvTranslate.setItemDelegateForColumn(self.wordTranslateModel.playFieldNum, PlayButtonWordTranslateDelegate(self, self.ui.tvTranslate, self.wordTranslateModel))
        self.ui.tvTranslate.setItemDelegateForColumn(self.wordTranslateModel.editFieldNum, EditButtonWordTranslateDelegate(self, self.ui.tvTranslate, self.wordTranslateModel))
        self.ui.tvTranslate.setItemDelegateForColumn(self.wordTranslateModel.removeFieldNum, RemoveButtonWordTranslateDelegate(self, self.ui.tvTranslate, self.wordTranslateModel))

        self.wordTranslateModel.onRefreshCallbacks.append(self._onTvTranslateDataChanged)
        self.wordTranslateModel.onRefresh()
