from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from functools import partial

#FIXME turn to widget. Possible memory leak
class PropertiesItem():
    def __init__(self, objModel, title):
        self._model = objModel

        self.widget = QGroupBox(title)
        self.layout = QHBoxLayout()
        self.widget.setLayout(self.layout)

        for propName, propValue in self._model.properties.items():
            groupbox = QGroupBox(propName)
            self.layout.addWidget(groupbox)
            box = QVBoxLayout()
            groupbox.setLayout(box)

            valType = type(propValue)
            # assume valType is Enum
            nValues = len(valType)
            
            comboBox = QComboBox()
            for option in list(valType):
                comboBox.addItem(option.name, option.name)
                if option.value == propValue.value:
                    comboBox.setCurrentIndex(comboBox.count() - 1)
            box.addWidget(comboBox)
            
            def onIndexChanged(propName, valueIdx):
                prop = self._model.properties[propName]
                values = list(type(prop))
                valueStr = values[valueIdx].value
                self._model.setProperty(propName, valueStr)

            comboBox.currentIndexChanged.connect(partial(onIndexChanged, propName))

class PropertiesPanel(QWidget):
    updatedEntireMap = pyqtSignal()
    def __init__(self):
        QWidget.__init__(self)

        self.x = None
        self.y = None

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

    def showSquareProperties(self, x, y):
        self.x = x
        self.y = y

        for i in reversed(range(self.properties.count())):
            self.properties.itemAt(i).widget().setParent(None)

        items = self.mapModel.getSquareItems(x, y)
        num = 0;
        for itemModel in items:
            self.coordinatesLbl.setText("X: " + str(x) + " Y: " + str(y))

            num += 1;
            title = str(num)
            itemWg = PropertiesItem(itemModel, title)
            self.properties.addWidget(itemWg.widget)

            removeBtn = QPushButton("Remove")
            self.properties.addWidget(removeBtn)

            removeBtn.clicked.connect(partial(self.removeObject, itemModel.id))

    def addObject(self):
        if self.x is not None and self.y is not None:
            obj = self.mapModel.createObjectAt(self.x, self.y)
            self.showSquareProperties(self.x, self.y)
            self.updatedEntireMap.emit()

    def removeObject(self, id):
        self.mapModel.deleteSquareById(id)
        self.showSquareProperties(self.x, self.y)

