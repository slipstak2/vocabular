# -*- coding: utf-8 -*-

from base.base_sql_query_model import \
    BaseSqlQuery, SqlQueryModel, SqlQuery, \
    need_refresh, \
    need_parent_refresh


class DictModel(SqlQueryModel):
    fields = ['name', 'date_create']
    nameFieldName = fields.index('name')

    @need_refresh
    def __init__(self, parentModel, dictId):
        super(DictModel, self).__init__(parentModel=parentModel)
        self.dictId = dictId

    @property
    def id(self):
        return self.dictId

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


class DictModelProxyViewer(SqlQueryModel):
    def __init__(self, dictListModel):
        super(DictModelProxyViewer, self).__init__(parentModel=dictListModel)

    @property
    def dictId(self):
        return self.parentModel.dictId

    def refresh(self):
        pass


class DictModelUtils(BaseSqlQuery):
    def __init__(self, parentModel, *args, **kwargs):
        super(DictModelUtils, self).__init__(parentModel=parentModel, *args, **kwargs)

    @need_parent_refresh
    def add(self, dictName):
        return SqlQuery(
            self,
            u'INSERT INTO dictionary (name) VALUES (:name)',
            {
                ':name': dictName
            }
        ).execute(True)

    @need_parent_refresh
    def edit(self, dictId, dictName):
        return SqlQuery(
            self,
            u'UPDATE dictionary SET name=:name WHERE id=:id',
            {
                u":id": dictId,
                u":name": dictName
            }
        ).execute()

    @need_parent_refresh
    def remove(self, dictId):
        return SqlQuery(
            self,
            u'DELETE from dictionary WHERE id=:id',
            {
                u':id': dictId
            }
        ).execute()
