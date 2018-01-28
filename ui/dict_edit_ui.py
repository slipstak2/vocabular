# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\YandexDisk\Vocabular\ui\dict_edit.ui'
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

class Ui_DictAddEdit(object):
    def setupUi(self, DictAddEdit):
        DictAddEdit.setObjectName(_fromUtf8("DictAddEdit"))
        DictAddEdit.setWindowModality(QtCore.Qt.ApplicationModal)
        DictAddEdit.resize(381, 91)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DictAddEdit.sizePolicy().hasHeightForWidth())
        DictAddEdit.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/images/dictionary.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DictAddEdit.setWindowIcon(icon)
        DictAddEdit.setModal(False)
        self.gridLayout = QtGui.QGridLayout(DictAddEdit)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(DictAddEdit)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.leDictName = QtGui.QLineEdit(DictAddEdit)
        self.leDictName.setObjectName(_fromUtf8("leDictName"))
        self.gridLayout.addWidget(self.leDictName, 0, 1, 1, 3)
        self.btnCancel = QtGui.QPushButton(DictAddEdit)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnCancel.sizePolicy().hasHeightForWidth())
        self.btnCancel.setSizePolicy(sizePolicy)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.gridLayout.addWidget(self.btnCancel, 2, 3, 1, 1)
        self.btnSave = QtGui.QPushButton(DictAddEdit)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSave.sizePolicy().hasHeightForWidth())
        self.btnSave.setSizePolicy(sizePolicy)
        self.btnSave.setObjectName(_fromUtf8("btnSave"))
        self.gridLayout.addWidget(self.btnSave, 2, 2, 1, 1)

        self.retranslateUi(DictAddEdit)
        QtCore.QMetaObject.connectSlotsByName(DictAddEdit)

    def retranslateUi(self, DictAddEdit):
        DictAddEdit.setWindowTitle(_translate("DictAddEdit", "Редактирование словаря", None))
        self.label.setText(_translate("DictAddEdit", "Словарь", None))
        self.btnCancel.setText(_translate("DictAddEdit", "Отмена", None))
        self.btnSave.setText(_translate("DictAddEdit", "Сохранить", None))

import resources_rc
