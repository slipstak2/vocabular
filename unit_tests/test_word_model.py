# -*- coding: utf-8 -*-

from unit_tests.base.test_base import TestDBBaseClass
from utils import Lang
from models.dict_model import DictionaryModel
from models.word_dict_model import WordDictModel
from PySide import QtCore
from models.word_model import WordModel


class TestWord(TestDBBaseClass):
    def setUp(self):
        self.wordEngModel = WordModel(1, 'exciting', Lang.Eng, Lang.Rus)
        self.translates = [u'захватывающий', u'восхитительный', u'еще одно слово']

    def tearDown(self):
        pass

    def testTranslates(self):
        self.assertEqual(3, self.wordEngModel.rowCount())
        for idx, translate in enumerate(self.translates):
            self.assertEqual(translate, self.wordEngModel.wordTranslate(idx))

    def testUpOrder(self):
        self.wordEngModel.upOrder(1)
        self.assertEqual(self.translates[0], self.wordEngModel.wordTranslate(1))
        self.assertEqual(self.translates[1], self.wordEngModel.wordTranslate(0))
        self.wordEngModel.upOrder(1)
        self.assertEqual(self.translates[0], self.wordEngModel.wordTranslate(0))
        self.assertEqual(self.translates[1], self.wordEngModel.wordTranslate(1))

    def testDownOrder(self):
        self.wordEngModel.downOrder(0)
        self.assertEqual(self.translates[0], self.wordEngModel.wordTranslate(1))
        self.assertEqual(self.translates[1], self.wordEngModel.wordTranslate(0))
        self.wordEngModel.downOrder(0)
        self.assertEqual(self.translates[0], self.wordEngModel.wordTranslate(0))
        self.assertEqual(self.translates[1], self.wordEngModel.wordTranslate(1))

    def testAddEmptyTranslateAndRemoveIt(self):
        rowCount = self.wordEngModel.rowCount()
        translateId = self.wordEngModel.addEmptyTranslate()
        self.assertNotEqual(False, translateId)
        self.assertEqual(rowCount + 1, self.wordEngModel.rowCount())
        self.assertTrue(self.wordEngModel.removeTranslate(translateId, silent=True))
        self.assertEqual(rowCount, self.wordEngModel.rowCount())

