import math
from copy import copy
from random import randrange, random

from modules.TerrainMapModel import *
from modules.GeometryPrimitives import *
from modules.GeneratorSettings import *

def genRandomObjPlace(landLotRect, objSize):
        x = randrange(landLotRect.pt.x, landLotRect.pt.x + landLotRect.sz.w - objSize.w)
        y = randrange(landLotRect.pt.y, landLotRect.pt.y + landLotRect.sz.h - objSize.h)
        return Point(x, y)

# Helper functions to edit map regions
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

class MapGenerator():
    def __init__(self, model):
        self.settings = GeneratorSettings()

        self._model = model
        self._editor = MapEditor(model)

        self._calcMapSize()

        self._currentLandLotId = 0

        self._w = None
        self._h = None

    def loadSettings(self):
        try:
            self.settings.loadFromFile()
        except FileNotFoundError:
            print("Warning: generator setting file is not found. Using default settings")

        self._calcMapSize()

    def _calcMapSize(self):
        self._w = self.settings.landLotSettings.size.w * self.settings.columns + 2 * self.settings.forestKeepOut
        self._h = self.settings.landLotSettings.size.h * self.settings.rows + 2 * self.settings.forestKeepOut + self.settings.landLotSettings.roadWidth

    def generateMap(self):
        print("Generating map size=" + str(self._h) + "x" + str(self._w))
        self._model.newMap(self._w, self._h)

        self.fillEverythingGrass()
        self.genKeepOutForest()
        self.genRoad()
        self.genLandLots()

    def fillEverythingGrass(self):
        self._editor.fillArea(Point(0,0), AreaSize(self._w, self._h), 'type', SquareType.Grass)

    def genKeepOutForest(self):
        self._editor.fillAreaBorder(Point(0,0),  AreaSize(self._w, self._h),
            SquareType.Forest, width=self.settings.forestKeepOut)

    def genRoad(self):
        #FIXME: do road after every landLot height
        halfHeight = math.ceil(self._h / 2)
        self._editor.fillArea(Point(0, halfHeight - 1), AreaSize(self._w, 2), 'type', SquareType.Road)

    def genLandLots(self):
        for row in range(self.settings.rows):
            for column in range(self.settings.columns):
                print("Generating LandLot. Row=" + str(row) + " column=" + str(column))
                startPt = Point(column * self.settings.landLotSettings.size.w + self.settings.forestKeepOut,
                                row * self.settings.landLotSettings.size.h + self.settings.forestKeepOut)

                #if (row != 0) and (row != self._rows - 1):
                if row != 0:
                    startPt.y += self.settings.landLotSettings.roadWidth;
                    print("    -->Add road offset")

                print("    startPt=" + str(startPt))
                self.genLandLot(startPt)
                self._currentLandLotId += 1

    def genLandLot(self, startPt):
        landLot = LandLotGenerator(self._model, self.settings.landLotSettings, startPt)
        landLot.generate()

class LandLotLwObject():
    def __init__(self, landLot, localPos=None, size=None, keepout=0):
        self.landLot = landLot
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
        return self.localPos + self.landLot.startPt

class LandLotObject(LandLotLwObject):
    def __init__(self, landLot):
        LandLotLwObject.__init__(self, landLot, keepout=1)

    def generate(self, size, squareType, mapObjType):
        self.size = size

        attempts = 500
        placeOk = False
        while (not placeOk) and attempts > 0:
            attempts -= 1
            self.localPos = genRandomObjPlace(self.landLot.allowedRect, size)
            placeOk = self.landLot.canPlaceObjectAt(self.localRect())

        if attempts == 0:
            print("!!!! Error: you are trying to put an object where is no place for it")
            return False

        print("    Obj placed at: " + str(self.localPos))
        self.landLot.editor.fillArea(self.globalPosition(),
            size, 'type', squareType)

        obj = MapObjectModel(self.globalPosition().x, self.globalPosition().y, mapObjType)
        self.landLot.model.addMapObject(obj)
        return True

class LandLotGenerator():
    def __init__(self, model, settings, startPt):
        self.model = model
        self.settings = settings
        self.editor = MapEditor(model)
        self.startPt = startPt
        self.landLotRect = Rectangle(Point(0,0), settings.size)
        self.landLotKeepout = 1
        self.allowedRect = self.landLotRect.shrink(self.landLotKeepout)
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
        # Debug landLot location
        #self.editor.fillAreaBorder(self.startPt, self.settings.size, SquareType.Empty)

        generateHouse = (random() < self.settings.houseProbability)
        if generateHouse:
            house = LandLotObject(self)
            house.generate(self.settings.houseSize,
                           SquareType.House,
                           MapObjectType.House)

            self.placedObjects.append(house)

        generateShed = (random() < self.settings.shedProbability)
        if generateShed:
            shed = LandLotObject(self)
            shed.generate(self.settings.shedSize,
                          SquareType.Shed,
                          MapObjectType.Shed)

            self.placedObjects.append(shed)


        self.generateTrees()

    def generateTrees(self):
        #rc = self.allowedRect
        rc = self.landLotRect
        for x in range(rc.pt.x, rc.pt.x + rc.sz.w):
            for y in range(rc.pt.y, rc.pt.y + rc.sz.h):
                treeRect = Rectangle(Point(x,y), AreaSize(1,1))
                if self.canPlaceObjectAt(treeRect):
                    generateTree = (random() < self.settings.treeProbability)
                    if generateTree:
                        # Should we place it to self.placedObjects?
                        obj = LandLotLwObject(self, Point(x,y), AreaSize(1, 1), keepout=0)
                        self.editor.fillArea(obj.globalPosition(),
                            obj.size, 'type', SquareType.Forest)

