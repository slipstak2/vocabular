# -*- coding: utf-8 -*-

from base.base_sql_query_model import BaseSqlQueryModel, SqlQuery, need_refresh
from models.dict_model import DictModelUtils


class DictListModel(BaseSqlQueryModel):
    fields = ['name', 'date_create', 'id']
    viewField = 'name'

    @need_refresh
    def __init__(self, currentDictIndex=0, *args, **kwargs):
        super(DictListModel, self).__init__(*args, **kwargs)
        self._currentDictIndex = currentDictIndex
        self.childModels = []

        self.dictModelUtils = DictModelUtils(self)

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
        return self.fieldIndex(DictListModel.viewField)

    def fieldIndex(self, fieldName):
        return DictListModel.fields.index(fieldName)

    def refresh(self):
        self.setQuery("SELECT {fields} FROM dictionary ORDER BY date_create".format(
            fields=', '.join(DictListModel.fields)
        ))

    def addDict(self, dictName):
        return self.dictModelUtils.add(dictName)

    def editDict(self, dictName, dictId=None):
        return self.dictModelUtils.edit(dictId if dictId else self.currentDictId, dictName)

    def removeDict(self, dictId=None):
        return self.dictModelUtils.remove(dictId if dictId else self.currentDictId)
