from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from functools import partial

class ActionsPanel(QWidget):
    newMap      = pyqtSignal(int, int)
    saveMap     = pyqtSignal(str)
    openMap     = pyqtSignal(str)

    def __init__(self):
        QWidget.__init__(self)
        self._layout = QHBoxLayout()

        self.setLayout(self._layout)

        self._newBtn     = QPushButton("New")
        self._openBtn    = QPushButton("Open")
        self._saveBtn    = QPushButton("Save")
        
        self._layout.addWidget(self._newBtn)
        self._layout.addWidget(self._openBtn)
        self._layout.addWidget(self._saveBtn)
        self._layout.addStretch()

        self._newBtn.clicked.connect(self._newFile)
        self._openBtn.clicked.connect(self._openFile)
        self._saveBtn.clicked.connect(self._saveFile)

    def _newFile(self):
        print("new map")
        self.newMap.emit(8, 8)

    def _saveFile(self):
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File', filter='*.json')
        name = name[0]
        print(name)
        self.saveMap.emit(name)

    def _openFile(self):
        name = QtGui.QFileDialog.getOpenFileName(self, 'Open File', filter='*.json')
        name = name[0]
        self.openMap.emit(name)
