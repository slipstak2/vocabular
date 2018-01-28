# https://gist.github.com/Riateche/5984815
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

import functools
from PySide import QtGui
from PySide.QtCore import Slot as pyqtSlot
from PySide import QtSql, QtCore
from models.base.db import getDb

columns = ['id', 'name', 'play']
buttonColumn = 2


def needRefresh(func):
    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.refresh()
        return result
    return inner


class DictionaryModel(QtSql.QSqlQueryModel):
    fields = ['id', 'name']
    tableName = 'dictionary'

    @needRefresh
    def __init__(self, currentDictIndex=0, *args, **kwargs):
        super(DictionaryModel, self).__init__(*args, **kwargs)
        self.db = getDb()   # TODO: singleton
        self._currentDictIndex = currentDictIndex
        self.childModels = []

    @property
    def currentDictIndex(self):
        return self._currentDictIndex

    @currentDictIndex.setter
    def currentDictIndex(self, index):
        self._currentDictIndex = index
        for childModel in self.childModels:
            childModel.refresh()

    @property
    def currentDictId(self):
        return self.record(self.currentDictIndex).value('id')

    @property
    def currentDictName(self):
        return self.record(self.currentDictIndex).value('name')

    def viewFieldIndex(self):
        return self.fieldIndex(DictionaryModel.viewField)

    def fieldIndex(self, fieldName):
        return DictionaryModel.fields.index(fieldName)

    def refresh(self):
        self.setQuery("SELECT {fields} FROM {tableName} ORDER BY date_create".format(
            fields=', '.join(DictionaryModel.fields),
            tableName=DictionaryModel.tableName
        ))

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(columns)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        value = super(DictionaryModel, self).data(index, role)
        if role == QtCore.Qt.DisplayRole and index.column() == buttonColumn:
            return 'play'
        return value


class TableModel(QtCore.QAbstractTableModel):
    def rowCount(self, parent=QtCore.QModelIndex()): return 5
    def columnCount(self, parent=QtCore.QModelIndex()): return len(columns)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        if not role == QtCore.Qt.DisplayRole:
            return None

        if index.column() == buttonColumn:
            return 'play'

        return "{0:02d}".format(index.row())
        
    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        print "setData", index.row(), index.column(), value



class ButtonDelegate(QtGui.QItemDelegate):
    def __init__(self, parent):
        QtGui.QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        btn = QtGui.QPushButton(str(index.data()), parent)
        btn.clicked.connect(self.currentIndexChanged)
        return btn
        
    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())
        
    @pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())


class TableView(QtGui.QTableView):
    """
    A simple table to demonstrate the QComboBox delegate.
    """
    def __init__(self, *args, **kwargs):
        QtGui.QTableView.__init__(self, *args, **kwargs)

        # Set the delegate for column 0 of our table
        # self.setItemDelegateForColumn(0, ButtonDelegate(self))
        self.setItemDelegateForColumn(buttonColumn, ButtonDelegate(self))

    
if __name__=="__main__":
    from sys import argv, exit

    class Widget(QtGui.QWidget):
        """
        A simple test widget to contain and own the model and table.
        """
        def __init__(self, parent=None):
            QtGui.QWidget.__init__(self, parent)

            l=QtGui.QVBoxLayout(self)
            self._tm=TableModel(self)
            self._tm=DictionaryModel(self)
            self._tv=TableView(self)
            #self._tv.setGridStyle(QtCore.Qt.NoPen)
            self._tv.setShowGrid(False)
            self._tv.setAlternatingRowColors(True)
            self._tv.setModel(self._tm)

            self._tv.hideColumn(0)

            for row in range(0, self._tm.rowCount()):
                self._tv.openPersistentEditor(self._tm.index(row, buttonColumn))
            
            l.addWidget(self._tv)

    a=QtGui.QApplication(argv)
    w=Widget()
    w.move(0, 0)
    w.resize(800, 600)    
    w.show()
    w.raise_()
    exit(a.exec_())