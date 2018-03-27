import os
import urllib2
from classes.file.base_file import BaseFile
from utils import createFullPath, Lang
from app_settings import AppSettings


class WebFile(BaseFile):
    def __init__(self, category, lang, url):
        BaseFile.__init__(self, lang, category)
        self._url = url

    @property
    def url(self):
        return self._url

    def checkOnlineExist(self):
        try:
            response = urllib2.urlopen(self.url)
            return response.code == 200
        except:
            return False

    @property
    def cacheRoot(self):
        return os.path.join(AppSettings().cacheRoot, self.category)

    @property
    def cachePath(self):
        return os.path.normpath(os.path.join(self.cacheRoot, self.lang.toShortStr(), self.url.replace('http://', '')))

    def checkCacheExist(self):
        return os.path.exists(self.cachePath)

    def saveInLocalCache(self):
        try:
            webFile = urllib2.urlopen(self.url)
            createFullPath(self.cachePath)
            with open(self.cachePath,'wb') as output:
                output.write(webFile.read())
            return True
        except:
            return False
