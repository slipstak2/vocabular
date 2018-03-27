from classes.ftp.ftp_manager import FtpManager


class BaseFile(object):
    def __init__(self, lang, category):
        self._lang = lang
        self._category = category
        self._ftpManager = FtpManager(category)

    @property
    def lang(self):
        return self._lang

    @property
    def category(self):
        return self._category
