# -*- coding: utf-8 -*-

import os
from enum import IntEnum

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Lang(IntEnum):
    Rus = 0
    Eng = 1
    Unknown = 2

    def toShortStr(self):
        return str(self).replace('Lang.', '')

rxEng = u"[a-zA-Z0-9_- ]+"
rxRus = u"[а-яА-Я0-9_- ]+"


def createFullPath(localPath):
    dirPath = os.path.dirname(localPath)
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)