# -*- coding: utf-8 -*-

from unit_tests.base.test_base import TestDBBaseClass
from models.dict_list_model import DictListModel


class TestDictModelProxyViewer(TestDBBaseClass):
    def testDefault(self):
        dictListModel = DictListModel()
        dictModelProxyViewer = dictListModel.dictModelProxyViewer
        self.assertEqual(dictListModel, dictModelProxyViewer.parentModel)
        self.assertEqual(1, dictModelProxyViewer.dictId)

    def testChangeDict(self):
        dictListModel = DictListModel()
        dictModelProxyViewer = dictListModel.dictModelProxyViewer
        self.assertEqual(0, dictListModel.dictIndex)
        dictListModel.dictIndex = 1
        self.assertEqual(2, dictModelProxyViewer.dictId)
