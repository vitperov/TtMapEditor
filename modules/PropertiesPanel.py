from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from functools import partial


class PropertiesPanel(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.coordinatesLbl = QLabel("X: ? Y: ?")
        layout.addWidget(self.coordinatesLbl)
        
        self._propertiesLayout = QVBoxLayout()
        layout.addLayout(self._propertiesLayout)
        
        
    def showSquareProperties(self, squareModel):
        [x, y] = squareModel.getXY()
        self.coordinatesLbl.setText("X: " + str(x) + " Y: " + str(y))
        
        for i in reversed(range(self._propertiesLayout.count())): 
            self._propertiesLayout.itemAt(i).widget().setParent(None)

        for propName, propValue in squareModel.properties.items():
            groupbox = QGroupBox(propName)
            self._propertiesLayout.addWidget(groupbox)
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
                
                btn.pressed.connect(partial(squareModel.setProperty, propName, option.value))

