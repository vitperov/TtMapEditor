from PyQt5 import QtWidgets, QtGui
from pyqtgraph.Qt import QtCore

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from functools import partial
from modules.SimpleSquareItem import SimpleSquareItem
from modules.ChooseRotationDlg import ChooseRotationDlg
from modules.ChooseModelDlg import ChooseModelDlg
from modules.MapModelGeneral import SelectionRange

class PropertiesItem(QWidget):
    updateAllProperties = pyqtSignal()  # Signal to notify when properties are updated

    def __init__(self, objModel, objCollection, mapModel, category, multi_select=False, tilesize=64, parent=None):
        super(PropertiesItem, self).__init__(parent)  # Initialize QWidget directly
        self._model = objModel
        self._mapModel = mapModel
        self._category = category
        
        sqType = self._model.getProperty('model')
        if multi_select:
            sqType += " (multiple squares)"

        # Create a layout for the widget
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Set up the group box with a title
        groupBox = QGroupBox(sqType, self)
        groupBoxLayout = QHBoxLayout()  # Change to QHBoxLayout for horizontal arrangement
        groupBox.setLayout(groupBoxLayout)
        layout.addWidget(groupBox)
        
        # Change groupbox background if multiple squares are selected
        if multi_select:
            groupBox.setStyleSheet("background-color: #A5CEC0")

        # Add SimpleSquareItem
        self.modelPicture = SimpleSquareItem(objModel, objCollection, tilesize, multi_select)
        groupBoxLayout.addWidget(self.modelPicture)

        # Create a vertical layout to stack buttons
        buttonLayout = QVBoxLayout()
        groupBoxLayout.addLayout(buttonLayout)
        
        # Model Button
        modelBtn = QPushButton()
        modelBtn.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        modelBtn.clicked.connect(self.showChooseModelDlg)
        buttonLayout.addWidget(modelBtn)

        # Rotation Button
        rotationBtn = QPushButton()
        rotationBtn.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        rotationBtn.clicked.connect(self.showChooseRotationDlg)
        buttonLayout.addWidget(rotationBtn)

        # Remove Button
        removeBtn = QPushButton()
        removeBtn.setIcon(self.style().standardIcon(QStyle.SP_DialogCancelButton))
        buttonLayout.addWidget(removeBtn)
        removeBtn.clicked.connect(partial(self.removeObject, self._model.id))

    def showChooseRotationDlg(self):
        dlg = ChooseRotationDlg(self._model, self._mapModel._objCollection, 64)
        if dlg.exec_() == QDialog.Accepted:
            chosenRotation = dlg.selectedRotation
            if chosenRotation is not None:
                self._model.setProperty('rotation', str(chosenRotation))
                self._mapModel.updateEntireMap()
                self.modelPicture.updatePixmap()

    def showChooseModelDlg(self):
        dlg = ChooseModelDlg(self._mapModel._objCollection, self._category, 64)
        if dlg.exec_() == QDialog.Accepted:
            chosenModel = dlg.selectedModel
            if chosenModel is not None:
                self._model.setProperty('model', chosenModel)
                self._mapModel.updateEntireMap()
                self.modelPicture.updatePixmap()

    def removeObject(self, id):
        self._mapModel.deleteSquareById(id)
        self.updateAllProperties.emit()

class PropertiesPanel(QWidget):
    updatedEntireMap = pyqtSignal()
    def __init__(self, category):
        QWidget.__init__(self)

        self.selectionRange = None
        self._category = category

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.coordinatesLbl = QLabel("X: ? Y: ?")
        layout.addWidget(self.coordinatesLbl)

        self.properties = QVBoxLayout()
        layout.addLayout(self.properties)

        addBtn = QPushButton()
        addBtn.setIcon(QtGui.QIcon('resources/greenPlus.png'))
        layout.addWidget(addBtn)
        addBtn.clicked.connect(self.addObject)

        layout.addStretch()  # Add vertical spacer at the end

    def setModel(self, model):
        self.mapModel = model

    def onSquaresSelected(self, selectionRange):
        self.selectionRange = selectionRange

        startCol = selectionRange.startCol
        startRow = selectionRange.startRow
        endCol = selectionRange.endCol
        endRow = selectionRange.endRow
        zLevel = selectionRange.zLevel

        for i in reversed(range(self.properties.count())):
            self.properties.itemAt(i).widget().setParent(None)

        if startCol == endCol and startRow == endRow:
            items = self.mapModel.getSquareItems(startCol, startRow, zLevel)
            self.coordinatesLbl.setText("X: " + str(startCol) + " Y: " + str(startRow) + " Zlevel: " + str(zLevel))
            multi_select = False
        else:
            items = self.mapModel.getAreaSquareUniqueItems(selectionRange)
            width = abs(endCol - startCol) + 1
            height = abs(endRow - startRow) + 1
            totalItems = width * height
            self.coordinatesLbl.setText(f"{totalItems} squares selected")
            multi_select = True
        
        for itemModel in items:
            itemWg = PropertiesItem(itemModel, self.mapModel._objCollection, self.mapModel, self._category, multi_select)
            itemWg.updateAllProperties.connect(self.update)
            self.properties.addWidget(itemWg)

    def addObject(self):
        if self.selectionRange is not None:
            obj = self.mapModel.createObjectAt(self.selectionRange.startCol, self.selectionRange.startRow, self.selectionRange.zLevel)
            self.onSquaresSelected(self.selectionRange)
            self.updatedEntireMap.emit()

    def update(self):
        if self.selectionRange:
            self.onSquaresSelected(self.selectionRange)
