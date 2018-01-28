# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\YandexDisk\Vocabular\ui\word_edit.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!


try:
    from PySide import QtCore, QtGui
except ImportError:
    from PyQt4 import QtCore, QtGui


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_WordAddEdit(object):
    def setupUi(self, WordAddEdit):
        WordAddEdit.setObjectName(_fromUtf8("WordAddEdit"))
        WordAddEdit.setWindowModality(QtCore.Qt.NonModal)
        WordAddEdit.resize(411, 453)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WordAddEdit.sizePolicy().hasHeightForWidth())
        WordAddEdit.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/images/dictionary.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        WordAddEdit.setWindowIcon(icon)
        WordAddEdit.setModal(False)
        self.gridLayout = QtGui.QGridLayout(WordAddEdit)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.leWord = QtGui.QLineEdit(WordAddEdit)
        self.leWord.setObjectName(_fromUtf8("leWord"))
        self.gridLayout_2.addWidget(self.leWord, 0, 2, 1, 1)
        self.label_2 = QtGui.QLabel(WordAddEdit)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(WordAddEdit)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 0, 3, 1, 1)
        self.cbLang = QtGui.QComboBox(WordAddEdit)
        self.cbLang.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbLang.sizePolicy().hasHeightForWidth())
        self.cbLang.setSizePolicy(sizePolicy)
        self.cbLang.setObjectName(_fromUtf8("cbLang"))
        self.cbLang.addItem(_fromUtf8(""))
        self.cbLang.addItem(_fromUtf8(""))
        self.cbLang.addItem(_fromUtf8(""))
        self.gridLayout_2.addWidget(self.cbLang, 0, 4, 1, 1)
        self.teMeaning = QtGui.QTextEdit(WordAddEdit)
        self.teMeaning.setMaximumSize(QtCore.QSize(16777215, 32))
        self.teMeaning.setObjectName(_fromUtf8("teMeaning"))
        self.gridLayout_2.addWidget(self.teMeaning, 1, 2, 1, 3)
        self.label = QtGui.QLabel(WordAddEdit)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 1, 1, 1)
        self.tabWidget = QtGui.QTabWidget(WordAddEdit)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.North)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabTranslate = QtGui.QWidget()
        self.tabTranslate.setObjectName(_fromUtf8("tabTranslate"))
        self.gridLayout_4 = QtGui.QGridLayout(self.tabTranslate)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.tvTranslate = QtGui.QTableView(self.tabTranslate)
        self.tvTranslate.setObjectName(_fromUtf8("tvTranslate"))
        self.gridLayout_4.addWidget(self.tvTranslate, 1, 0, 1, 1)
        self.toolBar = QtGui.QToolBar(self.tabTranslate)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        self.toolBar.setSizePolicy(sizePolicy)
        self.toolBar.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        self.gridLayout_4.addWidget(self.toolBar, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabTranslate, _fromUtf8(""))
        self.tabPronunciation = QtGui.QWidget()
        self.tabPronunciation.setObjectName(_fromUtf8("tabPronunciation"))
        self.tabWidget.addTab(self.tabPronunciation, _fromUtf8(""))
        self.gridLayout_2.addWidget(self.tabWidget, 3, 1, 1, 4)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 3)
        self.btnCancel = QtGui.QPushButton(WordAddEdit)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnCancel.sizePolicy().hasHeightForWidth())
        self.btnCancel.setSizePolicy(sizePolicy)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.gridLayout.addWidget(self.btnCancel, 2, 2, 1, 1)
        self.btnSave = QtGui.QPushButton(WordAddEdit)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSave.sizePolicy().hasHeightForWidth())
        self.btnSave.setSizePolicy(sizePolicy)
        self.btnSave.setObjectName(_fromUtf8("btnSave"))
        self.gridLayout.addWidget(self.btnSave, 2, 1, 1, 1)
        self.actAddTranslate = QtGui.QAction(WordAddEdit)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/images/add_translate.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actAddTranslate.setIcon(icon1)
        self.actAddTranslate.setObjectName(_fromUtf8("actAddTranslate"))
        self.actUpOrder = QtGui.QAction(WordAddEdit)
        self.actUpOrder.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/images/up_translate.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actUpOrder.setIcon(icon2)
        self.actUpOrder.setObjectName(_fromUtf8("actUpOrder"))
        self.actDownOrder = QtGui.QAction(WordAddEdit)
        self.actDownOrder.setEnabled(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/images/down_translate.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actDownOrder.setIcon(icon3)
        self.actDownOrder.setObjectName(_fromUtf8("actDownOrder"))
        self.toolBar.addAction(self.actAddTranslate)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actUpOrder)
        self.toolBar.addAction(self.actDownOrder)

        self.retranslateUi(WordAddEdit)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(WordAddEdit)

    def retranslateUi(self, WordAddEdit):
        WordAddEdit.setWindowTitle(_translate("WordAddEdit", "Редактирование слова", None))
        self.label_2.setText(_translate("WordAddEdit", "значение", None))
        self.label_3.setText(_translate("WordAddEdit", "язык", None))
        self.cbLang.setItemText(0, _translate("WordAddEdit", "рус", None))
        self.cbLang.setItemText(1, _translate("WordAddEdit", "eng", None))
        self.cbLang.setItemText(2, _translate("WordAddEdit", "?", None))
        self.label.setText(_translate("WordAddEdit", "слово", None))
        self.toolBar.setWindowTitle(_translate("WordAddEdit", "toolBar", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTranslate), _translate("WordAddEdit", "перевод", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabPronunciation), _translate("WordAddEdit", "произношение", None))
        self.btnCancel.setText(_translate("WordAddEdit", "Отмена", None))
        self.btnSave.setText(_translate("WordAddEdit", "Сохранить", None))
        self.actAddTranslate.setText(_translate("WordAddEdit", "Добавить перевод", None))
        self.actUpOrder.setText(_translate("WordAddEdit", "Увеличить приоритет", None))
        self.actDownOrder.setText(_translate("WordAddEdit", "Уменьшить приоритет", None))

import resources_rc
