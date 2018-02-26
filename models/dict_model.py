# -*- coding: utf-8 -*-

from base.base_sql_query_model import BaseSqlQuery, SqlQueryModel, SqlQuery, need_refresh


class DictModel(SqlQueryModel):
    fields = ['name', 'date_create']
    nameFieldName = fields.index('name')

    @need_refresh
    def __init__(self, dictId):
        super(DictModel, self).__init__()
        self.dictId = dictId
        self.utils = DictModelUtils()

    @property
    def name(self):
        if self.rowCount() != 0:
            return self.record(0).value('name')

    def refresh(self):
        self.setQuery(
            '''
            SELECT
                {fields}
            FROM
                dictionary
            WHERE
                id = {id}'''.format(
                fields=', '.join(self.fields),
                id=self.dictId
            )
        )


class DictModelUtils(BaseSqlQuery):
    def __init__(self, *args, **kwargs):
        super(DictModelUtils, self).__init__(*args, **kwargs)

    def addEmpty(self):
        return self.add('')

    def add(self, dictName):
        return SqlQuery(
            self,
            u'INSERT INTO dictionary (name) VALUES (:name)',
            {
                ':name': dictName
            }
        ).execute(True)


    def edit(self, dictId, dictName):
        return SqlQuery(
            self,
            u'UPDATE dictionary SET name=:name WHERE id=:id',
            {
                u":id": dictId,
                u":name": dictName
            }
        ).execute()


    def remove(self, dictId):
        return SqlQuery(
            self,
            u'DELETE from dictionary WHERE id=:id',
            {
                u':id': dictId
            }
        ).execute()
