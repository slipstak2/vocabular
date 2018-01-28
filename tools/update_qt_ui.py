import os
import subprocess

_DEPRECATED_IMPORT = 'from PyQt4 import QtCore, QtGui'
_UPDATE_IMPORT = '''
try:
    from PySide import QtCore, QtGui
except ImportError:
    from PyQt4 import QtCore, QtGui
'''


PYTHON_SITE_PACKAGE_CWD = r'C:\Python27\Lib\site-packages\PyQt4'

_TARGET_UI_PATH = r'E:\YandexDisk\Vocabular\ui'

_UI_ITEMS = [os.path.splitext(f)[0] for f in os.listdir('./ui') if os.path.isfile(os.path.join('./ui', f)) and f.endswith('.ui')]

_SOURCE_RES_NAME = 'resources.qrc'
_SOURCE_RES_PATH = os.path.join(_TARGET_UI_PATH, _SOURCE_RES_NAME)

_TARGET_RES_PY = 'resources_rc.py'
_TARGET_RES_PY_PATH = os.path.join(_TARGET_UI_PATH, _TARGET_RES_PY)


def _target_ui_py_path(ui_item):
    return os.path.join(_TARGET_UI_PATH, ui_item + '_ui.py')


def _runCmd(description, cmd, cwd):
    si = subprocess.STARTUPINFO()
    si.dwFlags = subprocess.STARTF_USESHOWWINDOW
    si.wShowWindow = subprocess.SW_HIDE
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=cwd,
        startupinfo=si,
    )
    out, err = process.communicate()
    if out or err:
        raise Exception(
            '{description}\nstdout = {out}\nstderr = {err}\n'.format(
                description=description,
                out=out,
                err=err,
            )
        )


def refreshMainWindowUi():
    for ui_item in _UI_ITEMS:
        cmd = [
            'pyuic4.bat',
            os.path.join(_TARGET_UI_PATH, ui_item + '.ui'),
            '-o',
            _target_ui_py_path(ui_item)
        ]
        _runCmd("refreshMainWindowUi", cmd, PYTHON_SITE_PACKAGE_CWD)


def refreshResources():
    cmd = [
        'pyrcc4.exe',
        _SOURCE_RES_PATH,
        '-o',
        _TARGET_RES_PY_PATH,
    ]
    _runCmd('refreshResources', cmd, PYTHON_SITE_PACKAGE_CWD)


def patchMainWindowUi():
    for ui_item in _UI_ITEMS:
        with open(_target_ui_py_path(ui_item), 'r') as f:
            content = f.read()

        content = content.replace(_DEPRECATED_IMPORT, _UPDATE_IMPORT)

        with open(_target_ui_py_path(ui_item), 'w') as f:
            f.write(content)


def updateQtUI():
    refreshMainWindowUi()
    refreshResources()
    patchMainWindowUi()


if __name__ == '__main__':
    updateQtUI()
