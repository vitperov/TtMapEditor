from PyQt5.QtCore import *

from modules.MapModelGeneral import *


class HouseMapModel(MapModelGeneral, QObject):
    updatedEntireMap = pyqtSignal()
    def __init__(self, objCollection):
        MapModelGeneral.__init__(self, MapObjectModelGeneral, objCollection)
        QObject.__init__(self)
        
        self.editorWidth = 8;
        self.editorHeight = 8;

        self.setUpdatedCallback(self._updateeEntireMap)

    def _updateeEntireMap(self):
        self.updatedEntireMap.emit()

