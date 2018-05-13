# -*- coding: utf-8 -*-

from unit_tests.base.test_base import TestDBBaseClass
from utils import Lang
from models.dict_list_model import DictListModel
from models.word_list_dict_model import WordListDictModel
from models.word_model import WordModel, WordUtils


class TestDict(TestDBBaseClass):
    def setUp(self):
        self.dictListModel = DictListModel(Lang.Eng)

    def tearDown(self):
        pass

    def testEngWords(self):
        dictListModel = DictListModel(Lang.Eng, dictIndex=0)
        wordEngListDictModel = WordListDictModel(
            dictListModel,
            Lang.Eng,
            Lang.Rus
        )
        self.assertEqual(2, wordEngListDictModel.rowCount())

        self.assertEqual('exicting', wordEngListDictModel.wordValue(0))
        self.assertEqual(u'захватывающий', wordEngListDictModel.translateValue(0))

        self.assertEqual('retrieval system', wordEngListDictModel.wordValue(1))
        self.assertEqual(u'поисковая система', wordEngListDictModel.translateValue(1))

    def testAddAndRemoveEngWords(self):
        dictListModel = DictListModel(Lang.Eng, dictIndex=0)
        wordEngListDictModel = WordListDictModel(
            dictListModel,
            Lang.Eng,
            Lang.Rus
        )
        rowCount = wordEngListDictModel.rowCount()

        wordEngUtils = WordUtils(Lang.Eng, Lang.Rus)
        id = wordEngUtils.add('new word', '')
        self.assertNotEqual(False, id)
        #TODO: fix tests
        addResult = wordEngListDictModel.addWordLink(id)
        self.assertEqual(rowCount + 1, wordEngListDictModel.rowCount())
        wordEngListDictModel.removeLinkWord(id, True)
        self.assertEqual(rowCount, wordEngListDictModel.rowCount())

    def testRusWords(self):
        dictListModel = DictListModel(Lang.Rus)
        wordRusListDictModel = WordListDictModel(
            dictListModel,
            Lang.Rus,
            Lang.Eng
        )
        self.assertEqual(0, wordRusListDictModel.rowCount())

        wordRusModelUtils= WordUtils(Lang.Rus, Lang.Eng)
        id = wordRusModelUtils.add(u'новое слово', '')
        self.assertNotEqual(False, id)
        wordRusListDictModel.addWordLink(id)
        self.assertEqual(1, wordRusListDictModel.rowCount())
        wordRusListDictModel.removeLinkWord(id, True)
        self.assertEqual(0, wordRusListDictModel.rowCount())
