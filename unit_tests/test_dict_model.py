# -*- coding: utf-8 -*-

from unit_tests.base.test_base import TestDBBaseClass
from models.dict_list_model import DictListModel


class TestDict(TestDBBaseClass):
    def setUp(self):
        self.dictListModel = DictListModel()

    def tearDown(self):
        pass

    def testDefaultDict(self):
        dictListModel = DictListModel()
        self.assertEqual(1, dictListModel.dictId)
        self.assertEqual(0, dictListModel.dictIndex)
        self.assertEqual(u'SFML Game Development by example', dictListModel.dictName)

    def testFirstDict(self):
        dictListModel = DictListModel(1)
        self.assertEqual(2, dictListModel.dictId)
        self.assertEqual(1, dictListModel.dictIndex)
        self.assertEqual(u'Effective Modern C++, 2014', dictListModel.dictName)

    def testSwitchDict(self):
        dictListModel = DictListModel(0)
        self.assertEqual(1, dictListModel.dictId)
        dictListModel.dictIndex = 1
        self.assertEqual(2, dictListModel.dictId)

    def testViewField(self):
        self.assertEqual(0, self.dictListModel.viewFieldIndex())

    def testFieldIndex(self):
        self.assertEqual(1, self.dictListModel.fieldIndex('date_create'))

    def testAddEditRemoveDict(self):
        dictListModel = DictListModel()
        rowCount = dictListModel.rowCount()

        # add dict
        dictName = 'new dict'
        self.assertTrue(dictListModel.addDict(dictName))
        self.assertEqual(rowCount + 1, dictListModel.rowCount())

        # edit dict
        dictListModel.dictIndex = dictListModel.rowCount() - 1
        dictId = dictListModel.dictId
        newDictName = dictName + ' update'
        self.assertTrue(dictListModel.dictModelUtils.edit(dictId, newDictName))
        self.assertEqual(newDictName, dictListModel.dictName)

        # remove dict
        dictListModel.removeDict()
        self.assertEqual(rowCount, dictListModel.rowCount())
