# -*- coding: utf-8 -*-

from unit_tests.base.test_base import TestDBBaseClass
from utils import Lang
from models.word_model import WordModel


class TestWord(TestDBBaseClass):
    def setUp(self):
        self.wordEngModel = WordModel(None, 1, Lang.Eng, Lang.Rus) # 'exciting'

    def tearDown(self):
        pass

    def testAddAndRemove(self):
        value = 'value'
        meaning = 'meaining'
        id = self.wordEngModel.addWord(value, meaning)
        self.assertNotEqual(False, id)

        wordModel = WordModel(None, id, self.wordEngModel.srcLang, self.wordEngModel.dstLang);
        self.assertEqual(value, wordModel.wordValue)
        self.assertEqual(meaning, wordModel.wordMeaning)

        self.assertTrue(wordModel.remove())

    def testUpdate(self):
        def check(value, meaning):
            self.assertEqual(value, self.wordEngModel.wordValue)
            self.assertEqual(meaning, self.wordEngModel.wordMeaning)

        init = ('exicting', '')
        check(*init)
        upd = ('new exicting', 'new meaning')
        self.wordEngModel.update(*upd)
        check(*upd)
        self.wordEngModel.update(*init)
        check(*init)
