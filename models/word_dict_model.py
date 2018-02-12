# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
from PySide.QtCore import Slot as pyqtSlot

from forms.forms_utils import WordEditMode
from models.base.base_sql_query_model import BaseSqlQueryModel, SqlQuery
from models.base.utils import need_refresh
from models.delegates import EditButtonDelegate, PlayButtonDelegate
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
            self.fields =       ['d_id', 'we_id', 'we_value',  'wr_value', 'play', 'edit']
        else:
            assert dstLang == Lang.Eng, "Currently supported only eng-rus translation"
            self.SRC_LANG_FULL  = 'rus'
            self.SRC_LANG_SHORT = 'r'
            self.DST_LANG_FULL  = 'eng'
            self.DST_LANG_SHORT = 'e'
            self.headerFields = ['',          '',      u'рус',      'eng',     '',     '']
            self.fields =       ['d_id', 'wr_id', 'wr_value',  'we_value', 'play', 'edit']


        self.playFieldNum = self.fields.index('play')
        self.editFieldNum = self.fields.index('edit')


    def wordValue(self, recordIndex):
        return self.record(recordIndex).value(SqlQuery(self, 'w[e]_value').str())

    def translateValue(self, recordIndex):
        return self.record(recordIndex).value(SqlQuery(self, 'w[r]_value').str())

    def dictId(self, recordIndex):
        return self.record(recordIndex).value('d_id')

    def wordId(self, recordIndex):
        return self.record(recordIndex).value(SqlQuery(self, 'w[e]_id').str())

    def refresh(self):
        query = SqlQuery(
            self,
            u'''
            SELECT d_id, w[e]_id, w[e]_value, w[r]_value  FROM (
                SELECT
                    DISTINCT word_[eng].id as w[e]_id, dictionary.id as d_id, word_[eng].value as w[e]_value, word_[rus].value as w[r]_value
                from
                    dictionary
                JOIN word_[eng]_dict ON word_[eng]_dict.dict_id = dictionary.id
                JOIN word_[eng] ON word_[eng].id = word_[eng]_dict.word_[eng]_id
                LEFT JOIN rus_eng ON rus_eng.word_[eng]_id = word_[eng].id
                LEFT JOIN word_[rus] ON word_[rus].id = rus_eng.word_[rus]_id
                WHERE dictionary.id = {dict_id}
                ORDER BY rus_eng.[rus]_order
            ) as x
            GROUP BY d_id, w[e]_id
            '''.format(dict_id=self.dictModel.currentDictId),
        ).str()
        self.setQuery(query)

        for idx, field in enumerate(self.headerFields):
            self.setHeaderData(idx, QtCore.Qt.Horizontal, field)
        self.onRefresh()

    @need_refresh
    def addWord(self, value, meaning=''):
        def _addWord(value, meaning):
            return SqlQuery(
                self,
                'INSERT INTO word_[eng] (id, value, meaning) VALUES (NULL, :value, :meaning)',
                {
                    ':value': value,
                    ':meaning': meaning
                }
            ).execute(True)

        def addWordDictLink(id):
            return SqlQuery(
                self,
                '''
                INSERT INTO
                  word_[eng]_dict
                (dict_id, word_[eng]_id)
                VALUES
                  (:dict_id, :w[e]_id)
                ''',
                {
                    ':dict_id': self.dictModel.currentDictId,
                    ':w[e]_id': id,
                }
            ).execute()

        id = _addWord(value, meaning)
        if id:
            if addWordDictLink(id):
                return id
        return False

    #TODO: удаление ссылки + зависимости в случае с пустым словом. Аналогично и для перевода
    @need_refresh
    def removeWord(self, wordId, silent=False):
        if silent == False:
            msgBox = QtGui.QMessageBox()
            msgBox.setIcon(QtGui.QMessageBox.Question)
            msgBox.setWindowIcon(QtGui.QIcon(":/res/images/dictionary.png"))
            msgBox.setText(u"Вы действительно хотите удалить слово: id = {id}".format(id=wordId))
            msgBox.setWindowTitle(u"Удаление слова")
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            if msgBox.exec_() != QtGui.QMessageBox.Ok:
                return False

        # delete by wordId and dictId from word_eng_dict
        # TODO: проблема висячих ссылок на слова
        return SqlQuery(
            self,
            '''
            DELETE FROM
                word_[eng]_dict
            WHERE
                dict_id = :dict_id AND word_[eng]_id = :word_id
            ''',
            {
                ':dict_id': self.dictModel.currentDictId,
                ':word_id': wordId
            }
        ).execute()

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
        from forms.word_edit_window import WordEditWindow
        print u"edit '{}'".format(self.model.wordValue(recordIndex))
        self.commitData.emit(self.sender())

        wordEditDialog = WordEditWindow(
            self.model.dictId(recordIndex),
            self.model.wordId(recordIndex),
            self.model.wordValue(recordIndex),
            self.model.srcLang,
            self.model.dstLang,
            WordEditMode.Edit
        )
        models_utils.setStartGeometry(self.parentWindow, wordEditDialog)

        wordEditDialog.exec_()
        self.model.refresh()
