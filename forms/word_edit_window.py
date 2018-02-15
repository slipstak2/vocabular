# -*- coding: utf-8 -*-

from PySide import QtGui
from PySide.QtGui import QDataWidgetMapper

from forms.base_dialog import BaseDialog
from ui.word_edit_ui import Ui_WordAddEdit
from models.word_model import WordModel
from models.word_translate_model import WordTranslateModel
from forms_utils import WordEditMode

from models.word_translate_model import PlayButtonWordTranslateDelegate, EditButtonWordTranslateDelegate, RemoveButtonWordTranslateDelegate

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


class WordEditWindow(BaseDialog):
    def __init__(self, dictId, wordId, srcLang, dstLang, mode, wordListDictModel=None, *args, **kwargs):
        super(WordEditWindow, self).__init__(*args, **kwargs)
        self.srcLang = srcLang
        self.dstLang = dstLang

        #TODO: зачем dictId? Вроде не нужен
        self.dictId = dictId
        self.mode = mode
        self.wordId = wordId

        self.wordListDictModel = wordListDictModel
        self.wordModel = self.registerModel(WordModel(wordListDictModel, wordId, srcLang, dstLang))
        self.wordTranslateModel = self.registerModel(WordTranslateModel(wordListDictModel, wordId, srcLang, dstLang))

        self.ui = Ui_WordAddEdit()
        self.ui.setupUi(self)
        self.initUI()
        self.setWindowIcon(iconTitleMap[mode])
        self.mapWordModelFields()

    def mapWordModelFields(self):
        mapper = QDataWidgetMapper()
        mapper.setModel(self.wordModel)
        mapper.addMapping(self.ui.leWord, self.wordModel.valueFieldNum)
        mapper.addMapping(self.ui.teMeaning, self.wordModel.meaningFieldNum)
        mapper.toFirst()

    def _onWordChanged(self, word, *args, **kwargs):
        #  TODO: валидация введенных символов
        pass

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
        if self.mode in [WordEditMode.AddNew, WordEditMode.Edit]:
            word = self.ui.leWord.text()
            meaning = self.ui.teMeaning.toPlainText()
            self.wordModel.update(word, meaning)

        if self.mode == WordEditMode.AddNew:
            self.wordListDictModel.addWord(self.wordId)
        if self.mode == WordEditMode.AddTranslate:
            print 'add translate'

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

        addTranslateDialog = WordEditWindow(
            dictId=-1,
            wordId=translateWordId,
            srcLang=self.dstLang,
            dstLang=self.srcLang,
            mode=WordEditMode.AddTranslate,
            wordListDictModel=self.wordListDictModel #TODO: раньше не было
        )
        models_utils.setStartGeometry(self, addTranslateDialog)
        addTranslateDialog.exec_()
        if addTranslateDialog.result() != 1:
            self.wordTranslateModel.removeTranslate(translateWordId, silent=True)

    def initHandlers(self):
        self.setWindowTitle(translateTitleMap[self.mode])
        self.ui.cbLang.setCurrentIndex(self.srcLang.value)
        self.ui.leWord.textChanged.connect(self._onWordChanged)

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
