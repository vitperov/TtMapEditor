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

class MapObjectType(str, Enum):
    Empty   = 'Empty'
    House   = 'House'
    Shed    = 'Shed'

class MapSquareModel(QObject):
    changed = pyqtSignal()

    def __init__(self, id):
        QObject.__init__(self)
        self.id = id

        self.classnames = dict()
        self.classnames['type']      = SquareType

        self.properties = dict()
        self.properties['type']      = SquareType.Empty

    def getXY(self):
        y = int(self.id / 1000)
        x = self.id % 1000

        return [x, y]

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

        obj['id'] =  self.id
        return obj
        

class MapObjectModel:
    def __init__(self, x, y, type):
        self.classnames = dict()
        self.classnames['type']      = MapObjectType

        self.properties = dict()
        self.properties['type']      = type
        
        self.x = x
        self.y = y

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
