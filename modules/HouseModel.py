from enum import Enum
from PyQt5.QtCore import *

import json

from modules.MapModelGeneral import *

class HouseSquareType(str, Enum):
    Empty   = 'Empty'
    Corner  = 'Corner'
    Wall    = 'Wall'
    Door    = 'Door'
    Window  = 'Window'
    Floor   = 'Floor'

class HouseSquareRotation(str, Enum):
    deg0    = '0'
    deg90   = '90'
    deg180  = '180'
    deg270  = '270'

class HouseSquareTerritory(str, Enum):
    Empty       = 'Empty'
    Kitchen     = 'Kitchen'
    Bedroom     = 'Bedroom'
    LivingRoom  = 'LivingRoom'
    StoreRoom   = 'StoreRoom'


class HouseMapSquareModel(MapObjectModelGeneral, QObject):
    changed = pyqtSignal()

    def __init__(self):
        MapObjectModelGeneral.__init__(self, 0, 0)
        QObject.__init__(self)
        
        self.classnames['type']      = HouseSquareType
        self.classnames['rotation']  = HouseSquareRotation
        #self.classnames['territory'] = HouseSquareTerritory

        self.properties['type']      = HouseSquareType.Empty
        self.properties['rotation']  = HouseSquareRotation.deg0
        #self.properties['territory'] = HouseSquareTerritory.Empty

    def setProperty(self, name, value):
        print("setProperty " + name + ": " + str(value))
        variableClass = self.classnames[name]
        self.properties[name] = variableClass(value);
        self.changed.emit()

    #def restoreFromJson(self, js):
    #    self.x = js['x']
    #    self.y = js['y']
    #
    #    self.properties['type']      = HouseSquareType(js['type'])
    #    self.properties['rotation']  = HouseSquareRotation(js['rotation'])
    #    self.properties['territory'] = HouseSquareTerritory(js['territory'])

class HouseMapModel(MapModelGeneral, QObject):
    updatedEntireMap = pyqtSignal()
    def __init__(self):
        MapModelGeneral.__init__(self, HouseMapSquareModel)
        QObject.__init__(self)

        self.setUpdatedCallback(self._updateeEntireMap)

    def _updateeEntireMap(self):
        self.updatedEntireMap.emit()

