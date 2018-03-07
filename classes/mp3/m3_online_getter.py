# -*- coding: utf-8 -*-

import os
import json
import urllib2
from enum import Enum
from utils import createFullPath

class MP3_DICT_TYPE(Enum):
    SINGLE = 1
    MULTI = 2

    @staticmethod
    def fromString(key):
        return eval("MP3_DICT_TYPE.{}".format(key))


class Mp3JsonDict(object):
    def __init__(self, root, jsonDictData):
        self.dictPath = os.path.join(root, jsonDictData['path'])
        self.dictType = MP3_DICT_TYPE.fromString(jsonDictData['type'])
        self.data = json.load(open(self.dictPath))

    def onlineMp3Path(self, word):
        if word in self.data:
            result = self.data[word]
            if self.dictType == MP3_DICT_TYPE.SINGLE:
                result = [result]
        else:
            result = []
        return set(result)


class Mp3OnlineGetter(object):
    def __init__(self, lang, root, jsonDicts, cacheRoot):
        self.lang = lang
        self.jsonDicts = [Mp3JsonDict(root, jsonDictData) for jsonDictData in jsonDicts]
        self.cacheMp3Root = os.path.join(cacheRoot, 'mp3')
        if not os.path.exists(self.cacheMp3Root):
            os.makedirs(self.cacheMp3Root)

    def onlineMp3Paths(self, word):
        word = word.decode('utf-8').lower()
        result = set()
        for jsonDict in self.jsonDicts:
            result = result.union(jsonDict.onlineMp3Path(word))
        return sorted(result)

    def cachePath(self, url):
        return os.path.normpath(os.path.join(self.cacheMp3Root, self.lang.toShortStr(), url.replace('http://', '')))

    def checkExist(self, url):
        try:
            response = urllib2.urlopen(url)
            return response.code == 200
        except:
            return False

    def saveInLocalCache(self, url):
        try:
            mp3file = urllib2.urlopen(url)
            cachePath = self.cachePath(url)
            createFullPath(cachePath)
            with open(cachePath,'wb') as output:
                output.write(mp3file.read())
            return True
        except:
            return False
