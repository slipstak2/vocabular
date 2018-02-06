# -*- coding: utf-8 -*-

from PySide import QtSql, QtCore
from PySide.QtCore import Slot as pyqtSlot
from models.base.utils import need_refresh
from models.base.base_sql_query_model import BaseSqlQueryModel
from models.delegates import EditButtonDelegate, PlayButtonDelegate, RemoveButtonDelegate
from models.word_model import WordModel
from utils import Lang


#TODO: объединить word_eng_model and word_rus_model
class WordRusModel(WordModel):
    headerFields = [     '', u'перевод',             '',   u'значение',     '',     '',       '']
    fields =       ['we_id', 'we_value', 're_eng_order',  'we_meaning', 'play', 'edit', 'remove']
    playFieldNum = fields.index('play')
    editFieldNum = fields.index('edit')
    removeFieldNum = fields.index('remove')

    def __init__(self, wordId, wordValue):
        super(WordRusModel, self).__init__(wordId, wordValue, Lang.Rus, Lang.Eng)

    def wordEngTranslate(self, recordIndex):
        return self.record(recordIndex).value('wr_value')

    def refresh(self):
        self.setQuery('''
        SELECT
            we.id as we_id, we.value as we_value, re.eng_order as re_eng_order, we.meaning as we_meaning
        FROM
            word_rus as wr
        JOIN rus_eng as re ON re.word_rus_id = wr.id
        JOIN word_eng as we ON we.id = re.word_eng_id

        WHERE wr.id = {wrId}
        ORDER BY re.eng_order ASC
        '''.format(wrId=self.wordId)) #TODO: bindValue

        for idx, field in enumerate(WordRusModel.headerFields):
            self.setHeaderData(idx, QtCore.Qt.Horizontal, field)

        self.onRefresh()

    def data(self, index, role):
        value = super(WordRusModel, self).data(index, role)

        if role == QtCore.Qt.DisplayRole:
            if index.column() in [WordRusModel.playFieldNum, WordRusModel.editFieldNum, WordRusModel.removeFieldNum]:
                return ''

        return value

    def changeOrder(self, row1, row2):
        query = QtSql.QSqlQuery()
        query.prepare(
            '''
            INSERT INTO
              rus_eng
              (word_eng_id, word_rus_id, eng_order)
            VALUES
              (:we_id1, :wr_id1, :eo1),(:we_id2, :wr_id2, :eo2)
            ON DUPLICATE KEY UPDATE rus_order=VALUES(rus_order)
            '''
        )

        query.bindValue(u":we_id1", self.record(row1).value('we_id'))
        query.bindValue(u":we_id2", self.record(row2).value('we_id'))
        query.bindValue(u":eo1", self.record(row2).value('re_eng_order'))
        query.bindValue(u":eo2", self.record(row1).value('re_eng_order'))
        query.bindValue(u":wr_id1", self.wordId)
        query.bindValue(u":wr_id2", self.wordId)

        try:
            query.exec_()
            self.db.commit()
            r = query.result()
            print u'change order: OK'
            return True
        except BaseException as ex:
            print ex
            self.db.rollback()
            return False

    @need_refresh
    def downOrder(self, row):
        self.changeOrder(row, row + 1)

    @need_refresh
    def upOrder(self, row):
        self.changeOrder(row, row - 1)

    def columnCount(self, *args, **kwargs):
        return len(WordRusModel.fields)


class PlayButtonWordRusTranslateDelegate(PlayButtonDelegate):
    def __init__(self, parent, model):
        PlayButtonDelegate.__init__(self, parent, model)

    @pyqtSlot()
    def onBtnClicked(self, recordIndex):
        print u"play '{}'".format(self.model.wordEngTranslate(recordIndex))
        self.commitData.emit(self.sender())


class EditButtonWordRusTranslateDelegate(EditButtonDelegate):
    def __init__(self, parent, model):
        EditButtonDelegate.__init__(self, parent, model)

    @pyqtSlot()
    def onBtnClicked(self, recordIndex):
        print u"edit '{}'".format(self.model.wordEngTranslate(recordIndex))
        self.commitData.emit(self.sender())


class RemoveButtonRusEngTranslateDelegate(RemoveButtonDelegate):
    def __init__(self, parent, model):
        RemoveButtonDelegate.__init__(self, parent, model)

    @pyqtSlot()
    def onBtnClicked(self, recordIndex):
        print u"remove '{}'".format(self.model.wordEngTranslate(recordIndex))
        self.commitData.emit(self.sender())
