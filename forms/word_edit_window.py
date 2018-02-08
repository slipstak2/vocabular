# -*- coding: utf-8 -*-

from PySide import QtGui

from ui.word_edit_ui import Ui_WordAddEdit
from models.word_model import WordModel
from forms_utils import EditMode

from models.word_model import PlayButtonWordTranslateDelegate, EditButtonWordTranslateDelegate, RemoveButtonWordTranslateDelegate

from models import models_utils as models_utils
from utils import Lang

translateTitleMap = {
    EditMode.AddNew: u'Добавление слова',
    EditMode.Edit: u'Редактирование слова',
    EditMode.AddTranslate: u'Добавление перевода',
}

iconTitleMap = {
    EditMode.AddNew:         QtGui.QIcon(":/res/images/add_word.png"),
    EditMode.Edit:           QtGui.QIcon(":/res/images/edit_word.png"),
    EditMode.AddTranslate:   QtGui.QIcon(":/res/images/add_translate.png")
}


class WordEditWindow(QtGui.QDialog):
    def __init__(self, dictId, wordId, wordValue, srcLang, dstLang, mode, *args, **kwargs):
        super(WordEditWindow, self).__init__(*args, **kwargs)

        self.dictId = dictId
        self.mode = mode

        self.wordModel = WordModel(wordId, wordValue, srcLang, dstLang)
        self.srcLang = srcLang
        self.dstLang = dstLang

        self.ui = Ui_WordAddEdit()
        self.ui.setupUi(self)
        self.initUI()
        self.setWindowIcon(iconTitleMap[mode])
