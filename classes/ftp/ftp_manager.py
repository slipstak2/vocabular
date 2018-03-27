# -*- coding: utf-8 -*-

# https://python-scripts.com/ftplib

import os
from ftplib import FTP, all_errors
from app_settings import AppSettings, AppMode


class FtpSaveCwd_WithNewCwd(object):
    def __init__(self, ftp, newCwd):
        self.ftp = ftp
        self.pwd = self.ftp.pwd()
        self.ftp.cwd(newCwd)

    def __enter__(self):
        return self.ftp

    def __exit__(self, *args):
        self.ftp.cwd(self.pwd)


class FtpSaveCwd(object):
    def __init__(self, ftp):
        self.ftp = ftp
        self.pwd = self.ftp.pwd()

    def __enter__(self):
        return self.ftp

    def __exit__(self, *args):
        self.ftp.cwd(self.pwd)


def ftpPathNorm(ftpPath):
    if not ftpPath:
        return '/'
    if ftpPath == '/':
        return ftpPath

    if ftpPath[0] != '/':
        ftpPath = '/{}'.format(ftpPath)

    ftpPath = ftpPath.replace('//', '/')

    if ftpPath[-1] == '/':
        ftpPath = ftpPath[:-1]

    return ftpPath


def ftpJoin(root, dir):
    result = '/{}/{}'.format(ftpPathNorm(root), dir)
    return ftpPathNorm(result)


class FtpManager(object):
    def __init__(self, category=''):
        self._category = category
        self.ftpParams = AppSettings().ftpParams
        self.ftp = FTP(self.ftpParams['host'])
        self.login()
        self.garanteeExistPath(self.rootDir)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.ftp.close()

    def login(self):
        self._loginInfo = self.ftp.login(self.ftpParams['user'], self.ftpParams['passwd'])
        self._isLogin = self._loginInfo == '230 Login successful.'

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

    def garanteeExistPath(self, ftpPath):
        self.ftp.cwd('/')
        curPath = ''
        for part in ftpPath.split('/'):
            if curPath == '/':
                curPath += part
            else:
                curPath += '/' + part
            if curPath == '/':
                self.ftp.cwd(curPath)
            else:
                files = self.ftp.nlst()
                if part in files:
                    self.ftp.cwd(curPath)
                else:
                    self.ftp.mkd(curPath)

    @property
    def isLogin(self):
        return self._isLogin

    @property
    def ftpRoot(self):
        return ftpPathNorm(self.ftpParams['root-dir'])

    @property
    def rootDir(self):
        return ftpJoin(self.ftpRoot, self._category)

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
