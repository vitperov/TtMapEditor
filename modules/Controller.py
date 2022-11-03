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
    def __init__(self, view, model):
        """Controller initializer."""
        self._view = view
        self._model = model

        self._populateView()
        self._connectSignals()
        
    def _onUpdateFirmwareClicked(self):
        filename = self._view.firmwareEdit.text()
        self._model.updateFirmware(filename)

    def _populateView(self):
        self._view.houseMapPanel.populateModelVariables(self._model)
        

    def _connectSignals(self):
        """Connect signals and slots."""
        self._view.houseMapPanel.activeItemChanged.connect(self._view.propPanel.showItem)

        
