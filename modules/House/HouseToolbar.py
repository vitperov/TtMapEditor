from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QSize
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
    #changedSelection = pyqtSignal(bool)

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

        #self._singleSelectionBtn = QPushButton()
        #self._singleSelectionBtn.setCheckable(True)
        #self._singleSelectionBtn.setChecked(True)
        #self._singleSelectionBtn.setIcon(QIcon("resources/single_selection.png"))
        #self._singleSelectionBtn.setIconSize(self.ICON_SIZE)
        #self._singleSelectionBtn.clicked.connect(self._onSingleSelection)
        
        #self._multipleSelectionBtn = QPushButton()
        #self._multipleSelectionBtn.setCheckable(True)
        #self._multipleSelectionBtn.setIcon(QIcon("resources/multiple_selection.png"))
        #self._multipleSelectionBtn.setIconSize(self.ICON_SIZE)
        #self._multipleSelectionBtn.clicked.connect(self._onMultipleSelection)

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
        #self._layout.addWidget(self._singleSelectionBtn)
        #self._layout.addWidget(self._multipleSelectionBtn)
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
        name, _ = QFileDialog.getSaveFileName(self, 'Save File', 'output/house', filter='*.json')
        if name:
            print(name)
            self.saveMap.emit(name)

    def _openFile(self):
        name, _ = QFileDialog.getOpenFileName(self, 'Open File', 'output/house', filter='*.json')
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
        model_z_level = index
        print("Floor changed to", model_z_level)
        self.zLevelChanged.emit(model_z_level)

    def _onSingleSelection(self):
        if self._multipleSelectionBtn.isChecked():
            self._multipleSelectionBtn.setChecked(False)
        print("Single Selection")
        self.changedSelection.emit(False)

    #def _onMultipleSelection(self):
    #    if self._singleSelectionBtn.isChecked():
    #        self._singleSelectionBtn.setChecked(False)
    #    print("Multiple Selection")
    #    self.changedSelection.emit(True)
