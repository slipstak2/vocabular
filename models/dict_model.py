# -*- coding: utf-8 -*-

from base.base_sql_query_model import BaseSqlQuery, SqlQueryModel, SqlQuery, need_refresh


class DictModel(SqlQueryModel):
    fields = ['name', 'date_create']
    nameFieldName = fields.index('name')

    @need_refresh
    def __init__(self, srcLang, dictId):
        super(DictModel, self).__init__()
        self.initLang(srcLang)
        self.dictId = dictId
        self.utils = DictUtils(srcLang)

    @property
    def name(self):
        if self.rowCount() != 0:
            return self.record(0).value('name')

    def refresh(self):
        query = SqlQuery(
            self,
            '''
            SELECT
                {fields}
            FROM
                dict_[eng]
            WHERE
                id = {id}
            '''.format(
                fields=', '.join(self.fields),
                id=self.dictId
            )
        ).str()

        self.setQuery(query)


class DictUtils(BaseSqlQuery):
    def __init__(self, srcLang, *args, **kwargs):
        super(DictUtils, self).__init__(*args, **kwargs)
        self.initLang(srcLang)

    def addEmpty(self):
        return self.add('')

    def add(self, dictName):
        return SqlQuery(
            self,
            u'INSERT INTO dict_[eng] (name) VALUES (:name)',
            {
                ':name': dictName
            }
        ).execute(True)


    def edit(self, dictId, dictName):
        return SqlQuery(
            self,
            u'UPDATE dict_[eng] SET name=:name WHERE id=:id',
            {
                u":id": dictId,
                u":name": dictName
            }
        ).execute()


    def remove(self, dictId):
        return SqlQuery(
            self,
            u'DELETE from dict_[eng] WHERE id=:id',
            {
                u':id': dictId
            }
        ).execute()
