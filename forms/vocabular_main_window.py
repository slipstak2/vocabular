# -*- coding: utf-8 -*-

# https://gist.github.com/Riateche/5984815
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PySide import QtGui
from ui.main_window_ui import Ui_VocabularMainWindow
from dict_edit_window import DictEditWindow, DictEditMode
from models.dict_list_model import DictListModel
from models.dict_model import DictModel
from models.word_list_dict_model import WordListDictModel
from models.word_list_dict_model import PlayButtonWordListDictDelegate, EditButtonWordListDictDelegate, RemoveButtonWordListDictDelegate
from models.word_model import WordModelProxy
from forms_utils import onBtnEnter, onBtnLeave, WordEditMode
from utils import Lang
from version import version
from forms.word_edit_window import WordEditWindow
from models import models_utils


#TODO: добавить удаление слова из словаря
class VocabularMainWindow(QtGui.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(VocabularMainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_VocabularMainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Vocabular v.{}".format(version))
        self.models = []

        self.srcLang = Lang.Eng
        self.dstLang = Lang.Rus
        self.dictListModel = self.registerModel(DictListModel())
        self.wordListDictModel = self.registerModel(WordListDictModel(self.dictListModel.dictModelProxy, self.srcLang, self.dstLang))
        self.initUI()

    def _onAddWord(self):

        wordId = self.wordListDictModel.wordModelUtils.add('', '')
        wordProxyModel = WordModelProxy(self.wordListDictModel, wordId, self.srcLang, self.dstLang) #TODO: register model
        addWordDialog = WordEditWindow(
            wordModelProxy=wordProxyModel,
            mode=WordEditMode.AddNew
        )
        models_utils.setStartGeometry(self, addWordDialog)
        addWordDialog.exec_()
        if addWordDialog.result() != 1:
            self.wordListDictModel.removeLinkWord(wordId, silent=True, removeWord=True)

    def _onExit(self, *args, **kwargs):
        self.close()

    def _onAddDict(self, *args, **kwargs):
        dictId = self.dictListModel.addDict('')
        dictModel = DictModel(self.dictListModel, dictId)
        dictDialog = DictEditWindow(dictModel, self.dictListModel.dictModelUtils, DictEditMode.Add)
        dictDialog.exec_()
        if dictDialog.result() == 1:
            self.ui.cbDicts.setCurrentIndex(self.dictListModel.rowCount() - 1)
        else:
            self.dictListModel.removeDict(dictId)


    def _onEditDict(self, *args, **kwargs):
        dictModel = DictModel(self.dictListModel, self.dictListModel.currentDictId)
        dictDialog = DictEditWindow(
            dictModel,
            self.dictListModel.dictModelUtils,
            DictEditMode.Edit,
        )
        currentIndex = self.ui.cbDicts.currentIndex()
        dictDialog.exec_()
        self.ui.cbDicts.setCurrentIndex(currentIndex)

    def _onRemoveDict(self, *args, **kwargs):
        result = QtGui.QMessageBox.question(
            self,
            u"Удаление словаря",
            u'Вы действительно хотите удалить словарь: "{}"'.format(self.dictListModel.currentDictName),
            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel,
            QtGui.QMessageBox.Cancel
        )
        if result == QtGui.QMessageBox.Ok:
            self.dictListModel.removeDict()

    def _onCbDictCurrentIndexChanged(self, index):
        self.dictListModel.currentDictIndex = index
        self.ui.gbWords.setTitle(u'Слова ({})'.format(self.wordListDictModel.rowCount()))

    def _onTvEngWordsDataChanged(self, *args, **kwargs):
        for row in range(0, self.wordListDictModel.rowCount()):
            for col in [self.wordListDictModel.playFieldNum, self.wordListDictModel.editFieldNum, self.wordListDictModel.removeFieldNum]:
                self.ui.tvEngWords.openPersistentEditor(self.wordListDictModel.index(row, col))
        self.ui.tvEngWords.resizeColumnsToContents()

    def initUI(self):
        self.initHandlers()
        self.initModels()

    def initHandlers(self):
        def initButtonsMouseHandlers(btn):
            btn.enterEvent = lambda event: onBtnEnter(btn, event)
            btn.leaveEvent = lambda event: onBtnLeave(btn, event)

        self.ui.actAddWord.triggered.connect(self._onAddWord)
        self.ui.actExit.triggered.connect(self._onExit)

        self.ui.btnAddDict.clicked.connect(self._onAddDict)
        self.ui.btnEditDict.clicked.connect(self._onEditDict)
        self.ui.btnRemoveDict.clicked.connect(self._onRemoveDict)
        self.ui.cbDicts.currentIndexChanged.connect(self._onCbDictCurrentIndexChanged)

        for btn in [self.ui.btnAddDict, self.ui.btnEditDict, self.ui.btnRemoveDict]:
            initButtonsMouseHandlers(btn)

    def initModels(self):
        self.ui.cbDicts.setModel(self.dictListModel)
        self.ui.cbDicts.setModelColumn(self.dictListModel.viewFieldIndex())

        self.ui.tvEngWords.setModel(self.wordListDictModel)
        self.ui.tvEngWords.hideColumn(0)
        self.ui.tvEngWords.hideColumn(1)
        self.ui.tvEngWords.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.ui.tvEngWords.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

        self.ui.tvEngWords.setItemDelegateForColumn(self.wordListDictModel.playFieldNum, PlayButtonWordListDictDelegate(self, self.ui.tvEngWords, self.wordListDictModel))
        self.ui.tvEngWords.setItemDelegateForColumn(self.wordListDictModel.editFieldNum, EditButtonWordListDictDelegate(self, self.ui.tvEngWords, self.wordListDictModel))
        self.ui.tvEngWords.setItemDelegateForColumn(self.wordListDictModel.removeFieldNum, RemoveButtonWordListDictDelegate(self, self.ui.tvEngWords, self.wordListDictModel))

        self.wordListDictModel.onRefreshCallbacks.append(self._onTvEngWordsDataChanged)
        self.wordListDictModel.onRefresh()

    def closeEvent(self, *args, **kwargs):
        self.releaseModels()

    def registerModel(self, model):
        self.models.append(model)
        return model

    def releaseModels(self):
        for model in reversed(self.models):
            model.release()
