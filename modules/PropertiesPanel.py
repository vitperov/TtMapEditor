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
    def __init__(self):
        QWidget.__init__(self)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.coordinatesLbl = QLabel("X: ? Y: ?")
        layout.addWidget(self.coordinatesLbl)
        
        self.properties = QHBoxLayout()
        layout.addLayout(self.properties)
    
        addBtn = QPushButton("Add object")
        layout.addWidget(addBtn)

    def setModel(self, model):
        self.mapModel = model

    def showSquareProperties(self, x, y):
        for i in reversed(range(self.properties.count())):
            self.properties.itemAt(i).widget().setParent(None)
        
        items = self.mapModel.getSquareItems(x, y)
        num = 0;
        for itemModel in items:
            x = itemModel.x
            y = itemModel.y
            self.coordinatesLbl.setText("X: " + str(x) + " Y: " + str(y))

            num += 1;
            title = str(num)
            itemWg = PropertiesItem(itemModel, title)
            self.properties.addWidget(itemWg.widget)

