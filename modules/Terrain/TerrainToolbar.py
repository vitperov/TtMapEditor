from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon

class TerrainToolbar(QWidget):
    mapSettings  = pyqtSignal()
    openMap      = pyqtSignal(str)
    saveMap      = pyqtSignal(str)
    refreshMap   = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._layout = QHBoxLayout()
        self.setLayout(self._layout)

        self._settingsBtn   = QPushButton("Generator settings")
        self._openBtn       = QPushButton("Open")
        self._saveBtn       = QPushButton("Save")
        self._refreshButton = QPushButton("Refresh", self)
        
        self._openBtn.setIcon(QIcon.fromTheme("document-open"))
        self._saveBtn.setIcon(QIcon.fromTheme("document-save"))
        self._refreshButton.setIcon(QIcon.fromTheme("view-refresh"))

        self._layout.addWidget(self._settingsBtn)
        self._layout.addWidget(self._openBtn)
        self._layout.addWidget(self._saveBtn)
        self._layout.addWidget(self._refreshButton)

        self._layout.addStretch()

        self._settingsBtn.clicked.connect(self._settingsDlg)
        self._openBtn.clicked.connect(self._openFile)
        self._saveBtn.clicked.connect(self._saveFile)
        self._refreshButton.clicked.connect(self._refreshAction)

    def _settingsDlg(self):
        self.mapSettings.emit()

    def _saveFile(self):
        name, _ = QFileDialog.getSaveFileName(self, 'Save File', 'output/terrain', filter='*.json')
        if name:
            self.saveMap.emit(name)

    def _openFile(self):
        name, _ = QFileDialog.getOpenFileName(self, 'Open File', 'output/terrain', filter='*.json')
        if name:
            self.openMap.emit(name)
        
    def _refreshAction(self):
        self.refreshMap.emit()
