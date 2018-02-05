# -*- coding: utf-8 -*-

import sys
import functools
from PySide import QtGui, QtSql
from app_settings import AppSettings


def once(func):
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        try:
            return decorated._once_result
        except AttributeError:
            decorated._once_result = func(*args, **kwargs)
            return decorated._once_result
    return decorated


@once
def getDb():
    dbParams = AppSettings().dbParams()
    db = QtSql.QSqlDatabase.addDatabase("QMYSQL")
    db.setHostName(dbParams['host'])
    db.setDatabaseName(dbParams['db'])
    db.setUserName(dbParams['user'])
    db.setPassword(dbParams['passwd'])
    ok = db.open()
    if not ok:
        QtGui.QMessageBox.warning(None, "Error", "Invalid database!")
        sys.exit(-1)
    return db