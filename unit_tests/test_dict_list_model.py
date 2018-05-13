# -*- coding: utf-8 -*-

from unit_tests.base.test_base import TestDBBaseClass
from models.dict_list_model import DictListModel
from utils import Lang


class TestDictListModel(TestDBBaseClass):
    def setUp(self):
        self.dictListModel = DictListModel(Lang.Eng)

    def tearDown(self):
        pass

    def testDefaultDict(self):
        dictListModel = DictListModel(Lang.Eng)
        self.assertEqual(1, dictListModel.dictId)
        self.assertEqual(0, dictListModel.dictIndex)
        self.assertEqual(u'SFML Game Development by example', dictListModel.dictName)

    def testFirstDict(self):
        dictListModel = DictListModel(Lang.Eng, 1)
        self.assertEqual(2, dictListModel.dictId)
        self.assertEqual(1, dictListModel.dictIndex)
        self.assertEqual(u'Effective Modern C++, 2014', dictListModel.dictName)

    def testSwitchDict(self):
        dictListModel = DictListModel(Lang.Eng, 0)
        self.assertEqual(1, dictListModel.dictId)
        dictListModel.dictIndex = 1
        self.assertEqual(2, dictListModel.dictId)

    def testFieldIndex(self):
        self.assertEqual(1, self.dictListModel.fieldIndex('date_create'))

    def testAddEditRemoveDict(self):
        dictListModel = DictListModel(Lang.Eng)
        rowCount = dictListModel.rowCount()

        # add dict
        dictName = 'new dict'
        dictId = dictListModel.dictUtils.add(dictName)
        self.assertNotEqual(False, dictId)
        dictListModel.refresh()
        self.assertEqual(rowCount + 1, dictListModel.rowCount())

        # edit dict
        dictListModel.dictIndex = dictListModel.rowCount() - 1
        newDictName = dictName + ' update'
        self.assertTrue(dictListModel.dictUtils.edit(dictId, newDictName))
        dictListModel.refresh()
        self.assertEqual(newDictName, dictListModel.dictName)

        # remove dict
        dictListModel.removeDict()
        self.assertEqual(rowCount, dictListModel.rowCount())
