# -*- coding: utf-8 -*-

from base.base_sql_query_model import BaseSqlQueryModel, SqlQuery, need_refresh, need_parent_refresh


class DictModel(BaseSqlQueryModel):
    fields = ['name', 'date_create', 'id']
    nameFieldName = fields.index('name')

    @need_refresh
    def __init__(self, parentModel, dictId):
        super(DictModel, self).__init__(parentModel=parentModel)
        self.parentModel = parentModel
        self.dictId = dictId

    @property
    def name(self):
        if self.rowCount() != 0:
            return self.record(0).value('name')
        return None

    @property
    def id(self):
        if self.rowCount() != 0:
            return self.record(0).value('id')
        return None

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


class DictModelProxy(BaseSqlQueryModel):
    def __init__(self, dictListModel):
        super(DictModelProxy, self).__init__(parentModel=dictListModel)

    @property
    def dictId(self):
        return self.parentModel.currentDictId

    def refresh(self):
        pass


class DictModelUtils(BaseSqlQueryModel):
    def __init__(self, parentModel, *args, **kwargs):
        super(DictModelUtils, self).__init__(parentModel=parentModel, referenceWithParent=False, *args, **kwargs)

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

    def refresh(self):
        pass
