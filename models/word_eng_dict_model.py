# -*- coding: utf-8 -*-

from PySide import QtSql, QtCore, QtGui
from PySide.QtCore import Slot as pyqtSlot

from forms.word_eng_edit_window import WordEngEditWindow
from forms.utils import EditMode, Lang
from models.base.base_sql_query_model import BaseSqlQueryModel
from models.base.utils import need_refresh
from delegates import ButtonDelegate, EditButtonDelegate, PlayButtonDelegate
from models import utils as models_utils


import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)


class WordEngDictModel(BaseSqlQueryModel):
    headerFields = ['',          '',      'eng',      u'рус',     '',     '']
    fields =       ['d_id', 'we_id', 'we_value',  'we_value', 'play', 'edit']
    playFieldNum = fields.index('play')
    editFieldNum = fields.index('edit')
    tableName = 'dictionary'

    @need_refresh
    def __init__(self, dictModel, *args, **kwargs):
        super(WordEngDictModel, self).__init__(*args, **kwargs)
        self.dictModel = dictModel

    def wordEngValue(self, recordIndex):
        return self.record(recordIndex).value('we_value')

    def dictId(self, recordIndex):
        return self.record(recordIndex).value('d_id')

    def wordEngId(self, recordIndex):
        return self.record(recordIndex).value('we_id')

    def refresh(self):
        self.setQuery('''
        SELECT d_id, we_id, we_value, wr_value  FROM (
            SELECT
                DISTINCT we.id as we_id, d.id as d_id, we.value as we_value, wr.value as wr_value
            from
                dictionary as d
            JOIN word_eng_dict as wed ON wed.dict_id = d.id
            JOIN word_eng as we ON we.id = wed.word_eng_id
            JOIN rus_eng as re ON re.word_eng_id = we.id
            JOIN word_rus as wr ON wr.id = re.word_rus_id
            WHERE d.id = {dictId}
            ORDER BY re.rus_order
        ) as x
        GROUP BY d_id, we_id
        '''.format(dictId=self.dictModel.currentDictId)) #TODO: bindValue

        for idx, field in enumerate(WordEngDictModel.headerFields):
            self.setHeaderData(idx, QtCore.Qt.Horizontal, field)

        self.onRefresh()

    def data(self, index, role):
        value = super(WordEngDictModel, self).data(index, role)
        if role == QtCore.Qt.TextColorRole and index.column() == 2:
            return QtGui.QColor(QtCore.Qt.blue)

        if role == QtCore.Qt.DisplayRole:
            if index.column() in [WordEngDictModel.playFieldNum, WordEngDictModel.editFieldNum]:
                return ''

        return value

    def columnCount(self, *args, **kwargs):
        return len(WordEngDictModel.fields)


class PlayButtonWordEngDictDelegate(PlayButtonDelegate):
    def __init__(self, parentWindow, parent, model):
        PlayButtonDelegate.__init__(self, parentWindow, parent, model)

    @pyqtSlot()
    def onBtnClicked(self, recordIndex):
        print "play '{}'".format(self.model.wordEngValue(recordIndex))
        self.commitData.emit(self.sender())


class EditButtonWordEngDictDelegate(EditButtonDelegate):
    def __init__(self, parentWindow, parent, model):
        EditButtonDelegate.__init__(self, parentWindow, parent, model)

    @pyqtSlot()
    def onBtnClicked(self, recordIndex):
        print "edit '{}'".format(self.model.wordEngValue(recordIndex))
        self.commitData.emit(self.sender())

        #TODO: появление окошек лесенкой, чтобы можно проследить историю глубины
        wordDialog = WordEngEditWindow(
            self.model.dictId(recordIndex),
            self.model.wordEngId(recordIndex),
            self.model.wordEngValue(recordIndex),
            Lang.Eng,
            EditMode.Edit
        )
        models_utils.setStartGeometry(self.parentWindow, wordDialog)

        wordDialog.exec_()
        print wordDialog.geometry()

        self.model.refresh()
