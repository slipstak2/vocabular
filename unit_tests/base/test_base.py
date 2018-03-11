# -*- coding: utf-8 -*-

import os
import sys
import unittest
import shutil
from PySide import QtGui

from classes.ftp.ftp_manager import FtpManager
from models.base.db import getDb
from app_settings import AppSettings
from unit_tests.unit_tests_utils import applySQLcommands


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
    def dbInit():
        sqlPaths = [
            AppSettings().dropSQLTablePath,
            AppSettings().createSQLTablePath,
            AppSettings().fillSQLTablesPath
        ]
        with open(AppSettings().allSqlCommandsPath, 'w') as total:
            for sqlPath in sqlPaths:
                with open(sqlPath, 'r') as f:
                    content = f.read()
                    total.write(content + '\n')

        applySQLcommands(AppSettings().allSqlCommandsPath)

    @classmethod
    def setUpClass(cls):
        if not TestDBBaseClass.isDbInit:
            TestDBBaseClass.dbInit()
            TestDBBaseClass.isDbInit = True

    @classmethod
    def tearDownClass(cls):
        pass


class TestSoundBaseClass(TestBaseClass):
    def __init__(self, *args, **kwargs):
        TestBaseClass.__init__(self, *args, **kwargs)

    @classmethod
    def setUpClass(cls):
        if os.path.exists(AppSettings()._cacheRoot):
            shutil.rmtree(AppSettings()._cacheRoot)


class TestFtpBaseClass(TestBaseClass):
    def __init__(self, *args, **kwargs):
        TestBaseClass.__init__(self, *args, **kwargs)

    @classmethod
    def setUpClass(cls):
        with FtpManager() as ftpManager:
            ftpManager.clearDirectoryContent(ftpManager.rootDir)
