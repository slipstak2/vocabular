# -*- coding: utf-8 -*-

from unit_tests.base.test_base import TestDBBaseClass
from utils import Lang
from models.dict_list_model import DictListModel
from models.word_list_dict_model import WordListDictModel
from models.word_model import WordModel, WordModelUtils
from PySide import QtCore


class TestDict(TestDBBaseClass):
    def setUp(self):
        self.dictListModel = DictListModel()

    def tearDown(self):
        pass

    def testEngWords(self):
        dictListModel = DictListModel(dictIndex=0)
        wordEngListDictModel = WordListDictModel(dictListModel.dictModelProxyViewer, Lang.Eng, Lang.Rus)
        self.assertEqual(2, wordEngListDictModel.rowCount())

        self.assertEqual('exicting', wordEngListDictModel.wordValue(0))
        self.assertEqual(u'захватывающий', wordEngListDictModel.translateValue(0))

        self.assertEqual('retrieval system', wordEngListDictModel.wordValue(1))
        self.assertEqual(u'поисковая система', wordEngListDictModel.translateValue(1))

    def testAddAndRemoveEngWords(self):
        dictListModel = DictListModel(dictIndex=0)
        wordEngListDictModel = WordListDictModel(dictListModel.dictModelProxyViewer, Lang.Eng, Lang.Rus)
        rowCount = wordEngListDictModel.rowCount()

        wordEngModelUtils = WordModelUtils(None, Lang.Eng, Lang.Rus)
        id = wordEngModelUtils.add('new word', '')
        self.assertNotEqual(False, id)
        #TODO: fix tests
        wordEngListDictModel.addWordLink(id)
        self.assertEqual(rowCount + 1, wordEngListDictModel.rowCount())
        wordEngListDictModel.removeLinkWord(id, True)
        self.assertEqual(rowCount, wordEngListDictModel.rowCount())

    def testRusWords(self):
        dictListModel = DictListModel()
        wordRusListDictModel = WordListDictModel(dictListModel.dictModelProxyViewer, Lang.Rus, Lang.Eng)
        self.assertEqual(0, wordRusListDictModel.rowCount())

        wordRusModelUtils= WordModelUtils(None, Lang.Rus, Lang.Eng)
        id = wordRusModelUtils.add(u'новое слово', '')
        self.assertNotEqual(False, id)
        wordRusListDictModel.addWordLink(id)
        self.assertEqual(1, wordRusListDictModel.rowCount())
        wordRusListDictModel.removeLinkWord(id, True)
        self.assertEqual(0, wordRusListDictModel.rowCount())
