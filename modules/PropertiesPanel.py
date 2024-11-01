from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from functools import partial
from modules.SimpleSquareItem import SimpleSquareItem
from modules.ChooseRotationDlg import ChooseRotationDlg
from modules.ChooseModelDlg import ChooseModelDlg

#FIXME turn to widget. Possible memory leak
class PropertiesItem():
    def __init__(self, objModel, title, objCollection, mapModel, category, tilesize=64):
        self._model = objModel
        self._mapModel = mapModel
        self._category = category

        self.widget = QGroupBox(title)
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        # Add SimpleSquareItem before properties
        self.modelPicture = SimpleSquareItem(objModel, objCollection, tilesize)
        self.layout.addWidget(self.modelPicture)

        #availableObjects = objCollection.getTypesInCategory(self._category)

        def addBoxParameter(propName, propValue, possibleValues):
            groupbox = QGroupBox(propName)
            self.layout.addWidget(groupbox)
            box = QVBoxLayout()
            groupbox.setLayout(box)

            if propName == 'rotation':
                dialogBtn = QPushButton("Choose Rotation")
                # lambda is needed to fix Qt connection issue
                dialogBtn.clicked.connect(lambda: self.showChooseRotationDlg())
                box.addWidget(dialogBtn)
            elif propName == 'model':
                dialogBtn = QPushButton("Choose Model")
                # lambda is needed to fix Qt connection issue
                dialogBtn.clicked.connect(lambda: self.showChooseModelDlg())
                box.addWidget(dialogBtn)
            else:
                # NOTE: it's useless code, but kept for the future when we might need additional properties support
                comboBox = QComboBox()
                for optionName in possibleValues:
                    comboBox.addItem(optionName, optionName)
                
                comboBox.setCurrentIndex(possibleValues.index(propValue))
                box.addWidget(comboBox)
                
                def onIndexChanged(propName, valueIdx):
                    valueStr = possibleValues[valueIdx]
                    self._model.setProperty(propName, valueStr)
                    self._mapModel.updateEntireMap()

                comboBox.currentIndexChanged.connect(partial(onIndexChanged, propName))

        addBoxParameter('model',    self._model.properties['model'], list())
        addBoxParameter('rotation', self._model.properties['rotation'], list())

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

class PropertiesPanel(QWidget):
    updatedEntireMap = pyqtSignal()
    def __init__(self, category):
        QWidget.__init__(self)

        self.x = None
        self.y = None
        self.zLevel = None
        self._category = category

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.coordinatesLbl = QLabel("X: ? Y: ?")
        layout.addWidget(self.coordinatesLbl)

        self.properties = QVBoxLayout()
        layout.addLayout(self.properties)

        addBtn = QPushButton("Add object")
        layout.addWidget(addBtn)
        addBtn.clicked.connect(self.addObject)

    def setModel(self, model):
        self.mapModel = model

    def showSquareProperties(self, x, y, z):
        self.x = x
        self.y = y
        self.zLevel = z

        for i in reversed(range(self.properties.count())):
            self.properties.itemAt(i).widget().setParent(None)

        items = self.mapModel.getSquareItems(x, y, z)
        num = 0;
        for itemModel in items:
            self.coordinatesLbl.setText("X: " + str(x) + " Y: " + str(y) + " Zlevel: " + str(z))

            num += 1;
            title = str(num)
            itemWg = PropertiesItem(itemModel, title, self.mapModel._objCollection, self.mapModel, self._category)
            self.properties.addWidget(itemWg.widget)

            removeBtn = QPushButton("Remove")
            self.properties.addWidget(removeBtn)

            removeBtn.clicked.connect(partial(self.removeObject, itemModel.id))

    def addObject(self):
        if self.x is not None and self.y is not None and self.zLevel is not None:
            obj = self.mapModel.createObjectAt(self.x, self.y, self.zLevel)
            self.showSquareProperties(self.x, self.y, self.zLevel)
            self.updatedEntireMap.emit()

    def removeObject(self, id):
        self.mapModel.deleteSquareById(id)
        self.showSquareProperties(self.x, self.y)
