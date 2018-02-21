# -*- coding: utf-8 -*-

from base.base_sql_query_model import SqlQueryModel, need_refresh
from models.dict_model import DictModelUtils


class DictListModel(SqlQueryModel):
    fields = ['name', 'date_create', 'id']

    @need_refresh
    def __init__(self, dictIndex=0, *args, **kwargs):
        super(DictListModel, self).__init__(parentModel=None, *args, **kwargs)
        self._dictIndex = dictIndex

        self.getDictId = lambda: self.dictId
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

    def fieldIndex(self, fieldName):
        return DictListModel.fields.index(fieldName)

    def refresh(self):
        self.setQuery("SELECT {fields} FROM dictionary ORDER BY date_create".format(
            fields=', '.join(DictListModel.fields)
        ))

    def addDict(self, dictName):
        return self.dictModelUtils.add(dictName)

    def editDict(self, dictName):
        return self.dictModelUtils.edit(self.dictId, dictName)

    def removeDict(self):
        return self.dictModelUtils.remove(self.dictId)
