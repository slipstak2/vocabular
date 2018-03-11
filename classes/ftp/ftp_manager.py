# -*- coding: utf-8 -*-

# https://python-scripts.com/ftplib

import os
from ftplib import FTP
from app_settings import AppSettings, AppMode


class FtpManager(object):
    def __init__(self, subdir=''):
        self._subdir = subdir
        self.ftpParams = AppSettings().ftpParams
        self.ftp = FTP(self.ftpParams['host'])
        self.connect()
        self.garanteeExistPath(self.rootDir)

        print(self.ftp.retrlines('LIST'))
        self.ftp.cwd(self.ftpParams['root-dir'])
        print(self.ftp.retrlines('LIST'))

        print(self.ftp.nlst())

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.ftp.close()

    def clearDirectoryContent(self, ftpPath):
        pass

    def connect(self):
        self._loginInfo = self.ftp.login(self.ftpParams['user'], self.ftpParams['passwd'])
        self._isLogin = self._loginInfo == '230 Login successful.'

    @property
    def isConnect(self):
        return self._isLogin

    @property
    def rootDir(self):
        return os.path.join(self.ftpParams['root-dir'], self._subdir)

    def garanteeExistPath(self, ftpPath):
        print ftpPath

    def checkExist(self, ftpPath):
        pass


    def upload(self, localPath, ftype='TXT'):
        if ftype == 'TXT':
            with open(localPath) as f:
                self.ftp.storlines('STOR ' + localPath, f)
        else:
            with open(localPath, 'rb') as f:
                self.ftp.storbinary('STOR ' + localPath, f, 1024)


class FtfAudioManager(FtpManager):
    def __init__(self):
        FtpManager.__init__(self, 'audio')

if __name__ == '__main__':
    AppSettings(AppMode.DEVELOP)
    manager = FtfAudioManager()
    manager.upload(r'C:\1.txt')
