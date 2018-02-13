# -*- coding: utf-8 -*-

from base.base_sql_query_model import BaseSqlQueryModel, SqlQuery, need_refresh

class DictionaryListModel(BaseSqlQueryModel):
    fields = ['name', 'date_create', 'id']
    viewField = 'name'

    @need_refresh
    def __init__(self, currentDictIndex=0, *args, **kwargs):
        super(DictionaryListModel, self).__init__(*args, **kwargs)
        self._currentDictIndex = currentDictIndex
        self.childModels = []

    @property
    def currentDictIndex(self):
        return self._currentDictIndex

    @currentDictIndex.setter
    def currentDictIndex(self, index):
        self._currentDictIndex = index
        for childModel in self.childModels:
            childModel.refresh()

    @property
    def currentDictId(self):
        return self.record(self.currentDictIndex).value('id')

    @property
    def currentDictName(self):
        return self.record(self.currentDictIndex).value('name')

    def viewFieldIndex(self):
        return self.fieldIndex(DictionaryListModel.viewField)

    def fieldIndex(self, fieldName):
        return DictionaryListModel.fields.index(fieldName)

    def refresh(self):
        self.setQuery("SELECT {fields} FROM dictionary ORDER BY date_create".format(
            fields=', '.join(DictionaryListModel.fields)
        ))

    @need_refresh
    def addDict(self, dictName):
        return SqlQuery(
            self,
            u'INSERT INTO dictionary (name) VALUES (:name)',
            {
                ':name': dictName
            }
        ).execute(True)

    @need_refresh
    def editDict(self, dictId, dictName):
        return SqlQuery(
            self,
            u'UPDATE dictionary SET name=:name WHERE id=:id',
            {
                u":id": dictId,
                u":name": dictName
            }
        ).execute()

    @need_refresh
    def removeDict(self):
        return SqlQuery(
            self,
            u'DELETE from dictionary WHERE id=:id',
            {
                u':id': self.currentDictId
            }
        ).execute()
