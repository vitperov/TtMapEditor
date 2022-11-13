import math
from random import randrange, random

from modules.MapModel import *
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
        self._houseProb = 0.9

        self._shedSize = AreaSize(2, 2)
        self._shedProb = 0.5 #probability
        
        self._currentZoneId = 0

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
        
    def fillAreaBorder(self, startPt, size, type):
        self.fillArea(startPt,                                  AreaSize(size.w, 1), 'type', type)
        self.fillArea(Point(startPt.x ,startPt.y + size.h - 1), AreaSize(size.w, 1), 'type', type)
        self.fillArea(startPt,                                  AreaSize(1, size.h), 'type', type)
        self.fillArea(Point(startPt.x + size.w - 1, startPt.y), AreaSize(1, size.h), 'type', type)

    def genKeepOutForest(self):
        self.fillAreaBorder(Point(0,0),  AreaSize(self._w, self._h), SquareType.Forest)

    def genRoad(self):
        #FIXME: do road after every zone height
        halfHeight = math.ceil(self._h / 2)
        self.fillArea(Point(0, halfHeight - 1), AreaSize(self._w, 2), 'type', SquareType.Road)

    def genZones(self):
        for row in range(self._rows):
            for column in range(self._columns):
                print("Generating zone. Row=" + str(row) + " column=" + str(column))
                startPt = Point(column * self._zoneSize.w + self._forestKeepOut,
                                row * self._zoneSize.h + self._forestKeepOut)

                #if (row != 0) and (row != self._rows - 1):
                if row != 0:
                    startPt.y += self._roadWidth;
                    print("    -->Add road offset")

                print("    startPt=" + str(startPt))
                self.genZone(startPt)
                self._currentZoneId += 1

    def genZone(self, startPt):
        # Debug zone location
        #self.fillAreaBorder(startPt, self._zoneSize, SquareType.Empty)

        generateHouse = (random() < self._houseProb)
        
        if not generateHouse:
            return # it it's no house, no need to generate shed
        
        zoneKeepout = 1
        houseKeepout = 1
        
        zoneRect = Rectangle(Point(0,0), self._zoneSize)
        #print("    Orig rect=" + str(zoneRect))
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
        
        houseObj = MapObjectModel(houseAbs.x, houseAbs.y, MapObjectType.House)
        self._model.addMapObject(houseObj)
        
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
            
            shedObj = MapObjectModel(shedAbs.x, shedAbs.y, MapObjectType.Shed)
            self._model.addMapObject(shedObj)
        

