from PySide import QtSql

from db import getDb


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
