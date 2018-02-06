# -*- coding: utf-8 -*-

from PySide import QtSql
from models.base.db import getDb


def iterSqlQuery(filePath):
    currentCommand = []
    with open(filePath) as f:
        for row in f.readlines():
            currentCommand.append(row)
            if row.strip().endswith(';'):
                yield ''.join(currentCommand)
                currentCommand = []


def applySQLcommands(filePath):
    query = QtSql.QSqlQuery()
    for command in iterSqlQuery(filePath):
        command = command.decode('utf-8')
        assert query.exec_(command), query.lastError()
    getDb().commit()
