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


class HouseMapSquareModel(QObject):
    changed = pyqtSignal()

    def __init__(self, id):
        QObject.__init__(self)
        self.id = id

        self.classnames = dict()
        self.classnames['type']      = HouseSquareType
        self.classnames['rotation']  = HouseSquareRotation
        self.classnames['territory'] = HouseSquareTerritory

        self.properties = dict()
        self.properties['type']      = HouseSquareType.Empty
        self.properties['rotation']  = HouseSquareRotation.deg0
        self.properties['territory'] = HouseSquareTerritory.Empty

    def getXY(self):
        y = int(self.id / 1000)
        x = self.id % 1000

        return [x, y]

    def setProperty(self, name, value):
        print("setProperty " + name + ": " + str(value))
        variableClass = self.classnames[name]
        self.properties[name] = variableClass(value);
        self.changed.emit()

    def getProperty(self, name):
        return self.properties[name]

    def toSerializableObj(self):
        # properties are enums, they can't be directly converted to int
        obj = dict()
        for name, prop in self.properties.items():
            value = prop
            obj[name] = value

        obj['id'] =  self.id
        return obj

    def restoreFromJson(self, js):
        self.id = js['id']
        self.properties['type']      = HouseSquareType(js['type'])
        self.properties['rotation']  = HouseSquareRotation(js['rotation'])
        self.properties['territory'] = HouseSquareTerritory(js['territory'])

class HouseMapModel(MapModelGeneral, QObject):
    updatedEntireMap = pyqtSignal()
    def __init__(self):
        MapModelGeneral.__init__(self, HouseMapSquareModel)
        QObject.__init__(self)
        
        self.setUpdatedCallback(self._updateeEntireMap)
        
    def _updateeEntireMap(self):
        self.updatedEntireMap.emit()

