# -*- coding: utf-8 -*-

from tools.update_qt_ui import updateQtUI
updateQtUI()

import sys
from PySide import QtGui
app = QtGui.QApplication(sys.argv)

from forms.vocabular_main_window import VocabularMainWindow
from app_settings import AppSettings, AppMode

def run():
    wnd = VocabularMainWindow()
    wnd.show()
    app.exec_()

if __name__ == '__main__':
    AppSettings(AppMode.DEVELOP)
    run()
