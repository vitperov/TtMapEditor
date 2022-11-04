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
        
        
    def _onHouseSquareClicked(self, squareId):
        model = self._houseModel.getSquare(squareId)
        self._view.propPanel.showSquareProperties(model)
        

        
