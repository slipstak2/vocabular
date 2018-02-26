# -*- coding: utf-8 -*-

from unit_tests.base.test_base import TestDBBaseClass
from utils import Lang
from models.word_translate_model import WordTranslateModel


class TestWordTranslate(TestDBBaseClass):
    def setUp(self):
        self.wordEngTranlsateModel = WordTranslateModel(1, Lang.Eng, Lang.Rus) # 'exciting'
        self.translates = [u'захватывающий', u'восхитительный', u'еще одно слово']

    def tearDown(self):
        pass

    def testTranslates(self):
        self.assertEqual(3, self.wordEngTranlsateModel.rowCount())
        for idx, translate in enumerate(self.translates):
            self.assertEqual(translate, self.wordEngTranlsateModel.wordTranslate(idx))

    def testUpOrder(self):
        self.wordEngTranlsateModel.upOrder(1)
        self.assertEqual(self.translates[0], self.wordEngTranlsateModel.wordTranslate(1))
        self.assertEqual(self.translates[1], self.wordEngTranlsateModel.wordTranslate(0))
        self.wordEngTranlsateModel.upOrder(1)
        self.assertEqual(self.translates[0], self.wordEngTranlsateModel.wordTranslate(0))
        self.assertEqual(self.translates[1], self.wordEngTranlsateModel.wordTranslate(1))

    def testDownOrder(self):
        self.wordEngTranlsateModel.downOrder(0)
        self.assertEqual(self.translates[0], self.wordEngTranlsateModel.wordTranslate(1))
        self.assertEqual(self.translates[1], self.wordEngTranlsateModel.wordTranslate(0))
        self.wordEngTranlsateModel.downOrder(0)
        self.assertEqual(self.translates[0], self.wordEngTranlsateModel.wordTranslate(0))
        self.assertEqual(self.translates[1], self.wordEngTranlsateModel.wordTranslate(1))

    def testAddEmptyTranslateAndRemoveIt(self):
        rowCount = self.wordEngTranlsateModel.rowCount()
        translateId = self.wordEngTranlsateModel.addEmptyTranslate()
        self.assertNotEqual(False, translateId)
        self.assertEqual(rowCount + 1, self.wordEngTranlsateModel.rowCount())
        self.assertTrue(self.wordEngTranlsateModel.removeTranslate(translateId, silent=True))
        self.assertEqual(rowCount, self.wordEngTranlsateModel.rowCount())

