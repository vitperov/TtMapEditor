from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class PropertiesPanel(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        
        self._model = None
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self.coordinatesLbl = QLabel("X: ? Y: ?")
        self._layout.addWidget(self.coordinatesLbl)
        
        
    def showSquareProperties(self, squareModel):
        [x, y] = squareModel.getXY()
        self.coordinatesLbl.setText("X: " + str(x) + " Y: " + str(y))
        #properties = squareModel.properties
        for propName, propValue in squareModel.properties.items():
            groupbox = QGroupBox(propName)
            self._layout.addWidget(groupbox)
            vbox = QHBoxLayout()
            groupbox.setLayout(vbox)
            
            valType = type(propValue)
            # assume valType is Enum
            nValues = len(valType)
            for option in list(valType):
                print("    " + option.name + "->" + str(option.value))
                btn = QRadioButton(option.name)
                btn.setChecked(option.value == propValue)
                vbox.addWidget(btn)

