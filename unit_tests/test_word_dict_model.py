# -*- coding: utf-8 -*-

from unit_tests.base.test_base import TestDBBaseClass
from utils import Lang
from models.dict_list_model import DictListModel
from models.word_dict_model import WordDictModel
from models.word_model import WordModel
from PySide import QtCore


class TestDict(TestDBBaseClass):
    def setUp(self):
        self.dictListModel = DictListModel()

    def tearDown(self):
        pass

    def testEngWords(self):
        dictListModel = DictListModel(currentDictIndex=0)
        wordEngDictModel = WordDictModel(dictListModel.dictModelProxy, Lang.Eng, Lang.Rus)
        self.assertEqual(2, wordEngDictModel.rowCount())

        self.assertEqual('exicting', wordEngDictModel.wordValue(0))
        self.assertEqual(u'захватывающий', wordEngDictModel.translateValue(0))

        self.assertEqual('retrieval system', wordEngDictModel.wordValue(1))
        self.assertEqual(u'поисковая система', wordEngDictModel.translateValue(1))

    def testAddAndRemoveEngWords(self):
        dictListModel = DictListModel(currentDictIndex=0)
        wordEngDictModel = WordDictModel(dictListModel.dictModelProxy, Lang.Eng, Lang.Rus)
        rowCount = wordEngDictModel.rowCount()

        wordModel = WordModel(None, None, Lang.Eng, Lang.Rus)
        id = wordModel.addWord('new word', '')
        self.assertNotEqual(False, id)
        #TODO: fix tests
        wordEngDictModel.addWord(id)
        self.assertEqual(rowCount + 1, wordEngDictModel.rowCount())
        wordEngDictModel.removeLinkWord(id, True)
        self.assertEqual(rowCount, wordEngDictModel.rowCount())

    def testRusWords(self):
        dictListModel = DictListModel()
        wordRusDictModel = WordDictModel(dictListModel.dictModelProxy, Lang.Rus, Lang.Eng)
        self.assertEqual(0, wordRusDictModel.rowCount())

        wordRusModel = WordModel(None, None, Lang.Rus, Lang.Eng)
        id = wordRusModel.addWord(u'новое слово', '')
        self.assertNotEqual(False, id)
        wordRusDictModel.addWord(id)
        self.assertEqual(1, wordRusDictModel.rowCount())
        wordRusDictModel.removeLinkWord(id, True)
        self.assertEqual(0, wordRusDictModel.rowCount())
