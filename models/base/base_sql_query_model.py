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
        replaceLangMap = {
            '[eng]': 'SRC_LANG_FULL',
            '[e]': 'SRC_LANG_SHORT',
            '[rus]': 'DST_LANG_FULL',
            '[r]': 'DST_LANG_SHORT',
        }
        for key, value in replaceLangMap.items():
            if hasattr(self._model, value):
                s = s.replace(key, getattr(self._model, value))
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
    def __init__(self):
        self.db = getDb()

    def __str__(self):
        return '{}->{}'.format(self.SRC_LANG_FULL, self.DST_LANG_FULL)

    def initLang(self, srcLang, dstLang=Lang.Unknown):
        self.srcLang = srcLang
        if dstLang != Lang.Unknown:
            self.dstLang = dstLang
        if srcLang == Lang.Eng:
            self.SRC_LANG_FULL  = 'eng'
            self.SRC_LANG_SHORT = 'e'
            if dstLang != Lang.Unknown:
                self.DST_LANG_FULL  = 'rus'
                self.DST_LANG_SHORT = 'r'
        elif srcLang == Lang.Rus:
            self.SRC_LANG_FULL  = 'rus'
            self.SRC_LANG_SHORT = 'r'
            if dstLang != Lang.Unknown:
                self.DST_LANG_FULL  = 'eng'
                self.DST_LANG_SHORT = 'e'


class SqlQueryModel(BaseSqlQuery, QtSql.QSqlQueryModel):
    def __init__(self, *args, **kwargs):
        BaseSqlQuery.__init__(self)
        QtSql.QSqlQueryModel.__init__(self, *args, **kwargs)

        self.childModels = []
        self.onRefreshCallbacks = []

    def addChildModel(self, childModel):
        self.childModels.append(childModel)

    def childModelsRefresh(self):
        for childModel in self.childModels:
            childModel.refresh()
            childModel.childModelsRefresh()

    def onRefresh(self):
        for callback in self.onRefreshCallbacks:
            callback()

    def refresh(self):
        raise NotImplementedError("pure virtual method 'refresh' must be implemented")
