# -*- coding: utf-8 -*-

from PySide import QtGui

from ui.word_edit_ui import Ui_WordAddEdit
from models.word_model import WordModel
from forms_utils import EditMode
from models.word_model import PlayButtonWordTranslateDelegate, EditButtonWordTranslateDelegate, RemoveButtonWordTranslateDelegate
from utils import Lang
from forms.word_edit_window import WordEditWindow

translateTitleMap = {
    EditMode.AddNew: u'Добавление слова',
    EditMode.Edit: u'Редактирование слова',
    EditMode.AddTranslate: u'Добавление перевода',
}

iconTitleMap = {
    EditMode.AddNew:         QtGui.QIcon(":/res/images/add_word.png"),
    EditMode.Edit:           QtGui.QIcon(":/res/images/edit_word.png"),
    EditMode.AddTranslate:   QtGui.QIcon(":/res/images/add_translate.png")
}

#TODO: Объединить word_eng_edit_window and word_rus_edit_window
class WordRusEditWindow(WordEditWindow):

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

    def initHandlers(self):
        self.setWindowTitle(translateTitleMap[self.mode])
        self.ui.cbLang.setCurrentIndex(self.srcLang.value)
        self.ui.leWord.textChanged.connect(self._onWordChanged)
        self.ui.leWord.setText(self.wordModel.wordValue)
        self.ui.btnCancel.clicked.connect(self._onCancel)
        self.ui.btnSave.clicked.connect(self._onOK)
        self.ui.actDownOrder.triggered.connect(self._onDownOrder)
        self.ui.actUpOrder.triggered.connect(self._onUpOrder)

        #self.ui.tabWidget.removeTab(0)

    def _onTvTranslateDataChanged(self, *args, **kwargs):
        for row in range(0, self.wordModel.rowCount()):
            self.ui.tvTranslate.openPersistentEditor(self.wordModel.index(row, self.wordModel.playFieldNum))
            self.ui.tvTranslate.openPersistentEditor(self.wordModel.index(row, self.wordModel.editFieldNum))
            self.ui.tvTranslate.openPersistentEditor(self.wordModel.index(row, self.wordModel.removeFieldNum))

        self.ui.tvTranslate.resizeColumnsToContents()


    def initModels(self):
        self.ui.tvTranslate.setModel(self.wordModel)
        self.ui.tvTranslate.hideColumn(0)  # TODO: именной индекс
        self.ui.tvTranslate.hideColumn(2)  # TODO: именной индекс
        self.ui.tvTranslate.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.ui.tvTranslate.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

        selectionModel = self.ui.tvTranslate.selectionModel()
        selectionModel.selectionChanged.connect(self._onTranslateChanged)

        self.ui.tvTranslate.setItemDelegateForColumn(self.wordModel.playFieldNum, PlayButtonWordTranslateDelegate(self, self.ui.tvTranslate, self.wordModel))
        self.ui.tvTranslate.setItemDelegateForColumn(self.wordModel.editFieldNum, EditButtonWordTranslateDelegate(self, self.ui.tvTranslate, self.wordModel))
        self.ui.tvTranslate.setItemDelegateForColumn(self.wordModel.removeFieldNum, RemoveButtonWordTranslateDelegate(self, self.ui.tvTranslate, self.wordModel))

        self.wordModel.onRefreshCallbacks.append(self._onTvTranslateDataChanged)
        self.wordModel.onRefresh()
