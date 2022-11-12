import math
from random import randrange, random

from modules.MapModel import SquareType
from modules.GeometryPrimitives import *

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

        self._shedSize = AreaSize(1, 1)
        self._shedProb = 0.5 #probability

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
        houseKeepout = 1
        
        zoneRect = Rectangle(Point(0,0), self._zoneSize)
        zoneRect.shrink(zoneKeepout)
        print("    Shrinked rect=" + str(zoneRect))
        
        def genRandomObjPlace(zoneRect, objSize):
            x = randrange(zoneRect.pt.x, zoneRect.pt.x + zoneRect.sz.w - objSize.w)
            y = randrange(zoneRect.pt.y, zoneRect.pt.y + zoneRect.sz.h - objSize.h)
            return Point(x, y)

        houseRelative = genRandomObjPlace(zoneRect, self._houseSize)
        print("    House placed at: " + str(houseRelative))

        houseAbs = houseRelative + startPt;

        print("        abs position: " + str(houseAbs))
        self.fillArea(houseAbs, self._houseSize, 'type', SquareType.House)
        
        generateShed = (random() < self._shedProb)
        
        if generateShed:
            houseRectRel = Rectangle(houseRelative, self._houseSize)
            houseRectRel.expand(houseKeepout)
        
            placeOk = False
            while not placeOk:
                shedRel = genRandomObjPlace(zoneRect, self._shedSize)
                shedRect = Rectangle(shedRel, self._shedSize)
                placeOk = not houseRectRel.isRectPartiallyInside(shedRect)
                
            shedAbs = shedRel + startPt
            self.fillArea(shedAbs, self._shedSize, 'type', SquareType.Shed)
        

