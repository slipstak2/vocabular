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
    def __init__(self, lang, root, jsonDicts, cacheRoot):
        self.lang = lang
        self.jsonDicts = [SoundFilesJsonDict(root, jsonDictData) for jsonDictData in jsonDicts]
        self.cacheSound3Root = os.path.join(cacheRoot, 'sound')
        if not os.path.exists(self.cacheSound3Root):
            os.makedirs(self.cacheSound3Root)

    def onlineSoundPaths(self, word):
        word = word.decode('utf-8').lower()
        result = set()
        for jsonDict in self.jsonDicts:
            result = result.union(jsonDict.onlineSoundPath(word))
        return sorted(result)

    def cachePath(self, url):
        return os.path.normpath(os.path.join(self.cacheSound3Root, self.lang.toShortStr(), url.replace('http://', '')))

    def checkOnlineExist(self, url):
        try:
            response = urllib2.urlopen(url)
            return response.code == 200
        except:
            return False

    def checkCacheExist(self, url):
        return os.path.exists(self.cachePath(url))

    def saveInLocalCache(self, url):
        try:
            soundFile = urllib2.urlopen(url)
            cachePath = self.cachePath(url)
            createFullPath(cachePath)
            with open(cachePath,'wb') as output:
                output.write(soundFile.read())
            return True
        except:
            return False

    def uploadToFtp(self, url):
        if not self.checkCacheExist(url):
            self.saveInLocalCache(url)
            assert self.checkCacheExist(url), "save in local cache error"

        localPath = self.cachePath(url)
        # TODO: context manager
        #manager = FtpManager()
        #manager.upload(localPath)




SoundEng = SoundFilesManager(
    Lang.Eng,
    AppSettings().startPath,
    AppSettings().config['sound']['eng'],
    AppSettings().cacheRoot
)
