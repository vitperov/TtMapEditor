import sys
from functools import partial
import datetime

from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui
import numpy


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from modules.Terrain.TerrainGeneratorSettingsDlg import *

class TerrainMapController:
    def __init__(self, view, model):
        self._view = view
        self._model = model

        self._provideModel()
        self._connectSignals()
        self._startActions()

    def _provideModel(self):
        self._view.mapWidget.setModel(self._model.map)
        self._view.propPanel.setModel(self._model.map)
        self._view.actionsPanel.saveMap.connect(self._model.map.saveMap)
        self._view.actionsPanel.mapSettings.connect(self._onSettingsClick)

    def _connectSignals(self):
        self._model.map.updatedEntireMap.connect(self._view.mapWidget.redrawAll)
        self._view.mapWidget.activeItemChanged.connect(self._onSquareClicked)

    def _startActions(self):
        self._view.generatorsPanel.populateGenerators(self._model.generators.generators)

    def _onSettingsClick(self):
        TerrainGeneratorSettingsDlg.runDlg("Terrain generator settings", \
            self._model.generators.generators['EverythingGenerator'].settings, self._view)

    def _onSquareClicked(self, x, y):
        #model = self._houseModel.getSquare(x, y)
        # TODO: delete wrapper and call directly
        self._view.propPanel.showSquareProperties(x, y)

