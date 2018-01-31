import sys
import unittest
from models.base.db import getDb
from PySide import QtGui


class TestBaseClass(unittest.TestCase):
    isQtInit = False

    def __init__(self, *args, **kwargs):
        super(TestBaseClass, self).__init__(*args, **kwargs)
        if not TestBaseClass.isQtInit:
            QtGui.QApplication(sys.argv)
            TestBaseClass.isQtInit = True


class TestDBBaseClass(TestBaseClass):
    isDbInit = False

    def __init__(self, *args, **kwargs):
        super(TestDBBaseClass, self).__init__(*args, **kwargs)
        self.db = getDb()

    @staticmethod
    def _dbRemoveTables():
        pass

    @staticmethod
    def _dbStructureInit():
        pass

    @staticmethod
    def _dbFillContent():
        pass

    @staticmethod
    def dbInit():
        TestDBBaseClass._dbRemoveTables()
        TestDBBaseClass._dbStructureInit()
        TestDBBaseClass._dbFillContent()

    @classmethod
    def setUpClass(cls):
        if not TestDBBaseClass.isDbInit:
            TestDBBaseClass.dbInit()
            TestDBBaseClass.isDbInit = True
        print 'setUpClass: TestDBBaseClass'

    @classmethod
    def tearDownClass(cls):
        print 'tearDownClass'
