import math
from random import randrange

from modules.MapModel import SquareType

class AreaSize:
    def __init__(self, w, h):
        self.w = w
        self.h = h

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __add__(self, pt):
        return Point(self.x + pt.x, 
                     self.y + pt.y)

    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


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

        # TODO: randomly choose house
        self._houseSize = AreaSize(7, 7)

    def generateMap(self):
        print("Generating map size=" + str(self._h) + "x" + str(self._w))
        self._model.newMap(self._w, self._h)

        self.fillEverythingGrass()
        self.genKeepOutForest()
        self.genRoad()
        self.genZones()

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

    def genZones(self):
        for row in range(self._rows):
            for column in range(self._columns):
                print("Generating zone. Row=" + str(row) + " column=" + str(column))
                startPt = Point(column * self._zoneSize.w,
                                row * self._zoneSize.h)

                #if (row != 0) and (row != self._rows - 1):
                if row != 0:
                    startPt.y += self._roadWidth;
                    print("    -->Add road offset")

                self.genZone(startPt)

    def genZone(self, startPt):
        zoneKeepout = 1
        xRange = self._zoneSize.w - 2*zoneKeepout - self._houseSize.w
        yRange = self._zoneSize.h - 2*zoneKeepout - self._houseSize.h

        houseRelative = Point(randrange(0,xRange) + zoneKeepout,
                              randrange(0, yRange)+ zoneKeepout)
        print("    House placed at: " + str(houseRelative))
        
        houseAbs = houseRelative + startPt;
        
        print("        abs position: " + str(houseAbs))
        self.fillArea(houseAbs, self._houseSize, 'type', SquareType.House)

