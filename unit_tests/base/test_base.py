# -*- coding: utf-8 -*-

import sys
import unittest
from models.base.db import getDb
from app_settings import AppSettings
from unit_tests.unit_tests_utils import applySQLcommands
from PySide import QtGui


class TestBaseClass(unittest.TestCase):
    app = None

    def __init__(self, *args, **kwargs):
        super(TestBaseClass, self).__init__(*args, **kwargs)
        if not TestBaseClass.app:
            TestBaseClass.app = QtGui.QApplication(sys.argv)


class TestDBBaseClass(TestBaseClass):
    isDbInit = False

    def __init__(self, *args, **kwargs):
        super(TestDBBaseClass, self).__init__(*args, **kwargs)
        self.db = getDb()

    @staticmethod
    def _dbDropTables():
        applySQLcommands(AppSettings().dropSQLTablePath)

    @staticmethod
    def _dbCreateTables():
        applySQLcommands(AppSettings().createSQLTablePath)

    @staticmethod
    def _dbFillTables():
        applySQLcommands(AppSettings().fillSQLTablesPath)

    @staticmethod
    def dbInit():
        TestDBBaseClass._dbDropTables()
        TestDBBaseClass._dbCreateTables()
        TestDBBaseClass._dbFillTables()

    @classmethod
    def setUpClass(cls):
        if not TestDBBaseClass.isDbInit:
            TestDBBaseClass.dbInit()
            TestDBBaseClass.isDbInit = True

    @classmethod
    def tearDownClass(cls):
        pass
