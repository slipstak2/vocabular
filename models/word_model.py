# -*- coding: utf-8 -*-

from models.base.base_sql_query_model import \
    BaseSqlQuery, SqlQueryModel, SqlQuery, \
    need_refresh, need_parent_refresh


class WordModel(SqlQueryModel):
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


class WordModelInfo(SqlQueryModel):
    def __init__(self, parentModel, wordId, srcLang, dstLang):
        super(WordModelInfo, self).__init__(parentModel=parentModel)
        self.wordId = wordId
        self.initLang(srcLang, dstLang)

    def refresh(self):
        pass


class WordModelUtils(BaseSqlQuery):
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
