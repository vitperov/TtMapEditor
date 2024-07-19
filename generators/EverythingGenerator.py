from modules.GeneratorPluginBase import *

import math
from copy import copy
from random import randrange, random

from modules.MapModelGeneral import *
from modules.GeometryPrimitives import *
from modules.Terrain.TerrainGeneratorSettings import *

from modules.Terrain.MapEditHelper import *

TypeForest = "Forest"
TypeRoad   = "Road"
TypeGrass  = "Grass"
TypeHouse  = "House"

def genRandomObjPlace(landLotRect, objSize):
        x = randrange(landLotRect.pt.x, landLotRect.pt.x + landLotRect.sz.w - objSize.w)
        y = randrange(landLotRect.pt.y, landLotRect.pt.y + landLotRect.sz.h - objSize.h)
        return Point(x, y)

class EverythingGenerator(GeneratorPluginBase):
    def __init__(self, mapModel):
        super().__init__(mapModel)
        self.oldSettings = TerrainGeneratorSettings()

        self._model = mapModel
        self._editor = MapEditHelper(mapModel)

        self._calcMapSize()

        self._currentLandLotId = 0

        self._w = None
        self._h = None
        
        self.loadSettings()

    def loadSettings(self):
        try:
            self.oldSettings.loadFromFile()
        except FileNotFoundError:
            print("Warning: generator setting file is not found. Using default settings")

        self._calcMapSize()

    def _calcMapSize(self):
        self._w = self.oldSettings.landLotSettings.size.w * self.oldSettings.columns + 2 * self.oldSettings.forestKeepOut
        self._h = self.oldSettings.landLotSettings.size.h * self.oldSettings.rows + 2 * self.oldSettings.forestKeepOut + self.oldSettings.roadWidth

    def generate(self):
        print("Generating map size=" + str(self._h) + "x" + str(self._w))
        self._model.newMap(self._w, self._h)

        self.fillEverythingGrass()
        self.genKeepOutForest()
        self.genRoad()
        self.genLandLots()

    def fillEverythingGrass(self):
        self._editor.fillArea(Point(0,0), AreaSize(self._w, self._h), 'model', TypeGrass)

    def genKeepOutForest(self):
        self._editor.fillAreaBorder(Point(0,0),  AreaSize(self._w, self._h),
            TypeForest, width=self.oldSettings.forestKeepOut)

    def genRoad(self):
        #FIXME: do road after every landLot height
        halfHeight = math.ceil(self._h / 2)

        startEndMargin = 0
        if self.oldSettings.roadExitsArea == 0: # generate map without exits
            startEndMargin = self.oldSettings.forestKeepOut

        self._editor.fillArea(Point(startEndMargin, halfHeight - 1), AreaSize(self._w-startEndMargin*2, 2), 'model', TypeRoad)

    def genLandLots(self):
        for row in range(self.oldSettings.rows):
            for column in range(self.oldSettings.columns):
                print("Generating LandLot. Row=" + str(row) + " column=" + str(column))
                startPt = Point(column * self.oldSettings.landLotSettings.size.w + self.oldSettings.forestKeepOut,
                                row * self.oldSettings.landLotSettings.size.h + self.oldSettings.forestKeepOut)

                #if (row != 0) and (row != self._rows - 1):
                if row != 0:
                    startPt.y += self.oldSettings.roadWidth;

                print("    startPt=" + str(startPt))
                self.genLandLot(startPt)
                self._currentLandLotId += 1

    def genLandLot(self, startPt):
        landLot = LandLotGenerator(self._model, self.oldSettings.landLotSettings, startPt)
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

    def generate(self, size, squareType, objModelName):
        # can we pass landObj and get it's size?
        self.size = size

        attempts = 500
        placeOk = False
        while (not placeOk) and attempts > 0:
            attempts -= 1
            self.localPos = genRandomObjPlace(self.landLot.allowedRect, size)
            placeOk = self.landLot.canPlaceObjectAt(self.localRect())

        if attempts == 0:
            print("!!!! Error: you are trying to put an object where there is no place for it")
            return False

        print("    Obj placed at: " + str(self.localPos) + "; size=" + str(size))

        obj = MapObjectModelGeneral()
        obj.init(self.globalPosition().x, self.globalPosition().y, objModelName)
        self._randomizeProperty(obj, 'rotation')
        self.landLot.model.addMapObject(obj)

        rotation = int(obj.properties['rotation'].value);
        rotatedSize = size.rotated(rotation)
        print("Rotation " + str(rotation) + ": size=" + str(size) + " -> " + str(rotatedSize))

        self.landLot.editor.fillArea(self.globalPosition(),
            rotatedSize, 'model', squareType)

        return True

    def _chooseObjVariant(self, landObj):
        nVariants = landObj.nVariants()
        sumProbability = landObj.sumProbability()

        normalizationF = 1.0 / sumProbability

        rnd = random()
        accumulatedProbability = 0
        for variantIdx in range(nVariants):
            variant = landObj.variants[variantIdx]
            accumulatedProbability += variant.probability * normalizationF
            #print(str(rnd) + "-> [" + variant.modelName + "] = "+ str(variant.probability) + "/" + str(accumulatedProbability))
            if rnd < accumulatedProbability:
                return variantIdx

    def _randomizeProperty(self, obj, propertyName):
        prop = obj.properties[propertyName]
        propClass = type(prop)

        newValueIdx = randrange(len(propClass))
        allPossibleValues = list(propClass)
        newValueStr = allPossibleValues[newValueIdx].value
        print("Rotation = " + str(newValueIdx) + "/" + str(len(propClass)))
        newValue = propClass(newValueStr)
        obj.properties[propertyName] = newValue

    def generateObjVariant(self, landObj, squareType):
        variantIdx = self._chooseObjVariant(landObj)
        variant = landObj.variants[variantIdx]
        self.generate(variant.size, squareType, variant.modelName)


class LandLotGenerator():
    def __init__(self, model, settings, startPt):
        self.model = model
        self.oldSettings = settings
        self.editor = MapEditHelper(model)
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
        #self.editor.fillAreaBorder(self.startPt, self.oldSettings.size, SquareType.Empty)

        generateHouse = (random() < self.oldSettings.house.probability)
        if generateHouse:
            house = LandLotObject(self)
            house.generateObjVariant(self.oldSettings.house,
                           TypeHouse)

            self.placedObjects.append(house)

        generateShed = (random() < self.oldSettings.shed.probability)
        if generateShed:
            shed = LandLotObject(self)
            shed.generate(self.oldSettings.shed.size,
                          SquareType.Shed,
                          "shed")

            self.placedObjects.append(shed)


        self.generateTrees()

    def generateTrees(self):
        #rc = self.allowedRect
        rc = self.landLotRect
        for x in range(rc.pt.x, rc.pt.x + rc.sz.w):
            for y in range(rc.pt.y, rc.pt.y + rc.sz.h):
                treeRect = Rectangle(Point(x,y), AreaSize(1,1))
                if self.canPlaceObjectAt(treeRect):
                    generateTree = (random() < self.oldSettings.treeProbability)
                    if generateTree:
                        # Should we place it to self.placedObjects?
                        obj = LandLotLwObject(self, Point(x,y), AreaSize(1, 1), keepout=0)
                        self.editor.fillArea(obj.globalPosition(),
                            obj.size, 'model', TypeForest)
