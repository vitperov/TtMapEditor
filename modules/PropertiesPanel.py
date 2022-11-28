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
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        for propName, propValue in self._model.properties.items():
            groupbox = QGroupBox(propName)
            self.layout.addWidget(groupbox)
            box = QVBoxLayout()
            groupbox.setLayout(box)
            #print(propName + "->" + str(propValue.value))

            valType = type(propValue)
            # assume valType is Enum
            nValues = len(valType)
            for option in list(valType):
                #print("    " + option.name + "->" + str(option.value))
                btn = QRadioButton(option.name)
                #print("    Checked = " + str(option.value == propValue.value))
                if option.value == propValue.value:
                    btn.setChecked(True)
                #btn.setChecked(option.value == propValue)
                box.addWidget(btn)

                btn.pressed.connect(partial(self._model.setProperty, propName, option.value))




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

        self.properties = QHBoxLayout()
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

