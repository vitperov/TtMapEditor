from enum import Enum
from PyQt5.QtCore import *

from modules.MapModelGeneral import *

class HouseSquareType(str, Enum):
    Empty       = 'Empty'
    Corner      = 'Corner'
    Wall        = 'Wall'
    Door        = 'Door'
    Window      = 'Window'
    Floor       = 'Floor'
    CornerInt   = 'CornerInternal'
    WallInt     = 'WallInternal'
    DoorInt     = 'DoorInternal'
    Wardrobe    = 'Wardrobe'
    Bed2p       = 'Bed2p'
    Drawer      = 'Drawer'
    SinkOven    = 'SinkOven'
    Fridge      = 'Fridge'
    Counter     = 'Counter'
    Sofa        = 'Sofa'
    TableChairs = 'TableChairs'
    Bookshelf   = 'Bookshelf'
    Light       = 'Light'
    Toilet      = 'Toilet'


class HouseMapSquareModel(MapObjectModelGeneral, QObject):
    changed = pyqtSignal()

    def __init__(self):
        MapObjectModelGeneral.__init__(self, 0, 0)
        QObject.__init__(self)

        self.classnames['type']      = HouseSquareType
        self.properties['type']      = HouseSquareType.Empty

    def setProperty(self, name, value):
        print("setProperty " + name + ": " + str(value))
        variableClass = self.classnames[name]
        self.properties[name] = variableClass(value);
        self.changed.emit()

class HouseMapModel(MapModelGeneral, QObject):
    updatedEntireMap = pyqtSignal()
    def __init__(self, objCollection):
        MapModelGeneral.__init__(self, HouseMapSquareModel, objCollection)
        QObject.__init__(self)
        
        self.editorWidth = 8;
        self.editorHeight = 8;

        self.setUpdatedCallback(self._updateeEntireMap)

    def _updateeEntireMap(self):
        self.updatedEntireMap.emit()

