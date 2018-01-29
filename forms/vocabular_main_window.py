# -*- coding: utf-8 -*-

# https://gist.github.com/Riateche/5984815
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PySide import QtGui, QtCore
from ui.main_window_ui import Ui_VocabularMainWindow
from dict_edit_window import DictEditWindow, EditMode
from utils import qtRus
from models.dict_model import DictionaryModel
from models.word_eng_dict_model import WordEngDictModel, PlayButtonWordEngDictDelegate, EditButtonWordEngDictDelegate
from utils import onBtnEnter, onBtnLeave
from version import version


#TODO: количество слов в словаре. отображать в имени group box: Слова(42)
#TODO: скрипт для поднятия версии

class VocabularMainWindow(QtGui.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(VocabularMainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_VocabularMainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Vocabular v.{}".format(version))

        self.dictModel = DictionaryModel()
        self.wordEngDictModel = WordEngDictModel(self.dictModel)
        self.dictModel.childModels.append(self.wordEngDictModel)
        self.initUI()

    def _onExit(self, *args, **kwargs):
        self.close()

    def _onAddDict(self, *args, **kwargs):
        dictDialog = DictEditWindow(self.dictModel, EditMode.AddNew)
        dictDialog.exec_()
        if dictDialog.result() == 1:
            self.ui.cbDicts.setCurrentIndex(self.ui.cbDicts.count() - 1)

    def _onEditDict(self, *args, **kwargs):
        dictDialog = DictEditWindow(
            self.dictModel,
            EditMode.Edit,
        )
        currentIndex = self.ui.cbDicts.currentIndex()
        dictDialog.exec_()
        self.ui.cbDicts.setCurrentIndex(currentIndex)

    def _onRemoveDict(self, *args, **kwargs):
        result = QtGui.QMessageBox.question(
            self,
            u"Удаление словаря",
            u'Вы действительно хотите удалить словарь: "{}"'.format(self.dictModel.currentDictName),
            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel,
            QtGui.QMessageBox.Cancel
        )
        if result == QtGui.QMessageBox.Ok:
            self.dictModel.removeDict()

    def _onCbDictCurrentIndexChanged(self, index):
        self.dictModel.currentDictIndex = index

    def _onTvEngWordsDataChanged(self, *args, **kwargs):
        for row in range(0, self.wordEngDictModel.rowCount()):
            self.ui.tvEngWords.openPersistentEditor(self.wordEngDictModel.index(row, WordEngDictModel.playFieldNum))
            self.ui.tvEngWords.openPersistentEditor(self.wordEngDictModel.index(row, WordEngDictModel.editFieldNum))
        self.ui.tvEngWords.resizeColumnsToContents()


    def initUI(self):
        self.initHandlers()
        self.initModels()

    def initHandlers(self):
        def initButtonsMouseHandlers(btn):
            btn.enterEvent = lambda event: onBtnEnter(btn, event)
            btn.leaveEvent = lambda event: onBtnLeave(btn, event)


        self.ui.actExit.triggered.connect(self._onExit)
        self.ui.btnAddDict.clicked.connect(self._onAddDict)
        self.ui.btnEditDict.clicked.connect(self._onEditDict)
        self.ui.btnRemoveDict.clicked.connect(self._onRemoveDict)
        self.ui.cbDicts.currentIndexChanged.connect(self._onCbDictCurrentIndexChanged)

        for btn in [self.ui.btnAddDict, self.ui.btnEditDict, self.ui.btnRemoveDict]:
            initButtonsMouseHandlers(btn)


    def initModels(self):
        self.ui.cbDicts.setModel(self.dictModel)
        self.ui.cbDicts.setModelColumn(self.dictModel.viewFieldIndex())

        self.ui.tvEngWords.setModel(self.wordEngDictModel)
        self.ui.tvEngWords.hideColumn(0)  # TODO: именной индекс
        self.ui.tvEngWords.hideColumn(1)  # TODO: именной индекс
        self.ui.tvEngWords.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.ui.tvEngWords.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

        self.ui.tvEngWords.setItemDelegateForColumn(WordEngDictModel.playFieldNum, PlayButtonWordEngDictDelegate(self, self.ui.tvEngWords, self.wordEngDictModel))
        self.ui.tvEngWords.setItemDelegateForColumn(WordEngDictModel.editFieldNum, EditButtonWordEngDictDelegate(self, self.ui.tvEngWords, self.wordEngDictModel))

        self.wordEngDictModel.onRefreshCallbacks.append(self._onTvEngWordsDataChanged)
        self.wordEngDictModel.onRefresh()
