import math
from random import randrange, random

from modules.TerrainMapModel import *
from modules.GeometryPrimitives import *


class MapEditor():
    def __init__(self, model):
        self._model = model

    def fillArea(self, startPt, size, property, value):
        for row in range(startPt.y, startPt.y + size.h):
            for column in range(startPt.x, startPt.x + size.w):
                square = self._model.getSquareXY(row, column)
                square.setProperty(property, value)
                
    def fillAreaBorder(self, startPt, size, type, width=1):
        self.fillArea(startPt,                                      AreaSize(size.w, width), 'type', type)
        self.fillArea(Point(startPt.x ,startPt.y + size.h - width), AreaSize(size.w, width), 'type', type)
        self.fillArea(startPt,                                      AreaSize(width, size.h), 'type', type)
        self.fillArea(Point(startPt.x + size.w - width, startPt.y), AreaSize(width, size.h), 'type', type)

class ZoneSettings():
    def __init__(self):
        self.size = AreaSize(15, 20)
        self.roadWidth = 2

        # TODO: randomly choose house
        self.houseSize = AreaSize(7, 7)
        self.houseProb = 0.9

        self.shedSize = AreaSize(2, 2)
        self.shedProb = 0.5

class MapGenerator():
    def __init__(self, model):
        self._model = model
        self._editor = MapEditor(model)

        self._rows = 2
        self._columns = 5

        self._zoneSettings = ZoneSettings()

        self._forestKeepOut = 3
        self._roadWidth = 2

        self._calcMapSize()

        self._currentZoneId = 0

    def _calcMapSize(self):
        self._w = self._zoneSettings.size.w * self._columns + 2 * self._forestKeepOut
        self._h = self._zoneSettings.size.h * self._rows + 2 * self._forestKeepOut + self._zoneSettings.roadWidth

    def generateMap(self):
        print("Generating map size=" + str(self._h) + "x" + str(self._w))
        self._model.newMap(self._w, self._h)

        self.fillEverythingGrass()
        self.genKeepOutForest()
        self.genRoad()
        self.genZones()

    def fillEverythingGrass(self):
        self._editor.fillArea(Point(0,0), AreaSize(self._w, self._h), 'type', SquareType.Grass)

    def genKeepOutForest(self):
        self._editor.fillAreaBorder(Point(0,0),  AreaSize(self._w, self._h),
            SquareType.Forest, width=self._forestKeepOut)

    def genRoad(self):
        #FIXME: do road after every zone height
        halfHeight = math.ceil(self._h / 2)
        self._editor.fillArea(Point(0, halfHeight - 1), AreaSize(self._w, 2), 'type', SquareType.Road)

    def genZones(self):
        for row in range(self._rows):
            for column in range(self._columns):
                print("Generating zone. Row=" + str(row) + " column=" + str(column))
                startPt = Point(column * self._zoneSettings.size.w + self._forestKeepOut,
                                row * self._zoneSettings.size.h + self._forestKeepOut)

                #if (row != 0) and (row != self._rows - 1):
                if row != 0:
                    startPt.y += self._zoneSettings.roadWidth;
                    print("    -->Add road offset")

                print("    startPt=" + str(startPt))
                self.genZone(startPt)
                self._currentZoneId += 1

    def genZone(self, startPt):
        zone = ZoneGenerator(self._model, startPt)
        zone.generate(self._zoneSettings)

                        

class ZoneGenerator:
    def __init__(self, model, startPt):
        self._model = model
        self._editor = MapEditor(model)
        self.startPt = startPt

    def generate(self, settings):
        # Debug zone location
        #self.fillAreaBorder(startPt, self._zoneSize, SquareType.Empty)

        generateHouse = (random() < settings.houseProb)

        if not generateHouse:
            return # it it's no house, no need to generate shed

        zoneKeepout = 1
        houseKeepout = 1

        zoneRect = Rectangle(Point(0,0), settings.size)
        #print("    Orig rect=" + str(zoneRect))
        zoneRect.shrink(zoneKeepout)
        print("    Shrinked rect=" + str(zoneRect))

        def genRandomObjPlace(zoneRect, objSize):
            x = randrange(zoneRect.pt.x, zoneRect.pt.x + zoneRect.sz.w - objSize.w)
            y = randrange(zoneRect.pt.y, zoneRect.pt.y + zoneRect.sz.h - objSize.h)
            return Point(x, y)

        houseRelative = genRandomObjPlace(zoneRect, settings.houseSize)
        print("    House placed at: " + str(houseRelative))

        houseAbs = houseRelative + self.startPt;

        print("        abs position: " + str(houseAbs))
        self._editor.fillArea(houseAbs, settings.houseSize, 'type', SquareType.House)

        houseObj = MapObjectModel(houseAbs.x, houseAbs.y, MapObjectType.House)
        self._model.addMapObject(houseObj)

        generateShed = (random() < settings.shedProb)

        if generateShed:
            houseRectRel = Rectangle(houseRelative, settings.houseSize)
            houseRectRel.expand(houseKeepout)

            placeOk = False
            while not placeOk:
                shedRel = genRandomObjPlace(zoneRect, settings.shedSize)
                shedRect = Rectangle(shedRel, settings.shedSize)
                placeOk = not houseRectRel.isRectPartiallyInside(shedRect)

            shedAbs = shedRel + self.startPt
            self._editor.fillArea(shedAbs, settings.shedSize, 'type', SquareType.Shed)

            shedObj = MapObjectModel(shedAbs.x, shedAbs.y, MapObjectType.Shed)
            self._model.addMapObject(shedObj)

