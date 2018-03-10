# -*- coding: utf-8 -*-

import os
import yaml
from enum import Enum
from utils import Singleton, Lang


class AppMode(Enum):
    UNKNOWN    = 0
    UNIT_TESTS = 1
    DEVELOP    = 2
    PRODUCTION = 3

_CONFIG_PATH = 'configs/db'

configMap = {
    AppMode.DEVELOP:    'config-develop.yaml',
    AppMode.UNIT_TESTS: 'config-unit-tests.yaml',
    AppMode.PRODUCTION: 'config-production.yaml',
}


class AppSettings:
    __metaclass__ = Singleton

    def __init__(self, mode=AppMode.UNKNOWN):
        assert mode != AppMode.UNKNOWN, 'Singleton error'

        self._mode = mode
        self._startPath = os.path.dirname(__file__)

        self._configPath = os.path.join(self._startPath, _CONFIG_PATH, configMap[mode])
        with open(self._configPath, "r") as configStream:
            self._config = yaml.load(configStream)

        self._cacheRoot = os.path.join(self._startPath, self._config['cache']['path'])

    @property
    def startPath(self):
        return self._startPath

    @property
    def config(self):
        return self._config

    @property
    def cacheRoot(self):
        return self._cacheRoot

    def dbParams(self):
        return self._config['db']

    @property
    def ftpParams(self):
        return self._config['ftp']

    @property
    def createSQLTablePath(self):
        return os.path.join(self._startPath, 'db_structure', 'create_tables.sql')

    @property
    def dropSQLTablePath(self):
        return os.path.join(self._startPath, 'db_structure', 'drop_tables.sql')

    @property
    def fillSQLTablesPath(self):
        return os.path.join(self._startPath, 'db_structure', 'fill_tables.sql')

    @property
    def allSqlCommandsPath(self):
        return os.path.join(self._startPath, 'db_structure', 'total.sql')
