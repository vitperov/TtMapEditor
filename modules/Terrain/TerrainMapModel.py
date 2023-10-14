from enum import Enum
from PyQt5.QtCore import *

from modules.MapModelGeneral import *

class SquareType(str, Enum):
    Empty   = 'Empty'
    Grass   = 'Grass'
    Forest  = 'Forest'
    Road    = 'Road'
    House   = 'House'
    Shed    = 'Shed'
    Respawn = 'Respawn'

class MapObjectType(str, Enum):
    Empty   = 'Empty'
    House   = 'House'
    Shed    = 'Shed'
    

class MapObjectModel(MapObjectModelGeneral):
    def __init__(self, x, y, type):
        MapObjectModelGeneral.__init__(self, x, y)

        self.classnames['model'] = str
        self.properties['model'] = type

class MapSquareModel(QObject):
    changed = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)
        self.x = 0
        self.y = 0

        self.classnames = dict()
        self.classnames['type']      = SquareType

        self.properties = dict()
        self.properties['type']      = SquareType.Empty

    def setProperty(self, name, value):
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

        obj['x'] =  self.x
        obj['y'] =  self.y
        return obj
        

class TerrainMapModel(MapModelGeneral, QObject):
    updatedEntireMap = pyqtSignal()
    def __init__(self):
        MapModelGeneral.__init__(self, MapSquareModel)
        QObject.__init__(self)
        
        self.setUpdatedCallback(self._updateeEntireMap)
        
    def _updateeEntireMap(self):
        self.updatedEntireMap.emit()
