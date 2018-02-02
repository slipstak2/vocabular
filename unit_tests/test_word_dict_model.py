from unit_tests.base.test_base import TestDBBaseClass
from models.dict_model import DictionaryModel


class TestDict(TestDBBaseClass):
    def setUp(self):
        self.dictModel = DictionaryModel()

    def tearDown(self):
        pass

    def testDefaultWords(self):
        dictModel = DictionaryModel()
