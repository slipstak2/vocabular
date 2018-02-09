# -*- coding: utf-8 -*-

from PySide import QtSql
from db import getDb


#TODO: insert query
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


class BaseSqlQueryModel(QtSql.QSqlQueryModel):
    def __init__(self, *args, **kwargs):
        super(BaseSqlQueryModel, self).__init__(*args, **kwargs)
        self.db = getDb()
        self.onRefreshCallbacks = []

    def onRefresh(self):
        for callback in self.onRefreshCallbacks:
            callback()

    def refresh(self):
        raise NotImplementedError("pure virtual method 'refresh' must be implemented")
