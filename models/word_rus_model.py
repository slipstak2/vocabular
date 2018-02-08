# -*- coding: utf-8 -*-

from PySide import QtSql, QtCore
from PySide.QtCore import Slot as pyqtSlot
from models.base.utils import need_refresh
from models.base.base_sql_query_model import BaseSqlQueryModel
from models.delegates import EditButtonDelegate, PlayButtonDelegate, RemoveButtonDelegate
from models.word_model import WordModel
from utils import Lang


#TODO: объединить word_eng_model and word_rus_model
class WordRusModel(WordModel):
    def __init__(self, wordId, wordValue):
        super(WordRusModel, self).__init__(wordId, wordValue, Lang.Rus, Lang.Eng)


class PlayButtonWordRusTranslateDelegate(PlayButtonDelegate):
    def __init__(self, parent, model):
        PlayButtonDelegate.__init__(self, parent, model)

    @pyqtSlot()
    def onBtnClicked(self, recordIndex):
        print u"play '{}'".format(self.model.wordTranslate(recordIndex))
        self.commitData.emit(self.sender())


class EditButtonWordRusTranslateDelegate(EditButtonDelegate):
    def __init__(self, parent, model):
        EditButtonDelegate.__init__(self, parent, model)

    @pyqtSlot()
    def onBtnClicked(self, recordIndex):
        print u"edit '{}'".format(self.model.wordTranslate(recordIndex))
        self.commitData.emit(self.sender())


class RemoveButtonRusEngTranslateDelegate(RemoveButtonDelegate):
    def __init__(self, parent, model):
        RemoveButtonDelegate.__init__(self, parent, model)

    @pyqtSlot()
    def onBtnClicked(self, recordIndex):
        print u"remove '{}'".format(self.model.wordTranslate(recordIndex))
        self.commitData.emit(self.sender())
