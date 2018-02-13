# -*- coding: utf-8 -*-

from unit_tests.base.test_base import TestDBBaseClass
from utils import Lang
from models.dict_model import DictionaryListModel
from models.word_dict_model import WordDictModel
from models.word_model import WordModel
from PySide import QtCore


class TestDict(TestDBBaseClass):
    def setUp(self):
        self.dictListModel = DictionaryListModel()

    def tearDown(self):
        pass

    def testEngWords(self):
        dictListModel = DictionaryListModel(currentDictIndex=0)
        wordEngDictModel = WordDictModel(dictListModel, Lang.Eng, Lang.Rus)
        self.assertEqual(2, wordEngDictModel.rowCount())

        self.assertEqual('exicting', wordEngDictModel.wordValue(0))
        self.assertEqual(u'захватывающий', wordEngDictModel.translateValue(0))

        self.assertEqual('retrieval system', wordEngDictModel.wordValue(1))
        self.assertEqual(u'поисковая система', wordEngDictModel.translateValue(1))

    def testAddAndRemoveEngWords(self):
        dictListModel = DictionaryListModel(currentDictIndex=0)
        wordEngDictModel = WordDictModel(dictListModel, Lang.Eng, Lang.Rus)
        rowCount = wordEngDictModel.rowCount()

        wordModel = WordModel(None, Lang.Eng, Lang.Rus)
        id = wordModel.addWord('new word', '')
        self.assertNotEqual(False, id)
        #TODO: fix tests
        wordEngDictModel.addWord(id)
        self.assertEqual(rowCount + 1, wordEngDictModel.rowCount())
        wordEngDictModel.removeLinkWord(id, True)
        self.assertEqual(rowCount, wordEngDictModel.rowCount())

    def testRusWords(self):
        dictListModel = DictionaryListModel()
        wordRusDictModel = WordDictModel(dictListModel, Lang.Rus, Lang.Eng)
        self.assertEqual(0, wordRusDictModel.rowCount())

        wordRusModel = WordModel(None, Lang.Rus, Lang.Eng)
        id = wordRusModel.addWord(u'новое слово', '')
        self.assertNotEqual(False, id)
        wordRusDictModel.addWord(id)
        self.assertEqual(1, wordRusDictModel.rowCount())
        wordRusDictModel.removeLinkWord(id, True)
        self.assertEqual(0, wordRusDictModel.rowCount())
