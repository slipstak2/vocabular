# -*- coding: utf-8 -*-

from base.base_sql_query_model import BaseSqlQueryModel, SqlQuery, need_refresh
from models.dict_model import DictModelUtils, DictModelProxy


class DictListModel(BaseSqlQueryModel):
    fields = ['name', 'date_create', 'id']
    viewField = 'name'

    @need_refresh
    def __init__(self, dictIndex=0, *args, **kwargs):
        super(DictListModel, self).__init__(parentModel=None, *args, **kwargs)
        self._dictIndex = dictIndex
        self.dictModelProxy = DictModelProxy(self)

        self.dictModelUtils = DictModelUtils(self)

    @property
    def dictIndex(self):
        return self._dictIndex

    @dictIndex.setter
    def dictIndex(self, index):
        self._dictIndex = index
        self.childModelsRefresh()

    @property
    def dictId(self):
        return self.record(self.dictIndex).value('id')

    @property
    def dictName(self):
        return self.record(self.dictIndex).value('name')

    def viewFieldIndex(self):
        return self.fieldIndex(DictListModel.viewField)

    def fieldIndex(self, fieldName):
        return DictListModel.fields.index(fieldName)

    def refresh(self):
        self.setQuery("SELECT {fields} FROM dictionary ORDER BY date_create".format(
            fields=', '.join(DictListModel.fields)
        ))

    # TODO: так ли нужны высокоуровневые методы, а может некоторые просто убрать?
    def addDict(self, dictName):
        return self.dictModelUtils.add(dictName)

    def editDict(self, dictName, dictId=None):
        return self.dictModelUtils.edit(dictId if dictId else self.dictId, dictName)

    def removeDict(self, dictId=None):
        return self.dictModelUtils.remove(dictId if dictId else self.dictId)
