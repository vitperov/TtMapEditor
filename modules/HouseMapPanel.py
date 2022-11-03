from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from functools import partial

from modules.HouseMapItem import *
    
class HouseMapPanel(QWidget):
    def __init__(self, width, heigth):
        QWidget.__init__(self)
        self._layout = QGridLayout()
        self._items = {}
        self.setLayout(self._layout)
        
        for column in range(width):
            for row in range(heigth):
                id = row*1000 + column
                item = HouseMapItem(id)
                self._layout.addWidget(item, row, column)


    #def _onSetClicked(self, name):
    #    if self._model is None:
    #        raise NoModelDefinedException
    #
    #    value = self._variables[name].edit.text()
    #    self._model.setVariable(name, value)


    def populateModelVariables(self, model):
        print("populateModelVariables")

    def _connectVariables(self):
        for name in self._variables:
            #FIXME: getters and setters should be implemented inside item class
            try:
                self._variables[name].setBtn.clicked.connect(partial(self._onSetClicked, name))
            except Exception:
                pass
            try:
                self._variables[name].getBtn.clicked.connect(partial(self._onGetClicked, name))
            except Exception:
                pass
            try:
                self._variables[name].cmdBtn.clicked.connect(partial(self._onCmdClicked, name))
            except Exception:
                pass

