from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class PropertiesPanel(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self.coordinatesLbl = QLabel("X: Y:")
        self._layout.addWidget(self.coordinatesLbl)
        
    def showItem(self, itemId):
        x = int(itemId / 1000)
        y = itemId % 1000
        
        self.coordinatesLbl.setText("X: " + str(x) + " Y: " + str(y))
