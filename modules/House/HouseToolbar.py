from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QFileDialog, QComboBox, QLabel
from PyQt5.QtGui import QIcon
from functools import partial

class HouseToolbar(QWidget):
    newMap = pyqtSignal(int, int)
    saveMap = pyqtSignal(str)
    openMap = pyqtSignal(str)
    addColumn = pyqtSignal()
    addRow = pyqtSignal()
    zLevelChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._layout = QHBoxLayout()
        self.setLayout(self._layout)

        # Create main toolbar buttons
        self._newBtn = QPushButton("New")
        self._openBtn = QPushButton("Open")
        self._saveBtn = QPushButton("Save")

        # Create additional toolbar buttons with icons
        self._addColumnBtn = QPushButton("Add Column")
        self._addColumnBtn.setIcon(QIcon("resources/add-column.png"))
        
        self._addRowBtn = QPushButton("Add Row")
        self._addRowBtn.setIcon(QIcon("resources/add-row.png"))

        # Create dropdown for Floor
        self._floorComboBox = QComboBox()
        self._floorComboBox.addItems(map(str, [i * 0.5 for i in range(7)]))
        self._floorComboBox.currentIndexChanged.connect(self._floorChanged)

        # Add buttons to layout
        self._layout.addWidget(self._newBtn)
        self._layout.addWidget(self._openBtn)
        self._layout.addWidget(self._saveBtn)
        self._layout.addWidget(self._addColumnBtn)
        self._layout.addWidget(self._addRowBtn)
        self._layout.addWidget(QLabel("Floor:"))
        self._layout.addWidget(self._floorComboBox)
        self._layout.addStretch()

        # Connect buttons to their respective methods
        self._newBtn.clicked.connect(self._newFile)
        self._openBtn.clicked.connect(self._openFile)
        self._saveBtn.clicked.connect(self._saveFile)
        self._addColumnBtn.clicked.connect(self._addColumn)
        self._addRowBtn.clicked.connect(self._addRow)

    def _newFile(self):
        print("new map")
        self.newMap.emit(8, 8)

    def _saveFile(self):
        name, _ = QFileDialog.getSaveFileName(self, 'Save File', filter='*.json')
        if name:
            print(name)
            self.saveMap.emit(name)

    def _openFile(self):
        name, _ = QFileDialog.getOpenFileName(self, 'Open File', filter='*.json')
        if name:
            print(name)
            self.openMap.emit(name)

    def _addColumn(self):
        print("add column")
        self.addColumn.emit()

    def _addRow(self):
        print("add row")
        self.addRow.emit()

    def _floorChanged(self, index):
        model_z_level = round(index * 2)
        print("Floor changed to", model_z_level)
        self.zLevelChanged.emit(model_z_level)
