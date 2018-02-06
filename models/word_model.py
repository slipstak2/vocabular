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

    def data(self, index, role):
        value = super(WordModel, self).data(index, role)
        if role == QtCore.Qt.DisplayRole:
            if index.column() in [self.playFieldNum, self.editFieldNum, self.removeFieldNum]:
                return ''
        return value
