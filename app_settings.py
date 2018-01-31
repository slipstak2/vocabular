import os
import sys
import yaml
from enum import Enum
from utils import Singleton


class AppMode(Enum):
    UNKNOWN    = 0
    UNIT_TESTS = 1
    DEVELOP    = 2
    PRODUCTION = 3

_CONFIG_PATH = 'configs/db'

configMap = {
    AppMode.DEVELOP:    'config-local.yaml',
    AppMode.UNIT_TESTS: 'config-unit-tests.yaml',
    AppMode.PRODUCTION: 'config-production.yaml',
}


class AppSettings:
    __metaclass__ = Singleton

    def __init__(self, mode=AppMode.UNKNOWN):
        assert mode != AppMode.UNKNOWN, 'Singleton error'

        self._mode = mode
        self._startPath = os.path.dirname(sys.argv[0])
        self._configPath = os.path.join(self._startPath, _CONFIG_PATH, configMap[mode])

        with open(self._configPath, "r") as configStream:
            self._config = yaml.load(configStream)

    def dbParams(self):
        return self._config['db']
