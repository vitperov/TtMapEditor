from enum import Enum
from PyQt5.QtCore import *

from modules.MapModelGeneral import *

class MapObjectType(str, Enum):
    Empty   = 'Empty'
    House   = 'House'
    Shed    = 'Shed'

class TerrainMapModel(MapModelGeneral, QObject):
    updatedEntireMap = pyqtSignal()
    def __init__(self, objCollection):
        MapModelGeneral.__init__(self, MapObjectModelGeneral, objCollection)
        QObject.__init__(self)
        
        self.setUpdatedCallback(self._updateEntireMap)
        
    def _updateEntireMap(self):
        self.updatedEntireMap.emit()
