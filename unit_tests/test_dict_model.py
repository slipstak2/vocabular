from unit_tests.base.test_base import TestDBBaseClass
from models.dict_model import DictionaryModel


class TestDict(TestDBBaseClass):
    def setUp(self):
        self.dictModel = DictionaryModel()

    def tearDown(self):
        pass

    def testDefaultDict(self):
        dictModel = DictionaryModel()
        self.assertEqual(1, dictModel.currentDictId)
        self.assertEqual(0, dictModel.currentDictIndex)
        self.assertEqual(u'SFML Game Development by example', dictModel.currentDictName)

    def testFirstDict(self):
        dictModel = DictionaryModel(1)
        self.assertEqual(2, dictModel.currentDictId)
        self.assertEqual(1, dictModel.currentDictIndex)
        self.assertEqual(u'Effective Modern C++, 2014', dictModel.currentDictName)

    def testSwitchDict(self):
        dictModel = DictionaryModel(0)
        self.assertEqual(1, dictModel.currentDictId)
        dictModel.currentDictIndex = 1
        self.assertEqual(2, dictModel.currentDictId)

    def testViewField(self):
        self.assertEqual(0, self.dictModel.viewFieldIndex())

    def testFieldIndex(self):
        self.assertEqual(1, self.dictModel.fieldIndex('date_create'))

    def testAddEditRemoveDict(self):
        dictModel = DictionaryModel()
        rowCount = dictModel.rowCount()

        # add dict
        dictName = 'new dict'
        self.assertTrue(dictModel.addDict(dictName))
        self.assertEqual(rowCount + 1, dictModel.rowCount())

        # edit dict
        dictModel.currentDictIndex = dictModel.rowCount() - 1
        dictId = dictModel.currentDictId
        newDictName = dictName + ' update'
        dictModel.editDict(dictId, newDictName)
        self.assertEqual(newDictName, dictModel.currentDictName)

        # remove dict
        dictModel.removeDict()
        self.assertEqual(rowCount, dictModel.rowCount())
