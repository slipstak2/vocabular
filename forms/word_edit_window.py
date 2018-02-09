# -*- coding: utf-8 -*-

from PySide import QtGui

from ui.word_edit_ui import Ui_WordAddEdit
from models.word_model import WordModel
from forms_utils import WordEditMode

from models.word_model import PlayButtonWordTranslateDelegate, EditButtonWordTranslateDelegate, RemoveButtonWordTranslateDelegate

from models import models_utils as models_utils

translateTitleMap = {
    WordEditMode.AddNew: u'Добавление слова',
    WordEditMode.Edit: u'Редактирование слова',
    WordEditMode.AddTranslate: u'Добавление перевода',
}

iconTitleMap = {
    WordEditMode.AddNew:         QtGui.QIcon(":/res/images/add_word.png"),
    WordEditMode.Edit:           QtGui.QIcon(":/res/images/edit_word.png"),
    WordEditMode.AddTranslate:   QtGui.QIcon(":/res/images/add_translate.png")
}


class WordEditWindow(QtGui.QDialog):
    def __init__(self, dictId, wordId, wordValue, srcLang, dstLang, mode, *args, **kwargs):
        super(WordEditWindow, self).__init__(*args, **kwargs)

        self.dictId = dictId
        self.mode = mode

        self.wordModel = WordModel(wordId, wordValue, srcLang, dstLang)
        self.srcLang = srcLang
        self.dstLang = dstLang

        self.ui = Ui_WordAddEdit()
        self.ui.setupUi(self)
        self.initUI()
        self.setWindowIcon(iconTitleMap[mode])

    def _onWordChanged(self, word, *args, **kwargs):
        #  TODO: валидация введенных символов
        pass

    def _onTranslateChanged(self, selected, deselected):
        row = self.ui.tvTranslate.currentIndex().row()
        self.ui.actDownOrder.setEnabled(row != self.wordModel.rowCount() - 1)
        self.ui.actUpOrder.setEnabled(row != 0)

    def initUI(self):
        self.initHandlers()
        self.initModels()

    def _onCancel(self, *args, **kwargs):
        self.close()

    def _onOK(self, *args, **kwargs):
        self.accept()

    def _onDownOrder(self, *args, **kwargs):
        currentRow = self.ui.tvTranslate.currentIndex().row()
        self.wordModel.downOrder(currentRow)
        self.ui.tvTranslate.selectRow(currentRow + 1)

    def _onUpOrder(self, *args, **kwargs):
        currentRow = self.ui.tvTranslate.currentIndex().row()
        self.wordModel.upOrder(currentRow)
        self.ui.tvTranslate.selectRow(currentRow - 1)

    def _onAddTranslate(self, *args, **kwargs):
        translateWordId = self.wordModel.addEmptyTranslate()
        assert isinstance(translateWordId, long)

        addTranslateDialog = WordEditWindow(dictId=-1, wordId=translateWordId, wordValue='', srcLang=self.dstLang, dstLang=self.srcLang, mode=WordEditMode.AddTranslate)
        models_utils.setStartGeometry(self, addTranslateDialog)
        addTranslateDialog.exec_()
        if addTranslateDialog.result() != 1:
            self.wordModel.removeTranslate(translateWordId, silent=True)

    def initHandlers(self):
        self.setWindowTitle(translateTitleMap[self.mode])
        self.ui.cbLang.setCurrentIndex(self.srcLang.value)
        self.ui.leWord.textChanged.connect(self._onWordChanged)
        self.ui.leWord.setText(self.wordModel.wordValue)
        self.ui.btnCancel.clicked.connect(self._onCancel)
        self.ui.btnSave.clicked.connect(self._onOK)
        self.ui.actDownOrder.triggered.connect(self._onDownOrder)
        self.ui.actUpOrder.triggered.connect(self._onUpOrder)
        self.ui.actAddTranslate.triggered.connect(self._onAddTranslate)

    def _onTvTranslateDataChanged(self, *args, **kwargs):
        for row in range(0, self.wordModel.rowCount()):
            self.ui.tvTranslate.openPersistentEditor(self.wordModel.index(row, self.wordModel.playFieldNum))
            self.ui.tvTranslate.openPersistentEditor(self.wordModel.index(row, self.wordModel.editFieldNum))
            self.ui.tvTranslate.openPersistentEditor(self.wordModel.index(row, self.wordModel.removeFieldNum))

        self.ui.tvTranslate.resizeColumnsToContents()

    def initModels(self):
        self.ui.tvTranslate.setModel(self.wordModel)
        self.ui.tvTranslate.hideColumn(0)
        self.ui.tvTranslate.hideColumn(2)
        self.ui.tvTranslate.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.ui.tvTranslate.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

        selectionModel = self.ui.tvTranslate.selectionModel()
        selectionModel.selectionChanged.connect(self._onTranslateChanged)

        self.ui.tvTranslate.setItemDelegateForColumn(self.wordModel.playFieldNum, PlayButtonWordTranslateDelegate(self, self.ui.tvTranslate, self.wordModel))
        self.ui.tvTranslate.setItemDelegateForColumn(self.wordModel.editFieldNum, EditButtonWordTranslateDelegate(self, self.ui.tvTranslate, self.wordModel))
        self.ui.tvTranslate.setItemDelegateForColumn(self.wordModel.removeFieldNum, RemoveButtonWordTranslateDelegate(self, self.ui.tvTranslate, self.wordModel))

        self.wordModel.onRefreshCallbacks.append(self._onTvTranslateDataChanged)
        self.wordModel.onRefresh()
