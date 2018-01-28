import sys
import functools
from PySide import QtGui, QtSql


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
    db = QtSql.QSqlDatabase.addDatabase("QMYSQL")
    db.setHostName("localhost")
    db.setDatabaseName("voc-app-db")
    db.setUserName("root")
    db.setPassword("passwd")
    ok = db.open()
    if not ok:
        QtGui.QMessageBox.warning(None, "Error", "Invalid database!")
        sys.exit(-1)
    return db