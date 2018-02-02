# -*- coding: utf-8 -*-

from PySide import QtSql, QtCore, QtGui
from PySide.QtCore import Slot as pyqtSlot
from models.base.utils import need_refresh
from models.base.base_sql_query_model import BaseSqlQueryModel
from models.delegates import EditButtonDelegate, PlayButtonDelegate, RemoveButtonDelegate


class WordEngModel(BaseSqlQueryModel):
    headerFields = [     '', u'перевод',             '',   u'значение',     '',     '',       '']
    fields =       ['wr_id', 'wr_value', 're_rus_order',  'wr_meaning', 'play', 'edit', 'remove']
    playFieldNum = fields.index('play')
    editFieldNum = fields.index('edit')
    removeFieldNum = fields.index('remove')

    @need_refresh
    def __init__(self, wordId, wordValue, *args, **kwargs):
        super(WordEngModel, self).__init__(*args, **kwargs)
        self.wordId = wordId
        self.wordValue = wordValue

    def wordEngTranslate(self, recordIndex):
        return self.record(recordIndex).value('wr_value')

    def wordEngTranslateId(self, recordIndex):
        return self.record(recordIndex).value('wr_id')

    def refresh(self):
        self.setQuery('''
        SELECT
            wr.id as wr_id, wr.value as wr_value, re.rus_order as re_rus_order, wr.meaning as wr_meaning
        FROM
            word_eng as we
        JOIN rus_eng as re ON re.word_eng_id = we.id
        JOIN word_rus as wr ON wr.id = re.word_rus_id

        WHERE we.id = {weId}
        ORDER BY re.rus_order ASC
        '''.format(weId=self.wordId))  # TODO: bindValue

        for idx, field in enumerate(WordEngModel.headerFields):
            self.setHeaderData(idx, QtCore.Qt.Horizontal, field)

        self.onRefresh()

    def data(self, index, role):
        value = super(WordEngModel, self).data(index, role)

        if role == QtCore.Qt.DisplayRole:
            if index.column() in [WordEngModel.playFieldNum, WordEngModel.editFieldNum, WordEngModel.removeFieldNum]:
                return ''

        return value

    def changeOrder(self, row1, row2):
        query = QtSql.QSqlQuery()
        query.prepare(
            '''
            INSERT INTO
              rus_eng
              (word_rus_id, word_eng_id, rus_order)
            VALUES
              (:wr_id1, :we_id1, :ro1),(:wr_id2, :we_id2, :ro2)
            ON DUPLICATE KEY UPDATE rus_order=VALUES(rus_order)
            '''
        )

        query.bindValue(u":wr_id1", self.record(row1).value('wr_id'))
        query.bindValue(u":wr_id2", self.record(row2).value('wr_id'))
        query.bindValue(u":ro1", self.record(row2).value('re_rus_order'))
        query.bindValue(u":ro2", self.record(row1).value('re_rus_order'))
        query.bindValue(u":we_id1", self.wordId)
        query.bindValue(u":we_id2", self.wordId)

        try:
            query.exec_()
            self.db.commit()
            r = query.result()
            print u'change order: OK'
            return True
        except BaseException as ex:
            print ex
            self.db.rollback()
            return False

    @need_refresh
    def addEmptyTranslate(self):
        #TODO: оформить все запросы - с меньшим количество кода через враппер
        def addEmptyWord():
            query = QtSql.QSqlQuery()
            query.prepare('INSERT INTO word_rus (id) VALUES (NULL)')
            try:
                query.exec_()
                self.db.commit()
                id = query.lastInsertId()
                print u'insert empty word: id = {id}'.format(id=id)
                return id
            except BaseException as ex:
                print ex
                self.db.rollback()
                return False

        def addTranslateLink(id):
            query = QtSql.QSqlQuery()
            query.prepare('''
              INSERT INTO
                rus_eng
              (word_rus_id, word_eng_id, rus_order, eng_order)
              VALUES
                (:wr_id, :we_id, :ro, :eo)
            ''')
            query.bindValue(':wr_id', id)
            query.bindValue(':we_id', self.wordId)
            query.bindValue(':ro', self.rowCount() + 1)
            query.bindValue(':eo', 1)

            try:
                res = query.exec_() #TODO: check return value
                self.db.commit()
                print u'insert translate link'
                return True
            except BaseException as ex:
                print ex
                self.db.rollback()
                return False

        id = addEmptyWord()
        if id:
            if addTranslateLink(id):
                return id

    @need_refresh
    def removeTranslate(self, rusWordId, silent=False):
        if silent == False:
            msgBox = QtGui.QMessageBox()
            msgBox.setIcon(QtGui.QMessageBox.Question)
            msgBox.setWindowIcon(QtGui.QIcon(":/res/images/dictionary.png"))
            #   TODO: собрать больше информации о переводе. id явно не достаточно. Добавить:
            #   TODO:       1) str value
            #   TODO:       2) количество переводов, в которых он задействован
            #   TODO:       3) количество словарей, в которых он задействован
            msgBox.setText(u"Вы действительно хотите удалить перевод: id = {id}".format(id=rusWordId))
            msgBox.setWindowTitle(u"Удаление перевода")
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            if msgBox.exec_() != QtGui.QMessageBox.Ok:
                return False

        query = QtSql.QSqlQuery()
        query.prepare('DELETE FROM word_rus WHERE id = :id')

        query.bindValue(u":id", rusWordId)
        try:
            query.exec_()
            self.db.commit()
            r = query.result()
            print u'remove translate: OK'
            return True
        except BaseException as ex:
            print ex
            self.db.rollback()
            return False


    @need_refresh
    def downOrder(self, row):
        self.changeOrder(row, row + 1)

    @need_refresh
    def upOrder(self, row):
        self.changeOrder(row, row - 1)

    def columnCount(self, *args, **kwargs):
        return len(WordEngModel.fields)


class PlayButtonWordEngTranslateDelegate(PlayButtonDelegate):
    def __init__(self, parentWindow, parent, model):
        PlayButtonDelegate.__init__(self, parentWindow, parent, model)

    @pyqtSlot()
    def onBtnClicked(self, recordIndex):
        print u"play '{}'".format(self.model.wordEngTranslate(recordIndex))
        self.commitData.emit(self.sender())


class EditButtonWordEngTranslateDelegate(EditButtonDelegate):
    def __init__(self, parentWindow, parent, model):
        EditButtonDelegate.__init__(self, parentWindow, parent, model)

    @pyqtSlot()
    def onBtnClicked(self, recordIndex):
        print u"edit '{}'".format(self.model.wordEngTranslate(recordIndex))
        self.commitData.emit(self.sender())


class RemoveButtonWordEngTranslateDelegate(RemoveButtonDelegate):
    def __init__(self, parentWindow, parent, model):
        RemoveButtonDelegate.__init__(self, parentWindow, parent, model)

    @pyqtSlot()
    def onBtnClicked(self, recordIndex):
        print u"remove '{}'".format(self.model.wordEngTranslate(recordIndex))
        self.model.removeTranslate(self.model.wordEngTranslateId(recordIndex))
        self.commitData.emit(self.sender())
