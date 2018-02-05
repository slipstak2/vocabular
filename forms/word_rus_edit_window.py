# -*- coding: utf-8 -*-

from PySide import QtGui

from ui.word_edit_ui import Ui_WordAddEdit
from models.word_rus_model import WordRusModel
from forms_utils import qtRus, EditMode
from models.word_eng_model import EditButtonWordEngTranslateDelegate, \
    PlayButtonWordEngTranslateDelegate, \
    RemoveButtonWordEngTranslateDelegate
#from utils import Lang

translateTitleMap = {
    EditMode.AddNew: "Добавление слова",
    EditMode.Edit: "Редактирование слова",
    EditMode.AddTranslate: "Добавление перевода",
}

iconTitleMap = {
    EditMode.AddNew:         QtGui.QIcon(":/res/images/add_word.png"),
    EditMode.Edit:           QtGui.QIcon(":/res/images/edit_word.png"),
    EditMode.AddTranslate:   QtGui.QIcon(":/res/images/add_translate.png")
}

#TODO: Объединить word_eng_edit_window and word_rus_edit_window
class WordRusEditWindow(QtGui.QDialog):
    def __init__(self, dictId, wordRusId, wordRusValue, lang, mode, *args, **kwargs):
        super(WordRusEditWindow, self).__init__(*args, **kwargs)

        self.dictId = dictId
        self.mode = mode

        self.wordRusModel = WordRusModel(wordRusId, wordRusValue)
        self.lang = lang

        self.ui = Ui_WordAddEdit()
        self.ui.setupUi(self)
        self.initUI()
        self.setWindowIcon(iconTitleMap[mode])

    def _onWordChanged(self, word, *args, **kwargs):
        #  TODO: валидация введенных символов
        pass

    def _onTranslateChanged(self, selected, deselected):
        row = self.ui.tvTranslate.currentIndex().row()
        self.ui.actDownOrder.setEnabled(row != self.wordRusModel.rowCount() - 1)
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
        self.wordRusModel.downOrder(currentRow)
        self.ui.tvTranslate.selectRow(currentRow + 1)

    def _onUpOrder(self, *args, **kwargs):
        currentRow = self.ui.tvTranslate.currentIndex().row()
        self.wordRusModel.upOrder(currentRow)
        self.ui.tvTranslate.selectRow(currentRow - 1)

    def initHandlers(self):
        self.setWindowTitle(qtRus(translateTitleMap[self.mode]))
        self.ui.cbLang.setCurrentIndex(self.lang.value)
        self.ui.leWord.textChanged.connect(self._onWordChanged)
        self.ui.leWord.setText(self.wordRusModel.wordRusValue)
        self.ui.btnCancel.clicked.connect(self._onCancel)
        self.ui.btnSave.clicked.connect(self._onOK)
        self.ui.actDownOrder.triggered.connect(self._onDownOrder)
        self.ui.actUpOrder.triggered.connect(self._onUpOrder)

        #self.ui.tabWidget.removeTab(0)

    def _onTvTranslateDataChanged(self, *args, **kwargs):
        for row in range(0, self.wordRusModel.rowCount()):
            self.ui.tvTranslate.openPersistentEditor(self.wordRusModel.index(row, WordRusModel.playFieldNum))
            self.ui.tvTranslate.openPersistentEditor(self.wordRusModel.index(row, WordRusModel.editFieldNum))
            self.ui.tvTranslate.openPersistentEditor(self.wordRusModel.index(row, WordRusModel.removeFieldNum))

        self.ui.tvTranslate.resizeColumnsToContents()


    def initModels(self):
        self.ui.tvTranslate.setModel(self.wordRusModel)
        self.ui.tvTranslate.hideColumn(0)  # TODO: именной индекс
        self.ui.tvTranslate.hideColumn(2)  # TODO: именной индекс
        self.ui.tvTranslate.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.ui.tvTranslate.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

        selectionModel = self.ui.tvTranslate.selectionModel()
        selectionModel.selectionChanged.connect(self._onTranslateChanged)

        self.ui.tvTranslate.setItemDelegateForColumn(WordRusModel.playFieldNum, PlayButtonWordEngTranslateDelegate(self, self.ui.tvTranslate, self.wordRusModel))
        self.ui.tvTranslate.setItemDelegateForColumn(WordRusModel.editFieldNum, EditButtonWordEngTranslateDelegate(self, self.ui.tvTranslate, self.wordRusModel))
        self.ui.tvTranslate.setItemDelegateForColumn(WordRusModel.removeFieldNum, RemoveButtonWordEngTranslateDelegate(self, self.ui.tvTranslate, self.wordRusModel))

        self.wordRusModel.onRefreshCallbacks.append(self._onTvTranslateDataChanged)
        self.wordRusModel.onRefresh()
