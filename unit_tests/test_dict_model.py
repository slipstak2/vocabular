# -*- coding: utf-8 -*-

from unit_tests.base.test_base import TestDBBaseClass
from models.dict_model import DictModel


class TestDictModel(TestDBBaseClass):
    def test1(self):
        dictModel = DictModel(None, 1)
        self.assertEqual(1, dictModel.id)
        self.assertEqual(u'SFML Game Development by example', dictModel.name)
