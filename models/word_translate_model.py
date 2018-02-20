# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
from PySide.QtCore import Slot as pyqtSlot
from models.base.base_sql_query_model import SqlQueryModel, SqlQuery, need_refresh
from models.delegates import EditButtonDelegate, PlayButtonDelegate, RemoveButtonDelegate
from utils import Lang
from models.word_model import WordModelProxy, WordModelUtils
from forms.forms_utils import WordEditMode
import models_utils


class WordTranslateModel(SqlQueryModel):
    @need_refresh
    def __init__(self, parentModel, wordId, srcLang, dstLang, *args, **kwargs):
        super(WordTranslateModel, self).__init__(parentModel=parentModel, *args, **kwargs)
        self.wordId = wordId
        self.initLang(srcLang, dstLang)
        self.wordModelUtils = WordModelUtils(self, self.dstLang, self.srcLang) # именно так

        if srcLang == Lang.Eng:
            self.headerFields = [     '', u'перевод',             '',   u'значение',     '',     '',       '']
            self.fields =       ['wr_id', 'wr_value', 're_rus_order',  'wr_meaning', 'play', 'edit', 'remove']
        else:
            self.headerFields = [     '', u'перевод',             '',   u'значение',     '',     '',       '']
            self.fields =       ['we_id', 'we_value', 're_eng_order',  'we_meaning', 'play', 'edit', 'remove']

        self.playFieldNum = self.fields.index('play')
        self.editFieldNum = self.fields.index('edit')
        self.removeFieldNum = self.fields.index('remove')

    def wordTranslate(self, recordIndex):
        return self.record(recordIndex).value(SqlQuery(self, 'w[r]_value').str())

    def wordTranslateId(self, recordIndex):
        return self.record(recordIndex).value(SqlQuery(self, 'w[r]_id').str())

    def wordTranslateOrder(self, recordIndex):
        return self.record(recordIndex).value(SqlQuery(self, 're_[rus]_order').str())

    def refresh(self):
        query = SqlQuery(
            self,
            '''
            SELECT
                word_[rus].id as w[r]_id, word_[rus].value as w[r]_value, rus_eng.[rus]_order as r[e]_[rus]_order, word_[rus].meaning as w[r]_meaning
            FROM
                word_[eng]
            JOIN rus_eng ON rus_eng.word_[eng]_id = word_[eng].id
            JOIN word_[rus] ON word_[rus].id = rus_eng.word_[rus]_id
            WHERE
                word_[eng].id = {word_id}
            ORDER BY
                rus_eng.[rus]_order ASC
            '''.format(word_id=self.wordId)
        ).str()

        self.setQuery(query)

        for idx, field in enumerate(self.headerFields):
            self.setHeaderData(idx, QtCore.Qt.Horizontal, field)

        self.onRefresh()

    def changeOrder(self, row1, row2):
        return SqlQuery(
            self,
            '''
            INSERT INTO
              rus_eng
              (word_[rus]_id, word_[eng]_id, [rus]_order)
            VALUES
              (:w[r]_id1, :w[e]_id1, :[r]o1),(:w[r]_id2, :w[e]_id2, :[r]o2)
            ON DUPLICATE KEY UPDATE [rus]_order=VALUES([rus]_order)
            ''',
            {
                ":w[r]_id1": self.wordTranslateId(row1),
                ":w[r]_id2": self.wordTranslateId(row2),
                ":[r]o1": self.wordTranslateOrder(row2),
                ":[r]o2": self.wordTranslateOrder(row1),
                ":w[e]_id1": self.wordId,
                ":w[e]_id2": self.wordId
            }
        ).execute()

    @need_refresh
    def addEmptyTranslate(self):
        def addEmptyWord():
            return SqlQuery(
                self,
                'INSERT INTO word_[rus] (id) VALUES (NULL)'
            ).execute(True)

        def addTranslateLink(id):
            return SqlQuery(
                self,
                '''
                INSERT INTO
                  rus_eng
                (word_[rus]_id, word_[eng]_id, [rus]_order, [eng]_order)
                VALUES
                  (:w[r]_id, :w[e]_id, :[r]o, :[e]o)
                ''',
                {
                    ':w[r]_id': id,
                    ':w[e]_id': self.wordId,
                    ':[r]o': self.rowCount() + 1,
                    ':[e]o': 1
                }
            ).execute()

        id = addEmptyWord()
        if id:
            if addTranslateLink(id):
                return id
        return False

    @need_refresh
    def removeTranslate(self, translateWordId, silent=False):
        if silent == False:
            msgBox = QtGui.QMessageBox()
            msgBox.setIcon(QtGui.QMessageBox.Question)
            msgBox.setWindowIcon(QtGui.QIcon(":/res/images/dictionary.png"))
            #   TODO: собрать больше информации о переводе. id явно не достаточно. Добавить:
            #       :       1) str value
            #       :       2) количество переводов, в которых он задействован
            #       :       3) количество словарей, в которых он задействован
            msgBox.setText(u"Вы действительно хотите удалить перевод: id = {id}".format(id=translateWordId))
            msgBox.setWindowTitle(u"Удаление перевода")
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            if msgBox.exec_() != QtGui.QMessageBox.Ok:
                return False

        return SqlQuery(
            self,
            '''
            DELETE FROM
              rus_eng
            WHERE
              word_[eng]_id = :word_id AND word_[rus]_id = :translate_id
            ''',
            {
                ':word_id': self.wordId,
                ':translate_id': translateWordId
            }
        ).execute()

    def data(self, index, role):
        value = super(WordTranslateModel, self).data(index, role)
        if role == QtCore.Qt.DisplayRole:
            if index.column() in [self.playFieldNum, self.editFieldNum, self.removeFieldNum]:
                return ''
        return value

    @need_refresh
    def downOrder(self, row):
        self.changeOrder(row, row + 1)

    @need_refresh
    def upOrder(self, row):
        self.changeOrder(row, row - 1)

    def columnCount(self, *args, **kwargs):
        return len(self.fields)


class PlayButtonWordTranslateDelegate(PlayButtonDelegate):
    def __init__(self, parentWindow, parent, model):
        PlayButtonDelegate.__init__(self, parentWindow, parent, model)

    @pyqtSlot()
    def onBtnClicked(self, recordIndex):
        print u"play '{}'".format(self.model.wordTranslate(recordIndex))
        self.commitData.emit(self.sender())


class EditButtonWordTranslateDelegate(EditButtonDelegate):
    def __init__(self, parentWindow, parent, model):
        EditButtonDelegate.__init__(self, parentWindow, parent, model)

    @pyqtSlot()
    def onBtnClicked(self, recordIndex):
        from forms.word_edit_window import WordEditWindow

        wordModelProxy = self.parentWindow.registerModel(
            WordModelProxy(
                self.model,
                self.model.wordTranslateId(recordIndex),
                srcLang=self.model.dstLang,
                dstLang=self.model.srcLang)
        )

        wordEditDialog = WordEditWindow(
            wordModelProxy=wordModelProxy,
            wordModelUtils=self.model.wordModelUtils,
            mode=WordEditMode.EditTranslate,
        )
        models_utils.setStartGeometry(self.parentWindow, wordEditDialog)

        wordEditDialog.exec_()
        #self.model.refresh()
        self.commitData.emit(self.sender())


class RemoveButtonWordTranslateDelegate(RemoveButtonDelegate):
    def __init__(self, parentWindow, parent, model):
        RemoveButtonDelegate.__init__(self, parentWindow, parent, model)

    @pyqtSlot()
    def onBtnClicked(self, recordIndex):
        print u"remove '{}'".format(self.model.wordTranslate(recordIndex))
        self.model.removeTranslate(self.model.wordTranslateId(recordIndex))
        self.commitData.emit(self.sender())
