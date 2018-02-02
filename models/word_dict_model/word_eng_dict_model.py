# -*- coding: utf-8 -*-

from PySide.QtCore import Slot as pyqtSlot

from forms.word_eng_edit_window import WordEngEditWindow
from forms.utils import EditMode, Lang
from models.delegates import EditButtonDelegate, PlayButtonDelegate
from models import utils as models_utils
from models.word_dict_model.word_dict_model import WordDictModel


import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)


class WordEngDictModel(WordDictModel):
    def __init__(self, dictModel, *args, **kwargs):
        super(WordEngDictModel, self).__init__(dictModel, Lang.Eng, *args, **kwargs)
        self.dictModel = dictModel


class PlayButtonWordEngDictDelegate(PlayButtonDelegate):
    def __init__(self, parentWindow, parent, model):
        PlayButtonDelegate.__init__(self, parentWindow, parent, model)

    @pyqtSlot()
    def onBtnClicked(self, recordIndex):
        print u"play '{}'".format(self.model.wordValue(recordIndex))
        self.commitData.emit(self.sender())


class EditButtonWordEngDictDelegate(EditButtonDelegate):
    def __init__(self, parentWindow, parent, model):
        EditButtonDelegate.__init__(self, parentWindow, parent, model)

    @pyqtSlot()
    def onBtnClicked(self, recordIndex):
        print u"edit '{}'".format(self.model.wordValue(recordIndex))
        self.commitData.emit(self.sender())

        #TODO: появление окошек лесенкой, чтобы можно проследить историю глубины
        wordDialog = WordEngEditWindow(
            self.model.dictId(recordIndex),
            self.model.wordId(recordIndex),
            self.model.wordValue(recordIndex),
            Lang.Eng,
            EditMode.Edit
        )
        models_utils.setStartGeometry(self.parentWindow, wordDialog)

        wordDialog.exec_()
        self.model.refresh()
