# -*- coding: utf-8 -*-

# https://python-scripts.com/ftplib

from ftplib import FTP
from app_settings import AppSettings, AppMode


class FtpManager(object):
    def __init__(self):
        params = AppSettings().ftpParams
        self.ftp = FTP(params['host'])
        print(self.ftp.login(params['user'], params['passwd']))

        print(self.ftp.retrlines('LIST'))
        self.ftp.cwd(params['root-dir'])
        print(self.ftp.retrlines('LIST'))

        print(self.ftp.nlst())


    def checkExist(self, ftpPath):
        pass


    def upload(self, localPath, ftype='TXT'):
        if ftype == 'TXT':
            with open(localPath) as f:
                self.ftp.storlines('STOR ' + localPath, f)
        else:
            with open(localPath, 'rb') as f:
                self.ftp.storbinary('STOR ' + localPath, f, 1024)

if __name__ == '__main__':
    AppSettings(AppMode.DEVELOP)
    manager = FtpManager()
    manager.upload(r'C:\1.txt')
