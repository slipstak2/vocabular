# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
from PySide.QtCore import Slot as pyqtSlot

from forms.forms_utils import WordEditMode
from models.base.base_sql_query_model import SqlQueryModel, SqlQuery, need_refresh
from models.delegates import EditButtonDelegate, PlayButtonDelegate, RemoveButtonDelegate
from models import models_utils
from models.word_model import WordModel, WordUtils, WordInfo
from utils import Lang


class WordListDictModel(SqlQueryModel):
    @need_refresh
    def __init__(self, dictListModel, srcLang, dstLang, *args, **kwargs):
        super(WordListDictModel, self).__init__(*args, **kwargs)
        self.wordUtils = WordUtils(srcLang=srcLang, dstLang=dstLang)
        self.initLang(srcLang, dstLang)

        self.dictListModel = dictListModel
        if srcLang == Lang.Eng:
            self.headerFields = ['',          '',      'eng',      u'рус',     '',     '',       '']
            self.fields =       ['d_id', 'we_id', 'we_value',  'wr_value', 'play', 'edit', 'remove']
        else:
            self.headerFields = ['',          '',      u'рус',      'eng',     '',     '',       '']
            self.fields =       ['d_id', 'wr_id', 'wr_value',  'we_value', 'play', 'edit', 'remove']

        self.playFieldNum = self.fields.index('play')
        self.editFieldNum = self.fields.index('edit')
        self.removeFieldNum = self.fields.index('remove')

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
                    DISTINCT word_[eng].id as w[e]_id, dict_[eng].id as d_id, word_[eng].value as w[e]_value, word_[rus].value as w[r]_value
                from
                    dict_[eng]
                JOIN word_[eng]_dict ON word_[eng]_dict.dict_[eng]_id = dict_[eng].id
                JOIN word_[eng] ON word_[eng].id = word_[eng]_dict.word_[eng]_id
                LEFT JOIN rus_eng ON rus_eng.word_[eng]_id = word_[eng].id
                LEFT JOIN word_[rus] ON word_[rus].id = rus_eng.word_[rus]_id
                WHERE dict_[eng].id = {dict_id}
                ORDER BY rus_eng.[rus]_order
            ) as x
            GROUP BY d_id, w[e]_id
            '''.format(dict_id=self.dictListModel.dictId),
        ).str()
        self.setQuery(query)

        for idx, field in enumerate(self.headerFields):
            self.setHeaderData(idx, QtCore.Qt.Horizontal, field)
        self.onRefresh()

    @need_refresh
    def addWordLink(self, wordId):
        return SqlQuery(
            self,
            '''
            INSERT INTO
              word_[eng]_dict
            (dict_[eng]_id, word_[eng]_id)
            VALUES
              (:dict_id, :w[e]_id)
            ''',
            {
                ':dict_id': self.dictListModel.dictId,
                ':w[e]_id': wordId,
            }
        ).execute()

    #TODO: удаление ссылки + зависимости в случае с пустым словом. Аналогично и для перевода
    @need_refresh
    def removeLinkWord(self, wordId, silent=False, removeWord=False):
        def removeLink():
            return SqlQuery(
            self,
            '''
            DELETE FROM
                word_[eng]_dict
            WHERE
                dict_[eng]_id = :dict_id AND word_[eng]_id = :word_id
            ''',
            {
                ':dict_id': self.dictListModel.dictId,
                ':word_id': wordId
            }
        ).execute()

        if silent == False:
            msgBox = QtGui.QMessageBox()
            msgBox.setIcon(QtGui.QMessageBox.Question)
            msgBox.setWindowIcon(QtGui.QIcon(":/res/images/dictionary.png"))
            msgBox.setText(u"Вы действительно хотите удалить слово: id = {id}".format(id=wordId))
            msgBox.setWindowTitle(u"Удаление слова")
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            if msgBox.exec_() != QtGui.QMessageBox.Ok:
                return False

        if removeLink():
            if removeWord:
                # TODO: Если слово входит хотя бы в один словарь, то удалять только link
                # TODO: если слово не входит ни в один словарь: спросить - удалить ли слово совсем?
                # TODO: что делать с переводами на это слово?
                self.wordUtils.remove(wordId)

    def data(self, index, role):
        value = super(WordListDictModel, self).data(index, role)
        if role == QtCore.Qt.TextColorRole and index.column() == 2:
            return QtGui.QColor(QtCore.Qt.blue)

        if role == QtCore.Qt.DisplayRole:
            if index.column() in [self.playFieldNum, self.editFieldNum, self.removeFieldNum]:
                return ''

        return value

    def columnCount(self, *args, **kwargs):
        return len(self.fields)


class PlayButtonWordListDictDelegate(PlayButtonDelegate):
    def __init__(self, parentWindow, parent, wordListDictModel):
        PlayButtonDelegate.__init__(self, parentWindow, parent)
        self.wordListDictModel = wordListDictModel


    @pyqtSlot()
    def onBtnClicked(self, recordIndex):
        print u"play '{}'".format(self.wordListDictModel.wordValue(recordIndex))
        self.commitData.emit(self.sender())


class EditButtonWordListDictDelegate(EditButtonDelegate):
    def __init__(self, parentWindow, parent, wordListDictModel):
        EditButtonDelegate.__init__(self, parentWindow, parent)
        self.wordListDictModel = wordListDictModel

    @pyqtSlot()
    def onBtnClicked(self, recordIndex):
        from forms.word_edit_window import WordEditWindow, WordEditContext
        print u"edit '{}'".format(self.wordListDictModel.wordValue(recordIndex))
        self.commitData.emit(self.sender())

        wordInfo = WordInfo(
            self.wordListDictModel.wordId(recordIndex),
            srcLang=self.wordListDictModel.srcLang,
            dstLang=self.wordListDictModel.dstLang
        )

        wordEditDialog = WordEditWindow(
            wordInfo=wordInfo,
            mode=WordEditMode.EditWord,
            wordEditContext=WordEditContext()
        )
        models_utils.setStartGeometry(self.parentWindow, wordEditDialog)

        wordEditDialog.exec_()
        self.wordListDictModel.refresh()


class RemoveButtonWordListDictDelegate(RemoveButtonDelegate):
    def __init__(self, parentWindow, parent, wordListDictModel):
        RemoveButtonDelegate.__init__(self,parentWindow, parent)
        self.wordListDictModel = wordListDictModel

    def onBtnClicked(self, recordIndex):
        print u"remove '{}'".format(self.wordListDictModel.wordValue(recordIndex))
        self.wordListDictModel.removeLinkWord(
            wordId=self.wordListDictModel.wordId(recordIndex),
            removeWord=True
        )
        self.wordListDictModel.refresh()
        self.commitData.emit(self.sender())
