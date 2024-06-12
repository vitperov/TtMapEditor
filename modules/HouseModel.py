from PyQt5.QtCore import *

from modules.MapModelGeneral import *

class HouseMapSquareModel(MapObjectModelGeneral):

    def __init__(self):
        MapObjectModelGeneral.__init__(self, 0, 0)

        self.classnames['model']      = str
        self.properties['model']      = "Empty"

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

