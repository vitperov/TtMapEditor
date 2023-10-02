from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from functools import partial

from modules.GeneratorSettingsDlg import *

class MapActionsPanel(QWidget):
    generateMap  = pyqtSignal()
    saveMap      = pyqtSignal(str)

    def __init__(self):
        QWidget.__init__(self)
        self._layout = QHBoxLayout()

        self.setLayout(self._layout)

        self._settingsBtn   = QPushButton("Generator settings");
        self._generateBtn   = QPushButton("Generate map");
        self._saveBtn       = QPushButton("Save")
        
        self._layout.addWidget(self._settingsBtn)
        self._layout.addWidget(self._generateBtn)
        self._layout.addWidget(self._saveBtn)

        self._layout.addStretch()

        self._settingsBtn.clicked.connect(self._settingsDlg)
        self._generateBtn.clicked.connect(self._newMap)
        self._saveBtn.clicked.connect(self._saveFile)

    def _settingsDlg(self):
        GeneratorSettingsDlg.runDlg()

    def _newMap(self):
        self.generateMap.emit()

    def _saveFile(self):
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File', filter='*.json')
        name = name[0]
        print(name)
        self.saveMap.emit(name)
