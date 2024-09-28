try:
    import PyQt5
    PyQt = 'PyQt5'
except:
    import PyQt4
    PyQt = 'PyQt4'
    
#def dynamic_import (module_full_name, target_name):
#    tmp = __import__(module_full_name)
#    return getattr(tmp, target_name)
#    
#def dynamic_import_from (module_full_name, target_names = ['*',], update_globals = True):
#    tmp = __import__(module_full_name, fromlist = target_names)
#    if (update_globals):
#        #print(tmp.__dict__)
#        was_star = False
#        for name in target_names:
#            if ('*' == name):
#                was_star = True
#                continue
#            print(name)
#            value = getattr(tmp, name)
#            globals()[name] = value
#        if (was_star):
#            globals().update(tmp.__dict__)
#    return tmp

import sys
from functools import partial
import datetime

from PyQt5 import QtWidgets #QtWidgets = dynamic_import(str(PyQt),  'QtWidgets') #
from pyqtgraph.Qt import QtCore, QtGui
import numpy


from PyQt5.QtCore import * #dynamic_import_from(str(PyQt) + '.QtCore', ['*']) #
from PyQt5.QtWidgets import * #dynamic_import_from(str(PyQt) + '.QtWidgets', ['*']) #

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
        self._view.actionsPanel.openMap.connect(self._model.map.openMap)
        self._view.actionsPanel.saveMap.connect(self._model.map.saveMap)
        self._view.actionsPanel.mapSettings.connect(self._onSettingsClick)
        self._view.actionsPanel.refreshMap.connect(self._view.mapWidget.redrawAll)

    def _connectSignals(self):
        self._model.map.updatedEntireMap.connect(self._view.mapWidget.redrawAll)
        self._view.mapWidget.activeItemChanged.connect(self._onSquareClicked)

    def _startActions(self):
        self._view.generatorsPanel.populateGenerators(self._model.generators.generators)

    def _onSettingsClick(self):
        TerrainGeneratorSettingsDlg.runDlg("Terrain generator settings", \
            self._model.generators.generators[1][2].settings, self._view) # EverythingGenerator was renamed to LandLotContentGenerator

    def _onSquareClicked(self, x, y):
        #model = self._houseModel.getSquare(x, y)
        # TODO: delete wrapper and call directly
        self._view.propPanel.showSquareProperties(x, y)

