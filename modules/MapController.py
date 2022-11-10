import sys
from functools import partial
import datetime

from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui
import numpy


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class MapController:
    def __init__(self, view, mapModel):
        self._view = view
        self._mapModel = mapModel

        #self._provideModel()
        self._connectSignals()

    #def _provideModel(self):
    #    self._view.houseMapPanel.setModel(self._houseModel)


    def _connectSignals(self):
        #self._view.mapPanel.activeItemChanged.connect(self._onHouseSquareClicked)
        #self._mapModel.updatedEntireMap.connect(self._view.houseMapPanel.redrawAll)
        print("Stub")
