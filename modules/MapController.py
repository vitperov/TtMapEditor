import sys
from functools import partial
import datetime

from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui
import numpy


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from modules.GeneratorSettingsDlg import *

class MapController:
    def __init__(self, view, model, generator):
        self._view = view
        self._mapModel = model
        self._generator = generator

        self._provideModel()
        self._connectSignals()

    def _provideModel(self):
        self._view.mapWidget.setModel(self._mapModel)

        #self._view.actionsPanel.generateMap.connect(self._generator.generateMap)
        self._view.actionsPanel.generateMap.connect(self._onGenerateClick)
        self._view.actionsPanel.saveMap.connect(self._mapModel.saveMap)
        self._view.actionsPanel.mapSettings.connect(self._onSettingsClick)

    def _connectSignals(self):
        #self._view.mapWidget.activeItemChanged.connect(self._onHouseSquareClicked)
        self._mapModel.updatedEntireMap.connect(self._view.mapWidget.redrawAll)
        print("Stub")

    def _onGenerateClick(self):
        self._generator.loadSettings()
        self._generator.generateMap()

    def _onSettingsClick(self):
        GeneratorSettingsDlg.runDlg("Terrain generator settings", \
            self._generator.settings, modal=False)
