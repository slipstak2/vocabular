# -*- coding: utf-8 -*-

from enum import Enum


#TODO: EditMode -> WordEditMode, DictEditMode
class EditMode(Enum):
    AddNew = 1
    Edit = 2
    AddTranslate = 3



def onBtnEnter(btn, event, **kwargs):
    btn.setFlat(False)


def onBtnLeave(btn, event, **kwargs):
    btn.setFlat(True)

