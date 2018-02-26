# -*- coding: utf-8 -*-

from unit_tests.base.test_base import TestDBBaseClass
from utils import Lang
from models.word_model import WordModel, WordModelUtils


class TestWord(TestDBBaseClass):
    def setUp(self):
        self.wordEngModel = WordModel(1, Lang.Eng, Lang.Rus) # 'exciting'
        self.wordEngModelUtils = WordModelUtils(Lang.Eng, Lang.Rus)

    def tearDown(self):
        pass

    def testAddAndRemove(self):
        value = 'value'
        meaning = 'meaining'
        id = self.wordEngModelUtils.add(value, meaning)
        self.assertNotEqual(False, id)

        wordModel = WordModel(id, self.wordEngModel.srcLang, self.wordEngModel.dstLang);
        self.assertEqual(value, wordModel.wordValue)
        self.assertEqual(meaning, wordModel.wordMeaning)

        self.assertTrue(self.wordEngModelUtils.remove(id))

    def testUpdate(self):
        def check(value, meaning):
            self.assertEqual(value, self.wordEngModel.wordValue)
            self.assertEqual(meaning, self.wordEngModel.wordMeaning)

        init = ('exicting', '')
        check(*init)
        upd = ('new exicting', 'new meaning')
        self.wordEngModelUtils.edit(wordId=1, value=upd[0], meaning=upd[1])
        self.wordEngModel.refresh()
        check(*upd)
        self.wordEngModelUtils.edit(wordId=1, value=init[0], meaning=init[1])
        self.wordEngModel.refresh()
        check(*init)
