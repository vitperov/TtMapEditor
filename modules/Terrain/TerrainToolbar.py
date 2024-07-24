from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from functools import partial

class TerrainToolbar(QWidget):
    mapSettings  = pyqtSignal()
    saveMap      = pyqtSignal(str)
    refreshMap   = pyqtSignal()

    def __init__(self):
        QWidget.__init__(self)
        self._layout = QHBoxLayout()

        self.setLayout(self._layout)

        self._settingsBtn   = QPushButton("Generator settings");
        self._saveBtn       = QPushButton("Save")
        self._refreshButton = QPushButton("Refresh", self)
        self._refreshButton.setIcon(QtGui.QIcon.fromTheme("view-refresh"))
        
        self._layout.addWidget(self._settingsBtn)
        self._layout.addWidget(self._saveBtn)
        self._layout.addWidget(self._refreshButton)

        self._layout.addStretch()

        self._settingsBtn.clicked.connect(self._settingsDlg)
        self._saveBtn.clicked.connect(self._saveFile)
        self._refreshButton.clicked.connect(self._refreshAction)

    def _settingsDlg(self):
        self.mapSettings.emit()

    def _saveFile(self):
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File', filter='*.json')
        name = name[0]
        print(name)
        self.saveMap.emit(name)
        
    def _refreshAction(self):
        self.refreshMap.emit()
