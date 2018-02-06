# -*- coding: utf-8 -*-

from PySide import QtSql, QtCore, QtGui
from PySide.QtCore import Slot as pyqtSlot
from models.base.utils import need_refresh
from models.base.base_sql_query_model import BaseSqlQueryModel
from models.delegates import EditButtonDelegate, PlayButtonDelegate, RemoveButtonDelegate

class WordModel(BaseSqlQueryModel):
    @need_refresh
    def __init__(self, wordId, wordValue, srcLang, dstLang, *args, **kwargs):
        super(WordModel, self).__init__(*args, **kwargs)
        self.wordId = wordId
        self.wordValue = wordValue
        self.srcLang = srcLang
        self.dstLang = dstLang
