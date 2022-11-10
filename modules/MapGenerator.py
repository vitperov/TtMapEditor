
class AreaSize:
    def __init__(self, w, h):
        self.w = w
        self.h = h


class MapGenerator():
    def __init__(self, model):
        self._model = model
        
        self._rows = 2
        self._columns = 5
        
        self._zoneSize = AreaSize(15, 20)
        
        self._forestKeepOut = 1
        self._roadWidth = 2
        
        self._w = self._zoneSize.w * self._columns + 2 * self._forestKeepOut
        self._h = self._zoneSize.h * self._rows + 2 * self._forestKeepOut + self._roadWidth

    def generateMap(self):
        #Only one type of map is supported
        #h = 44
        #w = 78
        self._model.newMap(self._w, self._h)
        
        
    def genZone():
        print("Stub")
        
    def genRoad():
        print("Stub")


