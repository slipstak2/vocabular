# -*- coding: utf-8 -*-

from PySide import QtGui

from ui.word_edit_ui import Ui_WordAddEdit
from models.word_eng_model import WordEngModel
from utils import qtRus, EditMode, Lang
from models.word_eng_model import EditButtonWordEngTranslateDelegate, \
    PlayButtonWordEngTranslateDelegate, \
    RemoveButtonWordEngTranslateDelegate

from forms.word_rus_edit_window import WordRusEditWindow
from models import utils as models_utils

translateTitleMap = {
    EditMode.AddNew: "Добавление слова",
    EditMode.Edit: "Редактирование слова"
}

iconTitleMap = {
    EditMode.AddNew:         QtGui.QIcon(":/res/images/add_word.png"),
    EditMode.Edit:           QtGui.QIcon(":/res/images/edit_word.png"),
    EditMode.AddTranslate:   QtGui.QIcon(":/res/images/add_translate.png")
}


#TODO: иконки на окне: откуда был совершен переход: Добавление слова, Редактирование слова, Добавление перевода

class WordEngEditWindow(QtGui.QDialog):
    def __init__(self, dictId, wordId, wordValue, lang, mode, *args, **kwargs):
        super(WordEngEditWindow, self).__init__(*args, **kwargs)

        self.dictId = dictId
        self.mode = mode

        self.wordEngModel = WordEngModel(wordId, wordValue)
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
        self.ui.actDownOrder.setEnabled(row != self.wordEngModel.rowCount() - 1)
        self.ui.actUpOrder.setEnabled(row != 0)

    def initUI(self):
        self.initHandlers()
        self.initModels()

    def _onCancel(self, *args, **kwargs):
        self.close()

    def _onAddTranslate(self, *args, **kwargs):
        rusWordId = self.wordEngModel.addEmptyTranslate()
        if rusWordId: # TODO:нужны ли такие проверки? или падать сразу внутри метода?
            addTranslateDialog = WordRusEditWindow(dictId=-1, wordRusId=rusWordId, wordRusValue='', lang=Lang.Rus, mode=EditMode.AddTranslate)
            models_utils.setStartGeometry(self, addTranslateDialog)
            addTranslateDialog.exec_()
            if addTranslateDialog.result() != 1:
                self.wordEngModel.removeTranslate(rusWordId, silent=True)

    def _onDownOrder(self, *args, **kwargs):
        currentRow = self.ui.tvTranslate.currentIndex().row()
        self.wordEngModel.downOrder(currentRow)
        self.ui.tvTranslate.selectRow(currentRow + 1)

    def _onUpOrder(self, *args, **kwargs):
        currentRow = self.ui.tvTranslate.currentIndex().row()
        self.wordEngModel.upOrder(currentRow)
        self.ui.tvTranslate.selectRow(currentRow - 1)

    def initHandlers(self):
        self.setWindowTitle(qtRus(translateTitleMap[self.mode]))
        self.ui.cbLang.setCurrentIndex(self.lang.value)
        self.ui.leWord.textChanged.connect(self._onWordChanged)
        self.ui.leWord.setText(self.wordEngModel.wordValue)
        self.ui.btnCancel.clicked.connect(self._onCancel)
        self.ui.actDownOrder.triggered.connect(self._onDownOrder)
        self.ui.actUpOrder.triggered.connect(self._onUpOrder)

        self.ui.actAddTranslate.triggered.connect(self._onAddTranslate)

    def _onTvTranslateDataChanged(self, *args, **kwargs):
        for row in range(0, self.wordEngModel.rowCount()):
            self.ui.tvTranslate.openPersistentEditor(self.wordEngModel.index(row, WordEngModel.playFieldNum))
            self.ui.tvTranslate.openPersistentEditor(self.wordEngModel.index(row, WordEngModel.editFieldNum))
            self.ui.tvTranslate.openPersistentEditor(self.wordEngModel.index(row, WordEngModel.removeFieldNum))

        self.ui.tvTranslate.resizeColumnsToContents()


    def initModels(self):
        self.ui.tvTranslate.setModel(self.wordEngModel)
        self.ui.tvTranslate.hideColumn(0)  # TODO: именной индекс
        self.ui.tvTranslate.hideColumn(2)  # TODO: именной индекс
        self.ui.tvTranslate.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.ui.tvTranslate.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

        selectionModel = self.ui.tvTranslate.selectionModel()
        selectionModel.selectionChanged.connect(self._onTranslateChanged)

        self.ui.tvTranslate.setItemDelegateForColumn(WordEngModel.playFieldNum, PlayButtonWordEngTranslateDelegate(self, self.ui.tvTranslate, self.wordEngModel))
        self.ui.tvTranslate.setItemDelegateForColumn(WordEngModel.editFieldNum, EditButtonWordEngTranslateDelegate(self, self.ui.tvTranslate, self.wordEngModel))
        self.ui.tvTranslate.setItemDelegateForColumn(WordEngModel.removeFieldNum, RemoveButtonWordEngTranslateDelegate(self, self.ui.tvTranslate, self.wordEngModel))

        self.wordEngModel.onRefreshCallbacks.append(self._onTvTranslateDataChanged)
        self.wordEngModel.onRefresh()
