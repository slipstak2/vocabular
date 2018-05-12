# -*- coding: utf-8 -*-

from base.base_sql_query_model import SqlQueryModel, need_refresh, SqlQuery
from models.dict_model import DictModelUtils
from utils import Lang


class DictListModel(SqlQueryModel):
    fields = ['name', 'date_create', 'id']

    @need_refresh
    def __init__(self, srcLang, dictIndex=0, *args, **kwargs):
        super(DictListModel, self).__init__(*args, **kwargs)
        self.initLang(srcLang)
        self._dictIndex = dictIndex

        self.dictModelUtils = DictModelUtils(srcLang)

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
        query = SqlQuery(
            self,
            "SELECT {fields} FROM dict_[eng] ORDER BY date_create".format(
                fields=', '.join(DictListModel.fields)
            )
        ).str()

        self.setQuery(query)

    @need_refresh
    def removeDict(self):
        return self.dictModelUtils.remove(self.dictId)
