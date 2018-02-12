# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
from PySide.QtCore import Slot as pyqtSlot
from models.base.base_sql_query_model import BaseSqlQueryModel, SqlQuery, need_refresh
from models.delegates import EditButtonDelegate, PlayButtonDelegate, RemoveButtonDelegate
from utils import Lang


class WordModel(BaseSqlQueryModel):
    fields = ['value', 'meaning']
    valueFieldNum = fields.index('value')
    meaningFieldNum = fields.index('meaning')

    @need_refresh
    def __init__(self, wordId, srcLang, dstLang, *args, **kwargs):
        super(WordModel, self).__init__(*args, **kwargs)
        self.wordId = wordId
        self.initLang(srcLang, dstLang)

    @property
    def wordValue(self):
        if self.rowCount() != 0:
            return self.record(0).value('value')
        return ''

    @property
    def wordMeaning(self):
        if self.rowCount() != 0:
            return self.record(0).value('meaning')
        return ''

    def refresh(self):
        if self.wordId:
            query = SqlQuery(
                self,
                '''
                SELECT
                    value, meaning
                FROM
                    word_[eng]
                WHERE
                    id = {word_id}
                '''.format(word_id=self.wordId)
            ).str()
            self.setQuery(query)

        self.onRefresh()

    def addWord(self, value, meaning):
        return SqlQuery(
            self,
            'INSERT INTO word_[eng] (id, value, meaning) VALUES (NULL, :value, :meaning)',
            {
                ':value': value,
                ':meaning': meaning
            }
        ).execute(True)

    @need_refresh
    def update(self, value, meaning):
        return SqlQuery(
            self,
            'UPDATE word_[eng] SET value=:value, meaning=:meaning WHERE id=:id',
            {
                ':value': value,
                ':meaning': meaning,
                ':id': self.wordId
            }
        ).execute()

    @need_refresh
    def remove(self, id=None):
        return SqlQuery(
            self,
            'DELETE FROM word_[eng] WHERE id=:id',
            {
                ':id': id if id else self.wordId
            }
        ).execute()
