# -*- coding: utf-8 -*-

from unit_tests.base.test_base import TestBaseClass
from PySide.QtGui import QRegExpValidator, QValidator
from PySide.QtCore import QRegExp
import utils


class TestEngLangValidator(TestBaseClass):
    def setUp(self):
        self.validator = QRegExpValidator(QRegExp(utils.rxEng), None)

    def _check(self, s1, targetState):
        expectedState, s2, pos = self.validator.validate(s1, 0)
        self.assertEqual((s1, targetState), (s1, expectedState))

    def testAcceptable(self):
        for word in ['abc', 'Abc DfZ', '123', 'vasia Petr', 'Salt-Shed rin']:
            self._check(word, QValidator.State.Acceptable)

    def testInvalid(self):
        for word in ['aз', 'Буки', 'Веди гл-а-голь', 'Вedi']:
            self._check(word, QValidator.State.Invalid)


class TestRusLangValidator(TestBaseClass):
    def setUp(self):
        self.validator = QRegExpValidator(QRegExp(utils.rxRus), None)

    def _check(self, s1, targetState):
        expectedState, s2, pos = self.validator.validate(s1, 0)
        self.assertEqual((s1, targetState), (s1, expectedState))

    def testAcceptable(self):
        for word in [u'аз', u'Буки', '123', u'Веди гл-а-голь']:
            self._check(word, QValidator.State.Acceptable)

    def testInvalid(self):
        for word in ['abc', 'Abc DfZ', 'vasia Petr', 'Salt-Shed rin', 'Вedi']:
            self._check(word, QValidator.State.Invalid)
