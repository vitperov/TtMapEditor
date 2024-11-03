import sys
from functools import partial
import datetime

from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui
import numpy


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class HouseController:
    def __init__(self, view, houseModel):
        self._view = view
        self._houseModel = houseModel

        self._provideModel()
        self._connectSignals()

    def _provideModel(self):
        self._view.mapWidget.setModel(self._houseModel)
        self._view.propPanel.setModel(self._houseModel)

    def _connectSignals(self):
        self._view.mapWidget.activeItemChanged.connect(self._onHouseSquareClicked)
        self._view.actionsPanel.newMap.connect(self._houseModel.newMap)
        self._view.actionsPanel.openMap.connect(self._houseModel.openMap)
        self._view.actionsPanel.saveMap.connect(self._houseModel.saveMap)
        self._view.actionsPanel.addColumn.connect(self._houseModel.addColumn)
        self._view.actionsPanel.addRow.connect(self._houseModel.addRow)
        self._view.actionsPanel.zLevelChanged.connect(self._setZLevel)
        self._view.actionsPanel.changedSelection.connect(self._view.mapWidget.onMultipleSelectionChanged)

        self._houseModel.updatedEntireMap.connect(self._view.mapWidget.redrawAll)
        self._view.propPanel.updatedEntireMap.connect(self._view.mapWidget.redrawAll)

        self._view.mapWidget.deleteRow.connect(self._houseModel.deleteRow)
        self._view.mapWidget.deleteColumn.connect(self._houseModel.deleteColumn)

    def _onHouseSquareClicked(self, x, y, z):
        #model = self._houseModel.getSquare(x, y)
        # TODO: delete wrapper and call directly
        self._view.propPanel.showSquareProperties(x, y, z)

    def _setZLevel(self, zLevel):
        self._view.mapWidget.zLevel = zLevel
        self._view.mapWidget.redrawAll()
