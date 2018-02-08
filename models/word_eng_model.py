# -*- coding: utf-8 -*-

from PySide import QtSql, QtCore, QtGui
from PySide.QtCore import Slot as pyqtSlot
from models.base.utils import need_refresh
from models.base.base_sql_query_model import BaseSqlQueryModel
from models.delegates import EditButtonDelegate, PlayButtonDelegate, RemoveButtonDelegate
from models.word_model import WordModel
from utils import Lang


class WordEngModel(WordModel):
    def __init__(self, wordId, wordValue):
        super(WordEngModel, self).__init__(wordId, wordValue, Lang.Eng, Lang.Rus)


    @need_refresh
    def removeTranslate(self, translateWordId, silent=False):
        if silent == False:
            msgBox = QtGui.QMessageBox()
            msgBox.setIcon(QtGui.QMessageBox.Question)
            msgBox.setWindowIcon(QtGui.QIcon(":/res/images/dictionary.png"))
            #   TODO: собрать больше информации о переводе. id явно не достаточно. Добавить:
            #   TODO:       1) str value
            #   TODO:       2) количество переводов, в которых он задействован
            #   TODO:       3) количество словарей, в которых он задействован
            msgBox.setText(u"Вы действительно хотите удалить перевод: id = {id}".format(id=translateWordId))
            msgBox.setWindowTitle(u"Удаление перевода")
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            if msgBox.exec_() != QtGui.QMessageBox.Ok:
                return False

        query = QtSql.QSqlQuery()
        query.prepare('DELETE FROM word_rus WHERE id = :id')

        query.bindValue(u":id", translateWordId)
        return self.executeQuery(query)


class PlayButtonWordEngTranslateDelegate(PlayButtonDelegate):
    def __init__(self, parentWindow, parent, model):
        PlayButtonDelegate.__init__(self, parentWindow, parent, model)

    @pyqtSlot()
    def onBtnClicked(self, recordIndex):
        print u"play '{}'".format(self.model.wordTranslate(recordIndex))
        self.commitData.emit(self.sender())


class EditButtonWordEngTranslateDelegate(EditButtonDelegate):
    def __init__(self, parentWindow, parent, model):
        EditButtonDelegate.__init__(self, parentWindow, parent, model)

    @pyqtSlot()
    def onBtnClicked(self, recordIndex):
        print u"edit '{}'".format(self.model.wordTranslate(recordIndex))
        self.commitData.emit(self.sender())


class RemoveButtonWordEngTranslateDelegate(RemoveButtonDelegate):
    def __init__(self, parentWindow, parent, model):
        RemoveButtonDelegate.__init__(self, parentWindow, parent, model)

    @pyqtSlot()
    def onBtnClicked(self, recordIndex):
        print u"remove '{}'".format(self.model.wordTranslate(recordIndex))
        self.model.removeTranslate(self.model.wordTranslateId(recordIndex))
        self.commitData.emit(self.sender())
