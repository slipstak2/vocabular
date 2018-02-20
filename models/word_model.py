# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
from PySide.QtCore import Slot as pyqtSlot
from models.base.base_sql_query_model import BaseSqlQueryModel, SqlQuery, need_refresh, need_parent_refresh
from models.delegates import EditButtonDelegate, PlayButtonDelegate, RemoveButtonDelegate
from utils import Lang


class WordModel(BaseSqlQueryModel):
    fields = ['value', 'meaning']
    valueFieldNum = fields.index('value')
    meaningFieldNum = fields.index('meaning')

    @need_refresh
    def __init__(self, parentModel, wordId, srcLang, dstLang, *args, **kwargs):
        super(WordModel, self).__init__(parentModel=parentModel, *args, **kwargs)
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


class WordModelProxy(BaseSqlQueryModel):
    def __init__(self, parentModel, wordId, srcLang, dstLang):
        super(WordModelProxy, self).__init__(parentModel=parentModel)
        self.wordId = wordId
        self.initLang(srcLang, dstLang)

    def addWordLink(self):
        from models.word_list_dict_model import WordListDictModel
        assert isinstance(self.parentModel, WordListDictModel)
        return self.parentModel.addWordLink(self.wordId)

    def edit(self, word, meaning):
        from models.word_list_dict_model import WordListDictModel
        assert isinstance(self.parentModel, WordListDictModel)
        return self.parentModel.wordModelUtils.edit(self.wordId, word, meaning)


    def refresh(self):
        pass


class WordModelUtils(BaseSqlQueryModel):
    def __init__(self, parentModel, srcLang, dstLang, *args, **kwargs):
        super(WordModelUtils, self).__init__(parentModel=parentModel, *args, **kwargs)
        self.initLang(srcLang, dstLang)

    @need_parent_refresh
    def add(self, value, meaning):
        return SqlQuery(
            self,
            'INSERT INTO word_[eng] (id, value, meaning) VALUES (NULL, :value, :meaning)',
            {
                ':value': value,
                ':meaning': meaning
            }
        ).execute(True)

    @need_parent_refresh
    def edit(self, wordId, value, meaning):
        return SqlQuery(
            self,
            'UPDATE word_[eng] SET value=:value, meaning=:meaning WHERE id=:id',
            {
                ':id': wordId,
                ':value': value,
                ':meaning': meaning
            }
        ).execute()

    @need_parent_refresh
    def remove(self, wordId):
        return SqlQuery(
            self,
            'DELETE FROM word_[eng] WHERE id=:id',
            {
                ':id': wordId
            }
        ).execute()

    def refresh(self):
        pass