# -*- coding: utf-8 -*-

from models.base.base_sql_query_model import \
    BaseSqlQuery, SqlQueryModel, SqlQuery, \
    need_refresh


class WordModel(SqlQueryModel):
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


class WordInfo(BaseSqlQuery):
    def __init__(self, wordId, srcLang, dstLang):
        super(WordInfo, self).__init__()
        self.wordId = wordId
        self.utils = WordUtils(srcLang, dstLang)
        self.initLang(srcLang, dstLang)


class WordUtils(BaseSqlQuery):
    def __init__(self, srcLang, dstLang, *args, **kwargs):
        super(WordUtils, self).__init__(*args, **kwargs)
        self.initLang(srcLang, dstLang)

    def addEmpty(self):
        return self.add('', '')

    def add(self, value, meaning):
        return SqlQuery(
            self,
            'INSERT INTO word_[eng] (id, value, meaning) VALUES (NULL, :value, :meaning)',
            {
                ':value': value,
                ':meaning': meaning
            }
        ).execute(True)

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

    def remove(self, wordId):
        return SqlQuery(
            self,
            'DELETE FROM word_[eng] WHERE id=:id',
            {
                ':id': wordId
            }
        ).execute()
