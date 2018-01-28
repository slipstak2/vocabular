# -*- coding: utf-8 -*-

import functools

from PySide import QtSql

from base.base_sql_query_model import BaseSqlQueryModel
from base.utils import need_refresh


class DictionaryModel(BaseSqlQueryModel):
    fields = ['name', 'date_create', 'id']
    viewField = 'name'

    tableName = 'dictionary'

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
        self.setQuery("SELECT {fields} FROM {tableName} ORDER BY date_create".format(
            fields=', '.join(DictionaryModel.fields),
            tableName=DictionaryModel.tableName
        ))

    @need_refresh
    def addDict(self, dictName):
        query = QtSql.QSqlQuery()

        query.prepare(
            u'INSERT INTO {tableName} (name) VALUES (:name)'.format(
                tableName=DictionaryModel.tableName
            ))
        query.bindValue(u":name", dictName)

        try:
            query.exec_()
            self.db.commit()
            import sys
            print u'Добавлен новый словарь: {}'.format(dictName)
            return True
        except BaseException as ex:
            print ex
            self.db.rollback()
            return False

    @need_refresh
    def editDict(self, dictId, dictName):
        query = QtSql.QSqlQuery()
        query.prepare(
            u'UPDATE {tableName} SET name=:name WHERE id=:id'.format(
                tableName=DictionaryModel.tableName
            )
        )
        query.bindValue(u":id", dictId)
        query.bindValue(u":name", dictName)
        try:
            query.exec_()
            self.db.commit()
            print u'Отредактирован словарь: {}'.format(dictName)
            return True
        except BaseException as ex:
            print ex
            self.db.rollback()
            return False

    @need_refresh
    def removeDict(self):
        print u"TODO: Удаление только пустого словаря!"

        query = QtSql.QSqlQuery()
        query.prepare(u'DELETE from {tableName} WHERE id=:id'.format(
            tableName=DictionaryModel.tableName
        ))
        query.bindValue(u':id', self.currentDictId)

        try:
            query.exec_()
            self.db.commit()
            print u'Удаление словаря: name={}; id={}'.format(
                self.currentDictName,
                self.currentDictId
            )
            return True
        except BaseException as ex:
            print ex
            self.db.rollback()
            return False
