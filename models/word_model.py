# -*- coding: utf-8 -*-

from PySide import QtSql, QtCore, QtGui
from PySide.QtCore import Slot as pyqtSlot
from models.base.utils import need_refresh
from models.base.base_sql_query_model import BaseSqlQueryModel
from models.delegates import EditButtonDelegate, PlayButtonDelegate, RemoveButtonDelegate
from utils import Lang


class WordModel(BaseSqlQueryModel):
    @need_refresh
    def __init__(self, wordId, wordValue, srcLang, dstLang, *args, **kwargs):
        super(WordModel, self).__init__(*args, **kwargs)
        self.wordId = wordId
        self.wordValue = wordValue
        self.srcLang = srcLang
        self.dstLang = dstLang

        if srcLang == Lang.Eng:
            assert dstLang == Lang.Rus, "Currently supported only eng-rus translation"
            self.SRC_LANG_FULL  = 'eng'
            self.SRC_LANG_SHORT = 'e'
            self.DST_LANG_FULL  = 'rus'
            self.DST_LANG_SHORT = 'r'
            self.headerFields = [     '', u'перевод',             '',   u'значение',     '',     '',       '']
            self.fields =       ['wr_id', 'wr_value', 're_rus_order',  'wr_meaning', 'play', 'edit', 'remove']
        else:
            assert dstLang == Lang.Eng, "Currently supported only eng-rus translation"
            self.SRC_LANG_FULL  = 'rus'
            self.SRC_LANG_SHORT = 'r'
            self.DST_LANG_FULL  = 'eng'
            self.DST_LANG_SHORT = 'e'
            self.headerFields = [     '', u'перевод',             '',   u'значение',     '',     '',       '']
            self.fields =       ['we_id', 'we_value', 're_eng_order',  'we_meaning', 'play', 'edit', 'remove']

        self.playFieldNum = self.fields.index('play')
        self.editFieldNum = self.fields.index('edit')
        self.removeFieldNum = self.fields.index('remove')

    def wordTranslate(self, recordIndex):
        return self.record(recordIndex).value('w{r}_value'.format(r=self.DST_LANG_SHORT))

    def wordTranslateId(self, recordIndex):
        return self.record(recordIndex).value('w{r}_id'.format(r=self.DST_LANG_SHORT))

    def wordTranslateOrder(self, recordIndex):
        return self.record(recordIndex).value('re_{rus}_order'.format(rus=self.DST_LANG_FULL))

    def refresh(self):
        query = '''
        SELECT
            word_{rus}.id as w{r}_id, word_{rus}.value as w{r}_value, rus_eng.{rus}_order as r{e}_{rus}_order, word_{rus}.meaning as w{r}_meaning
        FROM
            word_{eng}
        JOIN rus_eng ON rus_eng.word_{eng}_id = word_{eng}.id
        JOIN word_{rus} ON word_{rus}.id = rus_eng.word_{rus}_id
        WHERE
            word_{eng}.id = {word_id}
        ORDER BY
            rus_eng.{rus}_order ASC
        '''.format(
            word_id=self.wordId,
            r=self.DST_LANG_SHORT,
            rus=self.DST_LANG_FULL,
            e=self.SRC_LANG_SHORT,
            eng=self.SRC_LANG_FULL
        )

        self.setQuery(query)

        for idx, field in enumerate(self.headerFields):
            self.setHeaderData(idx, QtCore.Qt.Horizontal, field)

        self.onRefresh()

    def changeOrder(self, row1, row2):
        query = QtSql.QSqlQuery()
        query.prepare(
            '''
            INSERT INTO
              rus_eng
              (word_{rus}_id, word_{eng}_id, {rus}_order)
            VALUES
              (:w{r}_id1, :w{e}_id1, :{r}o1),(:w{r}_id2, :w{e}_id2, :{r}o2)
            ON DUPLICATE KEY UPDATE {rus}_order=VALUES({rus}_order)
            '''.format(
                r=self.DST_LANG_SHORT,
                rus=self.DST_LANG_FULL,
                e=self.SRC_LANG_SHORT,
                eng=self.SRC_LANG_FULL
            )
        )

        query.bindValue(":w{r}_id1".format(r=self.DST_LANG_SHORT), self.wordTranslateId(row1))
        query.bindValue(":w{r}_id2".format(r=self.DST_LANG_SHORT), self.wordTranslateId(row2))
        query.bindValue(":{r}o1".format(r=self.DST_LANG_SHORT), self.wordTranslateOrder(row2))
        query.bindValue(":{r}o2".format(r=self.DST_LANG_SHORT), self.wordTranslateOrder(row1))
        query.bindValue(":w{e}_id1".format(e=self.SRC_LANG_SHORT), self.wordId)
        query.bindValue(":w{e}_id2".format(e=self.SRC_LANG_SHORT), self.wordId)

        return self.executeQuery(query)

    @need_refresh
    def addEmptyTranslate(self):
        def addEmptyWord():
            query = QtSql.QSqlQuery()
            query.prepare('INSERT INTO word_rus (id) VALUES (NULL)')
            return self.executeQuery(query, True)

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

            return self.executeQuery(query)

        id = addEmptyWord()
        if id:
            if addTranslateLink(id):
                return id
        return False

    def data(self, index, role):
        value = super(WordModel, self).data(index, role)
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
