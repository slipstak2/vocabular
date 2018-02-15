# -*- coding: utf-8 -*-

from unit_tests.base.test_base import TestDBBaseClass
from utils import Lang
from models.dict_list_model import DictListModel
from models.word_dict_model import WordListDictModel
from models.word_model import WordModel
from PySide import QtCore


class TestDict(TestDBBaseClass):
    def setUp(self):
        self.dictListModel = DictListModel()

    def tearDown(self):
        pass

    def testEngWords(self):
        dictListModel = DictListModel(currentDictIndex=0)
        wordEngListDictModel = WordListDictModel(dictListModel.dictModelProxy, Lang.Eng, Lang.Rus)
        self.assertEqual(2, wordEngListDictModel.rowCount())

        self.assertEqual('exicting', wordEngListDictModel.wordValue(0))
        self.assertEqual(u'захватывающий', wordEngListDictModel.translateValue(0))

        self.assertEqual('retrieval system', wordEngListDictModel.wordValue(1))
        self.assertEqual(u'поисковая система', wordEngListDictModel.translateValue(1))

    def testAddAndRemoveEngWords(self):
        dictListModel = DictListModel(currentDictIndex=0)
        wordEngListDictModel = WordListDictModel(dictListModel.dictModelProxy, Lang.Eng, Lang.Rus)
        rowCount = wordEngListDictModel.rowCount()

        wordModel = WordModel(None, None, Lang.Eng, Lang.Rus)
        id = wordModel.addWord('new word', '')
        self.assertNotEqual(False, id)
        #TODO: fix tests
        wordEngListDictModel.addWord(id)
        self.assertEqual(rowCount + 1, wordEngListDictModel.rowCount())
        wordEngListDictModel.removeLinkWord(id, True)
        self.assertEqual(rowCount, wordEngListDictModel.rowCount())

    def testRusWords(self):
        dictListModel = DictListModel()
        wordRusListDictModel = WordListDictModel(dictListModel.dictModelProxy, Lang.Rus, Lang.Eng)
        self.assertEqual(0, wordRusListDictModel.rowCount())

        wordRusModel = WordModel(None, None, Lang.Rus, Lang.Eng)
        id = wordRusModel.addWord(u'новое слово', '')
        self.assertNotEqual(False, id)
        wordRusListDictModel.addWord(id)
        self.assertEqual(1, wordRusListDictModel.rowCount())
        wordRusListDictModel.removeLinkWord(id, True)
        self.assertEqual(0, wordRusListDictModel.rowCount())
