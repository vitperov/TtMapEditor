import math
from copy import copy
from random import randrange, random

from modules.TerrainMapModel import *
from modules.GeometryPrimitives import *

def genRandomObjPlace(zoneRect, objSize):
        x = randrange(zoneRect.pt.x, zoneRect.pt.x + zoneRect.sz.w - objSize.w)
        y = randrange(zoneRect.pt.y, zoneRect.pt.y + zoneRect.sz.h - objSize.h)
        return Point(x, y)

class MapEditor():
    def __init__(self, model):
        self._model = model

    def fillArea(self, startPt, size, property, value):
        for y in range(startPt.y, startPt.y + size.h):
            for x in range(startPt.x, startPt.x + size.w):
                square = self._model.getSquare(x, y)
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
        self.houseProbability = 0.9

        self.shedSize = AreaSize(2, 2)
        self.shedProbability = 0.5
        
        self.treeProbability = 0.2

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
        zone = ZoneGenerator(self._model, self._zoneSettings, startPt)
        zone.generate()

class ZoneLwObject():
    def __init__(self, zone, localPos=None, size=None, keepout=0):
        self.zone = zone
        self.objKeepout = keepout
        self.localPos = localPos
        self.size = size
        
    def localPosition(self):
        return self.localPos

    def localRect(self):
        return Rectangle(copy(self.localPos), copy(self.size))

    def localRectWithKeepout(self):
        return self.localRect().expand(self.objKeepout)

    def globalPosition(self):
        return self.localPos + self.zone.startPt

class ZoneObject(ZoneLwObject):
    def __init__(self, zone):
        ZoneLwObject.__init__(self, zone, keepout=1)

    def generate(self, size, squareType, mapObjType):
        self.size = size

        attempts = 500
        placeOk = False
        while (not placeOk) and attempts > 0:
            attempts -= 1
            self.localPos = genRandomObjPlace(self.zone.allowedRect, size)
            placeOk = self.zone.canPlaceObjectAt(self.localRect())

        if attempts == 0:
            print("!!!! Error: you are trying to put an object where is no place for it")
            return False

        print("    Obj placed at: " + str(self.localPos))
        self.zone.editor.fillArea(self.globalPosition(),
            size, 'type', squareType)
        
        obj = MapObjectModel(self.globalPosition().x, self.globalPosition().y, mapObjType)
        self.zone.model.addMapObject(obj)
        return True

class ZoneGenerator():
    def __init__(self, model, settings, startPt):
        self.model = model
        self.settings = settings
        self.editor = MapEditor(model)
        self.startPt = startPt
        self.zoneRect = Rectangle(Point(0,0), settings.size)
        self.zoneKeepout = 1
        self.allowedRect = self.zoneRect.shrink(self.zoneKeepout)
        print("    Shrinked rect=" + str(self.allowedRect))

        self.placedObjects = []

    def canPlaceObjectAt(self, objRect):
        for obj in self.placedObjects:
            objKeepout = obj.localRectWithKeepout()
            placeFail = objKeepout.isRectPartiallyInside(objRect)
            if placeFail:
                return False

        return True

    def generate(self):
        # Debug zone location
        #self.editor.fillAreaBorder(self.startPt, self.settings.size, SquareType.Empty)

        generateHouse = (random() < self.settings.houseProbability)
        if generateHouse:
            house = ZoneObject(self)
            house.generate(self.settings.houseSize,
                           SquareType.House,
                           MapObjectType.House)

            self.placedObjects.append(house)

        generateShed = (random() < self.settings.shedProbability)
        if generateShed:
            shed = ZoneObject(self)
            shed.generate(self.settings.shedSize,
                          SquareType.Shed,
                          MapObjectType.Shed)

            self.placedObjects.append(shed)
            
        
        self.generateTrees()
        
    def generateTrees(self):
        #rc = self.allowedRect
        rc = self.zoneRect
        for x in range(rc.pt.x, rc.pt.x + rc.sz.w):
            for y in range(rc.pt.y, rc.pt.y + rc.sz.h):
                treeRect = Rectangle(Point(x,y), AreaSize(1,1))
                if self.canPlaceObjectAt(treeRect):
                    generateTree = (random() < self.settings.treeProbability)
                    if generateTree:
                        # Should we place it to self.placedObjects?
                        obj = ZoneLwObject(self, Point(x,y), AreaSize(1, 1), keepout=0)
                        self.editor.fillArea(obj.globalPosition(),
                            obj.size, 'type', SquareType.Forest)

