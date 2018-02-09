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

    def testEngWords(self):
        dictModel = DictionaryModel(currentDictIndex=0)
        wordEngDictModel = WordDictModel(dictModel, Lang.Eng, Lang.Rus)
        self.assertEqual(2, wordEngDictModel.rowCount())

        self.assertEqual('exicting', wordEngDictModel.wordValue(0))
        self.assertEqual(u'захватывающий', wordEngDictModel.translateValue(0))

        self.assertEqual('retrieval system', wordEngDictModel.wordValue(1))
        self.assertEqual(u'поисковая система', wordEngDictModel.translateValue(1))

        #TODO: добавить новое слово
        #TODO: удалить новое слово

    def testRusWords(self):
        dictModel = DictionaryModel()
        wordRusDictModel = WordDictModel(dictModel, Lang.Rus, Lang.Eng)
        self.assertEqual(0, wordRusDictModel.rowCount())

        #TODO: добавить новое слово
        #TODO: удалить это слово


