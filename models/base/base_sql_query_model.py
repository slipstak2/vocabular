# -*- coding: utf-8 -*-

from PySide import QtSql
from db import getDb
from utils import Lang


import functools


def need_refresh(func):
    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.refresh()
        return result
    return inner


def need_parent_refresh(func):
    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        parentModel = self.parentModel
        while parentModel:
            parentModel.refresh()
            parentModel = parentModel.parentModel
        return result
    return inner


class SqlQuery(object):
    def __init__(self, model, strQuery, params={}):
        self._model = model
        self._strQuery = strQuery
        self._params = params

        self._query = QtSql.QSqlQuery()
        self._prepare()

    def str(self):
        return self._normalize(self._strQuery)

    @property
    def db(self):
        return self._model.db

    def _prepare(self):
        q = self._normalize(self._strQuery)
        self._query.prepare(q)
        for name, value in self._params.items():
            self._query.bindValue(self._normalize(name), value)

    def _normalize(self, s):
        try:
            replaceLangMap = {
                '[eng]': self._model.SRC_LANG_FULL,
                '[e]': self._model.SRC_LANG_SHORT,
                '[rus]': self._model.DST_LANG_FULL,
                '[r]': self._model.DST_LANG_SHORT,
            }

            for key, value in replaceLangMap.items():
                s = s.replace(key, value)
        except BaseException:
            pass
        return s

    def execute(self, returnLastInsertId=False):
        try:
            assert self._query.exec_(), self._query.lastError()
            self.db.commit()
            return self._query.lastInsertId() if returnLastInsertId else True
        except BaseException as ex:
            print ex
            self.db.rollback()
            return False


class BaseSqlQuery(object):
    def __init__(self, parentModel):
        self.db = getDb()
        self.parentModel = parentModel

    def __str__(self):
        return '{}->{}'.format(self.SRC_LANG_FULL, self.DST_LANG_FULL)

    def initLang(self, srcLang, dstLang):
        self.srcLang = srcLang
        self.dstLang = dstLang
        if srcLang == Lang.Eng:
            assert dstLang == Lang.Rus, "Currently supported only eng-rus translation"
            self.SRC_LANG_FULL  = 'eng'
            self.SRC_LANG_SHORT = 'e'
            self.DST_LANG_FULL  = 'rus'
            self.DST_LANG_SHORT = 'r'
        else:
            assert dstLang == Lang.Eng, "Currently supported only eng-rus translation"
            self.SRC_LANG_FULL  = 'rus'
            self.SRC_LANG_SHORT = 'r'
            self.DST_LANG_FULL  = 'eng'
            self.DST_LANG_SHORT = 'e'


class SqlQueryModel(BaseSqlQuery, QtSql.QSqlQueryModel):
    def __init__(self, parentModel, *args, **kwargs):
        BaseSqlQuery.__init__(self, parentModel)
        QtSql.QSqlQueryModel.__init__(self, *args, **kwargs)

        if self.parentModel:
            self.parentModel.childModels.append(self)
        self.childModels = []
        self.onRefreshCallbacks = []

    def __str__(self):
        return ''

    def release(self):
        #assert len(self.childModels) == 0, "childModels wasn't release"
        #assert self.parentModel.childModels[-1] == self, "bad order in parent model on release"
        if self.parentModel:
            self.parentModel.childModels.pop()

    def childModelsRefresh(self):
        for childModel in self.childModels:
            childModel.refresh()
            childModel.childModelsRefresh()

    def onRefresh(self):
        for callback in self.onRefreshCallbacks:
            callback()

    def refresh(self):
        raise NotImplementedError("pure virtual method 'refresh' must be implemented")
