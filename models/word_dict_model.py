# -*- coding: utf-8 -*-

from PySide import QtSql, QtCore, QtGui
from PySide.QtCore import Slot as pyqtSlot

from forms.forms_utils import EditMode
from models.base.base_sql_query_model import BaseSqlQueryModel
from models.base.utils import need_refresh
from models.delegates import ButtonDelegate, EditButtonDelegate, PlayButtonDelegate
from models import models_utils as models_utils
from utils import Lang


class WordDictModel(BaseSqlQueryModel):
    @need_refresh
    def __init__(self, dictModel, srcLang, dstLang, *args, **kwargs):
        super(WordDictModel, self).__init__(*args, **kwargs)
        self.dictModel = dictModel
        self.srcLang = srcLang
        self.dstLang = dstLang
        if srcLang == Lang.Eng:
            assert dstLang == Lang.Rus, "Currently supported only eng-rus translation"
            self.SRC_LANG_FULL  = 'eng'
            self.SRC_LANG_SHORT = 'e'
            self.DST_LANG_FULL  = 'rus'
            self.DST_LANG_SHORT = 'r'
            self.headerFields = ['',          '',      'eng',      u'рус',     '',     '']
            self.fields =       ['d_id', 'we_id', 'we_value',  'we_value', 'play', 'edit']
        else:
            assert dstLang == Lang.Eng, "Currently supported only eng-rus translation"
            self.SRC_LANG_FULL  = 'rus'
            self.SRC_LANG_SHORT = 'r'
            self.DST_LANG_FULL  = 'eng'
            self.DST_LANG_SHORT = 'e'

        self.playFieldNum = self.fields.index('play')
        self.editFieldNum = self.fields.index('edit')


    def wordValue(self, recordIndex):
        return self.record(recordIndex).value('w{e}_value'.format(e=self.SRC_LANG_SHORT))

    def dictId(self, recordIndex):
        return self.record(recordIndex).value('d_id')

    def wordId(self, recordIndex):
        return self.record(recordIndex).value('w{e}_id'.format(e=self.SRC_LANG_SHORT))

    def refresh(self):
        query = u'''
        SELECT d_id, w{e}_id, w{e}_value, w{r}_value  FROM (
            SELECT
                DISTINCT word_{eng}.id as w{e}_id, dictionary.id as d_id, word_{eng}.value as w{e}_value, word_{rus}.value as w{r}_value
            from
                dictionary
            JOIN word_{eng}_dict ON word_{eng}_dict.dict_id = dictionary.id
            JOIN word_{eng} ON word_{eng}.id = word_{eng}_dict.word_{eng}_id
            JOIN rus_eng ON rus_eng.word_{eng}_id = word_{eng}.id
            JOIN word_{rus} ON word_{rus}.id = rus_eng.word_{rus}_id
            WHERE dictionary.id = {dict_id}
            ORDER BY rus_eng.{rus}_order
        ) as x
        GROUP BY d_id, w{e}_id
        '''.format(
            eng=self.SRC_LANG_FULL,
            e=self.SRC_LANG_SHORT,
            rus=self.DST_LANG_FULL,
            r=self.DST_LANG_SHORT,
            dict_id=self.dictModel.currentDictId
        )
        self.setQuery(query)

        for idx, field in enumerate(self.headerFields):
            self.setHeaderData(idx, QtCore.Qt.Horizontal, field)
        self.onRefresh()

    def data(self, index, role):
        value = super(WordDictModel, self).data(index, role)
        if role == QtCore.Qt.TextColorRole and index.column() == 2:
            return QtGui.QColor(QtCore.Qt.blue)

        if role == QtCore.Qt.DisplayRole:
            if index.column() in [self.playFieldNum, self.editFieldNum]:
                return ''

        return value

    def columnCount(self, *args, **kwargs):
        return len(self.fields)


class PlayButtonWordDictDelegate(PlayButtonDelegate):
    def __init__(self, parentWindow, parent, model):
        PlayButtonDelegate.__init__(self, parentWindow, parent, model)

    @pyqtSlot()
    def onBtnClicked(self, recordIndex):
        print u"play '{}'".format(self.model.wordValue(recordIndex))
        self.commitData.emit(self.sender())


class EditButtonWordDictDelegate(EditButtonDelegate):
    def __init__(self, parentWindow, parent, model):
        EditButtonDelegate.__init__(self, parentWindow, parent, model)

    @pyqtSlot()
    def onBtnClicked(self, recordIndex):
        from forms.word_eng_edit_window import WordEngEditWindow
        print u"edit '{}'".format(self.model.wordValue(recordIndex))
        self.commitData.emit(self.sender())

        #TODO: появление окошек лесенкой, чтобы можно проследить историю глубины
        wordDialog = WordEngEditWindow(
            self.model.dictId(recordIndex),
            self.model.wordId(recordIndex),
            self.model.wordValue(recordIndex),
            Lang.Eng,
            EditMode.Edit
        )
        models_utils.setStartGeometry(self.parentWindow, wordDialog)

        wordDialog.exec_()
        self.model.refresh()
