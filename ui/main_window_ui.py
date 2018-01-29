# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:/slipstak2/vocabular\ui\main_window.ui'
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

class Ui_VocabularMainWindow(object):
    def setupUi(self, VocabularMainWindow):
        VocabularMainWindow.setObjectName(_fromUtf8("VocabularMainWindow"))
        VocabularMainWindow.resize(349, 543)
        VocabularMainWindow.setMouseTracking(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/images/dictionary.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        VocabularMainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(VocabularMainWindow)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gbDictionary = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbDictionary.sizePolicy().hasHeightForWidth())
        self.gbDictionary.setSizePolicy(sizePolicy)
        self.gbDictionary.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.gbDictionary.setMouseTracking(True)
        self.gbDictionary.setFlat(False)
        self.gbDictionary.setCheckable(False)
        self.gbDictionary.setObjectName(_fromUtf8("gbDictionary"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.gbDictionary)
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(9, 0, 9, 6)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.cbDicts = QtGui.QComboBox(self.gbDictionary)
        self.cbDicts.setFrame(True)
        self.cbDicts.setObjectName(_fromUtf8("cbDicts"))
        self.horizontalLayout.addWidget(self.cbDicts)
        self.btnAddDict = QtGui.QPushButton(self.gbDictionary)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAddDict.sizePolicy().hasHeightForWidth())
        self.btnAddDict.setSizePolicy(sizePolicy)
        self.btnAddDict.setMouseTracking(True)
        self.btnAddDict.setAutoFillBackground(False)
        self.btnAddDict.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/images/add_dict.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAddDict.setIcon(icon1)
        self.btnAddDict.setIconSize(QtCore.QSize(24, 24))
        self.btnAddDict.setCheckable(False)
        self.btnAddDict.setAutoDefault(False)
        self.btnAddDict.setDefault(False)
        self.btnAddDict.setFlat(True)
        self.btnAddDict.setObjectName(_fromUtf8("btnAddDict"))
        self.horizontalLayout.addWidget(self.btnAddDict)
        self.btnEditDict = QtGui.QPushButton(self.gbDictionary)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnEditDict.sizePolicy().hasHeightForWidth())
        self.btnEditDict.setSizePolicy(sizePolicy)
        self.btnEditDict.setMouseTracking(True)
        self.btnEditDict.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/images/edit_dict.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnEditDict.setIcon(icon2)
        self.btnEditDict.setIconSize(QtCore.QSize(24, 24))
        self.btnEditDict.setAutoDefault(False)
        self.btnEditDict.setDefault(False)
        self.btnEditDict.setFlat(True)
        self.btnEditDict.setObjectName(_fromUtf8("btnEditDict"))
        self.horizontalLayout.addWidget(self.btnEditDict)
        self.btnRemoveDict = QtGui.QPushButton(self.gbDictionary)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnRemoveDict.sizePolicy().hasHeightForWidth())
        self.btnRemoveDict.setSizePolicy(sizePolicy)
        self.btnRemoveDict.setMouseTracking(True)
        self.btnRemoveDict.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/images/delete_dict.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnRemoveDict.setIcon(icon3)
        self.btnRemoveDict.setIconSize(QtCore.QSize(24, 24))
        self.btnRemoveDict.setCheckable(False)
        self.btnRemoveDict.setFlat(True)
        self.btnRemoveDict.setObjectName(_fromUtf8("btnRemoveDict"))
        self.horizontalLayout.addWidget(self.btnRemoveDict)
        self.verticalLayout.addWidget(self.gbDictionary)
        self.gbWords = QtGui.QGroupBox(self.centralwidget)
        self.gbWords.setObjectName(_fromUtf8("gbWords"))
        self.gridLayout = QtGui.QGridLayout(self.gbWords)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tvEngWords = QtGui.QTableView(self.gbWords)
        self.tvEngWords.setObjectName(_fromUtf8("tvEngWords"))
        self.gridLayout.addWidget(self.tvEngWords, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.gbWords)
        VocabularMainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtGui.QToolBar(VocabularMainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        VocabularMainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.menuBar = QtGui.QMenuBar(VocabularMainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 349, 21))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuHelp = QtGui.QMenu(self.menuBar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menu = QtGui.QMenu(self.menuBar)
        self.menu.setObjectName(_fromUtf8("menu"))
        VocabularMainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtGui.QStatusBar(VocabularMainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        VocabularMainWindow.setStatusBar(self.statusBar)
        self.actionAbout = QtGui.QAction(VocabularMainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/images/info.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon4)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actExit = QtGui.QAction(VocabularMainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/images/exit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actExit.setIcon(icon5)
        self.actExit.setObjectName(_fromUtf8("actExit"))
        self.actAddWord = QtGui.QAction(VocabularMainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/images/add_word.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actAddWord.setIcon(icon6)
        self.actAddWord.setObjectName(_fromUtf8("actAddWord"))
        self.toolBar.addAction(self.actAddWord)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuFile.addAction(self.actExit)
        self.menu.addAction(self.actAddWord)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menu.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(VocabularMainWindow)
        QtCore.QMetaObject.connectSlotsByName(VocabularMainWindow)

    def retranslateUi(self, VocabularMainWindow):
        VocabularMainWindow.setWindowTitle(_translate("VocabularMainWindow", "Vocabular", None))
        self.gbDictionary.setTitle(_translate("VocabularMainWindow", "Словарь", None))
        self.btnAddDict.setToolTip(_translate("VocabularMainWindow", "Добавить словарь", None))
        self.btnEditDict.setToolTip(_translate("VocabularMainWindow", "Редактировать словарь", None))
        self.btnRemoveDict.setToolTip(_translate("VocabularMainWindow", "Удалить словарь", None))
        self.gbWords.setTitle(_translate("VocabularMainWindow", "Слова", None))
        self.toolBar.setWindowTitle(_translate("VocabularMainWindow", "toolBar", None))
        self.menuHelp.setTitle(_translate("VocabularMainWindow", "Помощь", None))
        self.menuFile.setTitle(_translate("VocabularMainWindow", "Файл", None))
        self.menu.setTitle(_translate("VocabularMainWindow", "Редактирование", None))
        self.actionAbout.setText(_translate("VocabularMainWindow", "О программе", None))
        self.actExit.setText(_translate("VocabularMainWindow", "Выход", None))
        self.actExit.setShortcut(_translate("VocabularMainWindow", "Ctrl+Q", None))
        self.actAddWord.setText(_translate("VocabularMainWindow", "Добавить слово", None))

import resources_rc