from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import json
from json import JSONEncoder

from modules.ClassVariablesGuiEditor import *

def clearLayout(layout):
    for i in reversed(range(layout.count())):
        child = layout.itemAt(i)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())

class TerrainGeneratorSettingsDlg(QtGui.QDialog):
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

