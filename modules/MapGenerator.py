import math
from modules.MapModel import SquareType

class AreaSize:
    def __init__(self, w, h):
        self.w = w
        self.h = h

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


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
        print("Generating map size=" + str(self._h) + "x" + str(self._w))
        self._model.newMap(self._w, self._h)

        self.fillEverythingGrass()
        self.genKeepOutForest()
        self.genRoad()


    def fillArea(self, startPt, size, property, value):
        for row in range(startPt.y, startPt.y + size.h):
            for column in range(startPt.x, startPt.x + size.w):
                square = self._model.getSquareXY(row, column)
                square.setProperty(property, value)
                
    def fillEverythingGrass(self):
        self.fillArea(Point(0,0), AreaSize(self._w, self._h), 'type', SquareType.Grass)

    def genKeepOutForest(self):
        self.fillArea(Point(0,0),           AreaSize(self._w, 1), 'type', SquareType.Forest)
        self.fillArea(Point(0,self._h -1),  AreaSize(self._w, 1), 'type', SquareType.Forest)
        self.fillArea(Point(0,0),           AreaSize(1, self._h), 'type', SquareType.Forest)
        self.fillArea(Point(self._w -1, 0), AreaSize(1, self._h), 'type', SquareType.Forest)
        
    def genRoad(self):
        #FIXME: do road after every zone height
        halfHeight = math.ceil(self._h / 2)
        self.fillArea(Point(0, halfHeight - 1), AreaSize(self._w, 2), 'type', SquareType.Road)

    def genZone():
        print("Stub")

