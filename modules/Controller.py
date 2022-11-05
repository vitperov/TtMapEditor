import sys
from functools import partial
import datetime

from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui
import numpy


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Stream(QtCore.QObject):
    newText = QtCore.pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))

class Controller:
    def __init__(self, view, houseModel):
        """Controller initializer."""
        self._view = view
        self._houseModel = houseModel

        self._provideModel()
        self._connectSignals()
        
    def _provideModel(self):
        self._view.houseMapPanel.setModel(self._houseModel)
        

    def _connectSignals(self):
        """Connect signals and slots."""
        #self._view.houseMapPanel.activeItemChanged.connect(self._view.propPanel.showItem)
        self._view.houseMapPanel.activeItemChanged.connect(self._onHouseSquareClicked)
        #self._view.propPanel.
        self._view.actionsPanel.newMap.connect(self._houseModel.newMap)
        self._view.actionsPanel.openMap.connect(self._houseModel.openMap)
        self._view.actionsPanel.saveMap.connect(self._houseModel.saveMap)
        
        self._houseModel.updatedEntireMap.connect(self._view.houseMapPanel.redrawAll)
        
    def _onHouseSquareClicked(self, squareId):
        model = self._houseModel.getSquare(squareId)
        self._view.propPanel.showSquareProperties(model)
        

        
