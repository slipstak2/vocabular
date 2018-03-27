# -*- coding: utf-8 -*-

import os
import json
import urllib2
from enum import Enum
from utils import createFullPath, Lang
from app_settings import AppSettings
from classes.ftp.ftp_manager import FtpManager


class SOUND_DICT_TYPE(Enum):
    SINGLE = 1
    MULTI = 2

    @staticmethod
    def fromString(key):
        return eval("SOUND_DICT_TYPE.{}".format(key))


class SoundFilesJsonDict(object):
    def __init__(self, root, jsonDictData):
        self.dictPath = os.path.join(root, jsonDictData['path'])
        self.dictType = SOUND_DICT_TYPE.fromString(jsonDictData['type'])
        self.data = json.load(open(self.dictPath))

    def onlineSoundPath(self, word):
        if word in self.data:
            result = self.data[word]
            if self.dictType == SOUND_DICT_TYPE.SINGLE:
                result = [result]
        else:
            result = []
        return set(result)


class SoundFilesManager(object):
    def __init__(self, lang, root, jsonDicts):
        self.lang = lang
        self.jsonDicts = [SoundFilesJsonDict(root, jsonDictData) for jsonDictData in jsonDicts]

    def onlineSoundPaths(self, word):
        word = word.decode('utf-8').lower()
        result = set()
        for jsonDict in self.jsonDicts:
            result = result.union(jsonDict.onlineSoundPath(word))
        return sorted(result)






SoundEng = SoundFilesManager(
    Lang.Eng,
    AppSettings().startPath,
    AppSettings().config['sound']['eng'],
)
