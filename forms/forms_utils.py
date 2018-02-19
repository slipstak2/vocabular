# -*- coding: utf-8 -*-

from enum import Enum


class DictEditMode(Enum):
    Add = 1
    Edit = 2


class WordEditMode(Enum):
    AddNew = 1
    Edit = 2
    AddTranslate = 3
    EditTranslate = 4


def onBtnEnter(btn, event, **kwargs):
    btn.setFlat(False)


def onBtnLeave(btn, event, **kwargs):
    btn.setFlat(True)
