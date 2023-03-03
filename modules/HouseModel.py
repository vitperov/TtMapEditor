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

class HouseSquareRotation(str, Enum):
    deg0    = '0'
    deg90   = '90'
    deg180  = '180'
    deg270  = '270'

class HouseMapSquareModel(MapObjectModelGeneral, QObject):
    changed = pyqtSignal()

    def __init__(self):
        MapObjectModelGeneral.__init__(self, 0, 0)
        QObject.__init__(self)

        self.classnames['type']      = HouseSquareType
        self.classnames['rotation']  = HouseSquareRotation

        self.properties['type']      = HouseSquareType.Empty
        self.properties['rotation']  = HouseSquareRotation.deg0

    def setProperty(self, name, value):
        print("setProperty " + name + ": " + str(value))
        variableClass = self.classnames[name]
        self.properties[name] = variableClass(value);
        self.changed.emit()

class HouseMapModel(MapModelGeneral, QObject):
    updatedEntireMap = pyqtSignal()
    def __init__(self):
        MapModelGeneral.__init__(self, HouseMapSquareModel)
        QObject.__init__(self)

        self.setUpdatedCallback(self._updateeEntireMap)

    def _updateeEntireMap(self):
        self.updatedEntireMap.emit()

