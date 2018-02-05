# -*- coding: utf-8 -*-

from enum import Enum

from PySide import QtGui
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


def qtRus(text):
    return _translate(u'emptyContext', text, None)


#TODO: EditMode -> WordEditMode, DictEditMode
class EditMode(Enum):
    AddNew = 1
    Edit = 2
    AddTranslate = 3



def onBtnEnter(btn, event, **kwargs):
    btn.setFlat(False)


def onBtnLeave(btn, event, **kwargs):
    btn.setFlat(True)

