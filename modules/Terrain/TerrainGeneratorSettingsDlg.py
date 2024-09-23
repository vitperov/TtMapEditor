try:
    import PyQt5
    PyQt = 'PyQt5'
except:
    import PyQt4
    PyQt = 'PyQt4'

def dynamic_import (module_full_name, target_name):
    tmp = __import__(module_full_name)
    return getattr(tmp, target_name)
    
def dynamic_import_from (module_full_name, target_names = ['*',], update_globals = True):
    tmp = __import__(module_full_name, fromlist = target_names)
    if (update_globals):
        was_star = False
        for name in target_names:
            if ('*' == name):
                was_star = True
                continue
            value = getattr(tmp, name)
            globals()[name] = value
        if (was_star):
            globals().update(tmp.__dict__)
    return tmp

def fullname (o):
    module = o.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return o.__class__.__name__
    return module + '.' + o.__class__.__name__

QtWidgets = dynamic_import(str(PyQt),  'QtWidgets') #from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

dynamic_import_from(str(PyQt) + '.QtCore', ['*']) #from PyQt5.QtCore import *
dynamic_import_from(str(PyQt) + '.QtWidgets', ['*']) #from PyQt5.QtWidgets import *

try:
    dynamic_import_from(str(PyQt) + '.QtGui', ['QDialog']) #from PyQt5.QtGui import QDialog
except:
    dynamic_import_from(str(PyQt) + '.QtWidgets', ['QDialog']) #from PyQt5.QtWidgets import QDialog # see https://github.com/3liz/lizmap-plugin/issues/98

import json
from json import JSONEncoder

from modules.ClassVariablesGuiEditor import *

#print('QDialog: ', fullname(QDialog))

def clearLayout(layout):
    for i in reversed(range(layout.count())):
        child = layout.itemAt(i)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())

class TerrainGeneratorSettingsDlg(QDialog):
    def __init__(self, title, dataPtrRW, parent=None):
        super().__init__(parent)

        self._data = dataPtrRW

        self.setWindowTitle(title)

        layout = QVBoxLayout()

        loadSaveLayout = QHBoxLayout()

        loadButton = QPushButton()
        saveButton = QPushButton()

        loadButton.setText("Reset settings")
        saveButton.setText("Save settings")

        loadButton.clicked.connect(self.onLoadPressed)
        saveButton.clicked.connect(self.onSavePressed)

        loadSaveLayout.addWidget(loadButton)
        loadSaveLayout.addWidget(saveButton)

        layout.addLayout(loadSaveLayout)

        self.dynamicLayout = QVBoxLayout()
        layout.addLayout(self.dynamicLayout)

        self.setLayout(layout)

    def onSavePressed(self):
        self._data.saveToFile()

    def onLoadPressed(self):
        self._data.loadFromFile()
        clearLayout(self.dynamicLayout)
        edt = ClassVariablesGuiEditor();
        edt.createControls(self._data, "Settings:", self.dynamicLayout)

    # Set parentWnd=None for modal dialogue
    @staticmethod
    def runDlg(title, dataPtrRW, parentWnd=None):
        dlg = TerrainGeneratorSettingsDlg(title, dataPtrRW, parentWnd)

        if parentWnd is None:
            dlg.setModal(True)
            dlg.exec_()
        else:
            dlg.show()

