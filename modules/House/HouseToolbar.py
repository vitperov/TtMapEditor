from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QFileDialog, QComboBox, QLabel, QMenu
from PyQt5.QtGui import QIcon
from functools import partial

class HouseToolbar(QWidget):
    newMap = pyqtSignal(int, int)
    saveMap = pyqtSignal(str)
    openMap = pyqtSignal(str)
    addColumn = pyqtSignal(bool)
    addRow = pyqtSignal(bool)
    zLevelChanged = pyqtSignal(int)
    generateWallFrame = pyqtSignal()
    generateRoofFrame = pyqtSignal()

    ICON_SIZE = QSize(32, 32)  # Common size constant for all icons

    def __init__(self):
        super().__init__()
        self._layout = QHBoxLayout()
        self.setLayout(self._layout)

        # Create main toolbar buttons with standard icons
        self._newBtn = QPushButton()
        self._newBtn.setIcon(QIcon.fromTheme("document-new"))
        self._newBtn.setIconSize(self.ICON_SIZE)

        self._openBtn = QPushButton()
        self._openBtn.setIcon(QIcon.fromTheme("document-open"))
        self._openBtn.setIconSize(self.ICON_SIZE)

        self._saveBtn = QPushButton()
        self._saveBtn.setIcon(QIcon.fromTheme("document-save"))
        self._saveBtn.setIconSize(self.ICON_SIZE)

        # Create additional toolbar buttons with icons
        self._addColumnBtn = QPushButton("")
        self._addColumnBtn.setIcon(QIcon("resources/add-column.png"))
        self._addColumnBtn.setIconSize(self.ICON_SIZE)
        
        self._addRowBtn = QPushButton("")
        self._addRowBtn.setIcon(QIcon("resources/add-row.png"))
        self._addRowBtn.setIconSize(self.ICON_SIZE)

        # Add dropdown to buttons
        self._addColumnMenu = QMenu()
        self._addColumnMenu.addAction("Before", partial(self._addColumn, True))
        self._addColumnMenu.addAction("After", partial(self._addColumn, False))
        self._addColumnBtn.setMenu(self._addColumnMenu)

        self._addRowMenu = QMenu()
        self._addRowMenu.addAction("Before", partial(self._addRow, True))
        self._addRowMenu.addAction("After", partial(self._addRow, False))
        self._addRowBtn.setMenu(self._addRowMenu)

        # Create frame generation buttons
        self._generateWallBtn = QPushButton("Generate Wall frame")
        self._generateWallBtn.setIcon(QIcon("resources/wall-frame.png"))
        self._generateWallBtn.setIconSize(self.ICON_SIZE)
        
        self._generateRoofBtn = QPushButton("Generate Roof frame")
        self._generateRoofBtn.setIcon(QIcon("resources/roof-frame.png"))
        self._generateRoofBtn.setIconSize(self.ICON_SIZE)

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
        self._layout.addWidget(self._generateWallBtn)
        self._layout.addWidget(self._generateRoofBtn)
        self._layout.addWidget(QLabel("Floor:"))
        self._layout.addWidget(self._floorComboBox)
        self._layout.addStretch()

        # Connect buttons to their respective methods
        self._newBtn.clicked.connect(self._newFile)
        self._openBtn.clicked.connect(self._openFile)
        self._saveBtn.clicked.connect(self._saveFile)
        self._generateWallBtn.clicked.connect(self.generateWallFrame.emit)
        self._generateRoofBtn.clicked.connect(self.generateRoofFrame.emit)

    def _newFile(self):
        print("new map")
        self.newMap.emit(8, 8)

    def _saveFile(self):
        name, _ = QFileDialog.getSaveFileName(self, 'Save File', 'output/house', filter='*.json')
        if name:
            print(name)
            self.saveMap.emit(name)

    def _openFile(self):
        name, _ = QFileDialog.getOpenFileName(self, 'Open File', 'output/house', filter='*.json')
        if name:
            print(name)
            self.openMap.emit(name)

    def _addColumn(self, before):
        print(f"add column {'before' if before else 'after'}")
        self.addColumn.emit(before)

    def _addRow(self, before):
        print(f"add row {'before' if before else 'after'}")
        self.addRow.emit(before)

    def _floorChanged(self, index):
        model_z_level = index
        print("Floor changed to", model_z_level)
        self.zLevelChanged.emit(model_z_level)
