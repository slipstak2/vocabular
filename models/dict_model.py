# -*- coding: utf-8 -*-

from PySide import QtSql

from base.base_sql_query_model import BaseSqlQueryModel
from base.utils import need_refresh


class DictionaryModel(BaseSqlQueryModel):
    fields = ['name', 'date_create', 'id']
    viewField = 'name'

    @need_refresh
    def __init__(self, currentDictIndex=0, *args, **kwargs):
        super(DictionaryModel, self).__init__(*args, **kwargs)
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
        return self.fieldIndex(DictionaryModel.viewField)

    def fieldIndex(self, fieldName):
        return DictionaryModel.fields.index(fieldName)

    def refresh(self):
        self.setQuery("SELECT {fields} FROM dictionary ORDER BY date_create".format(
            fields=', '.join(DictionaryModel.fields)
        ))

    @need_refresh
    def addDict(self, dictName):
        query = QtSql.QSqlQuery()
        query.prepare(u'INSERT INTO dictionary (name) VALUES (:name)')
        query.bindValue(u":name", dictName)

        return self.executeQuery(query)

    @need_refresh
    def editDict(self, dictId, dictName):
        query = QtSql.QSqlQuery()
        query.prepare(u'UPDATE dictionary SET name=:name WHERE id=:id')
        query.bindValue(u":id", dictId)
        query.bindValue(u":name", dictName)
        return self.executeQuery(query)

    @need_refresh
    def removeDict(self):
        query = QtSql.QSqlQuery()
        query.prepare(u'DELETE from dictionary WHERE id=:id')
        query.bindValue(u':id', self.currentDictId)

        return self.executeQuery(query)
