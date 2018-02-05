# -*- coding: utf-8 -*-

from unit_tests.base.test_base import TestDBBaseClass
from utils import Lang
from models.dict_model import DictionaryModel
from models.word_dict_model import WordDictModel
from PySide import QtCore


class TestDict(TestDBBaseClass):
    def setUp(self):
        self.dictModel = DictionaryModel()

    def tearDown(self):
        pass

    def testDefaultWords(self):
        dictModel = DictionaryModel(currentDictIndex=0)
        wordEngModel = WordDictModel(dictModel, Lang.Eng, Lang.Rus)
        self.assertEqual(2, wordEngModel.rowCount())

        self.assertEqual('exicting', wordEngModel.wordValue(0))
        self.assertEqual('retrieval system', wordEngModel.wordValue(1))

        #self.assertEqual('захватывающий', wordEngModel.record(0).value('wr_value'))
