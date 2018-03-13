# -*- coding: utf-8 -*-

# https://python-scripts.com/ftplib

import os
from ftplib import FTP, all_errors
from app_settings import AppSettings, AppMode


'''
with FtpCwd(self.ftp, ftpPath) as ftp:
    for something in ftp.nlst():
        try:
            ftp.delete(something)
        except Exception:
            ftp.rmd(something)'''

class FtpCwd(object):
    def __init__(self, ftp, newCwd):
        self.ftp = ftp
        self.pwd = self.ftp.pwd()
        self.ftp.cwd(newCwd)

    def __enter__(self):
        return self.ftp

    def __exit__(self, *args):
        self.ftp.cwd(self.pwd)


def ftpJoin(root, dir):
    result = '/{}/{}'.format(root, dir)
    result = result.replace('//', '/')
    return result


class FtpManager(object):
    def __init__(self, subdir=''):
        self._subdir = subdir
        self.ftpParams = AppSettings().ftpParams
        self.ftp = FTP(self.ftpParams['host'])
        self.login()
        self.garanteeExistPath(self.rootDir)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.ftp.close()

    def clearDirectoryContent(self, ftpPath, deep=0):
        wd = self.ftp.pwd()
        names = self.ftp.nlst(ftpPath)
        for name in names:
            if os.path.split(name)[1] in ('.', '..'):
                continue
            try:
                self.ftp.cwd(name)
                self.ftp.cwd(wd)
                self.clearDirectoryContent(name, deep + 1)
            except all_errors:
                self.ftp.delete(name)

        if deep != 0:
            self.ftp.rmd(ftpPath)

    def login(self):
        self._loginInfo = self.ftp.login(self.ftpParams['user'], self.ftpParams['passwd'])
        self._isLogin = self._loginInfo == '230 Login successful.'

    @property
    def isLogin(self):
        return self._isLogin

    @property
    def rootDir(self):
        return ftpJoin(self.ftpParams['root-dir'], self._subdir)

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


class FtpAudioManager(FtpManager):
    def __init__(self):
        FtpManager.__init__(self, 'audio')

if __name__ == '__main__':
    AppSettings(AppMode.DEVELOP)
    manager = FtpAudioManager()
    manager.upload(r'C:\1.txt')
