from modules.GeneratorPluginBase import *

from random import randrange, random

from modules.GeometryPrimitives import *
from modules.Terrain.MapEditHelper import *
from modules.Terrain.TerrainGeneratorSettings import *

TypeLandLot  = "LandLot"
TypeHouse    = "House"
TypeShed     = "Shed"
TypeForest   = "Forest"
TypeNone     = "None"

class LandLotContentGenerator(GeneratorPluginBase):
    def __init__(self, mapModel):
        super().__init__(mapModel)

    def generate(self):
        print("Generating landLotContent")
        houseProbability = float(self.settings['houseProbability'])
        #shedProbability = float(self.settings['shedProbability'])
        forestProbability = float(self.settings['forestProbability'])

        landLots = self.mapModel.getAllObjectOfType(TypeLandLot)
        print("    found " + str(len(landLots)) + " land lots")
        for lot in landLots:
            startPt = Point(lot.x, lot.y)
            size    = AreaSize(lot.w, lot.h)
            generator = LandLotGenerator(self.mapModel, startPt, size)
            generator.generate(houseProbability, forestProbability)

        self.mapModel.updateEntireMap()

        print("Done")
        
    def clear_generated(self):
        print("Clear generated LandLotContent")
        print("Done nothing TODO")


class LandLotGenerator():
    def __init__(self, model, startPt, size):
        self.model = model
        self.editor = MapEditHelper(model)
        self.startPt = startPt
        self.landLotRect = Rectangle(Point(0,0), size)
        self.landLotKeepout = 1
        self.allowedRect = self.landLotRect.shrink(self.landLotKeepout)
        print("Shrinked rect=" + str(self.allowedRect))

        self.placedObjects = []

        # Depricated should be removed
        self.oldSettings = TerrainGeneratorSettings()
        self.oldSettings.loadFromFile()

    def canPlaceObjectAt(self, objRect):
        for obj in self.placedObjects:
            objKeepout = obj.localRectWithKeepout()
            placeFail = objKeepout.isRectPartiallyInside(objRect)
            if placeFail:
                return False

        return True

    def generate(self, houseProbability, forestProbability):
        generateHouse = (random() < houseProbability)
        if generateHouse:
            house = LandLotObject(self)
            house.generateObjVariant(self.oldSettings.landLotSettings.house,
                           TypeHouse)

            self.placedObjects.append(house)

        #generateShed = (random() < shedProbability)
        #if generateShed:
        #    shed = LandLotObject(self)
        #    shed.generate(self.oldSettings.shed.size,
        #                  SquareType.Shed,
        #                  "shed")
        #
        #    self.placedObjects.append(shed)


        self.generateForest(forestProbability)

    def generateForest(self, forestProbability):
        rc = self.landLotRect
        for x in range(rc.pt.x, rc.pt.x + rc.sz.w):
            for y in range(rc.pt.y, rc.pt.y + rc.sz.h):
                treeRect = Rectangle(Point(x,y), AreaSize(1,1))
                if self.canPlaceObjectAt(treeRect):
                    generateTree = (random() < forestProbability)
                    if generateTree:
                        # Intentionally not appending into self.placedObjects
                        obj = LandLotLwObject(self, Point(x,y), AreaSize(1, 1), keepout=0)
                        self.editor.fillArea(obj.globalPosition(),
                            obj.size, 'model', TypeForest)


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

    def generate(self, size, objModelName, objModelVariant):
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
        obj.init(self.globalPosition().x, self.globalPosition().y, objModelName, ObjectRotation.deg0, size.w, size.h)
        obj.setProperty('variant',objModelVariant)
        self._randomizeProperty(obj, 'rotation')
        self.landLot.model.addMapObject(obj)

        rotation = int(obj.properties['rotation'].value);
        rotatedSize = size.rotated(rotation)
        print("Rotation " + str(rotation) + ": size=" + str(size) + " -> " + str(rotatedSize))

        #delete grass under the object
        self.landLot.editor.fillArea(self.globalPosition(),
            rotatedSize, 'model', TypeNone)

        return True

    def _chooseObjVariant(self, landObj):
        nVariants = landObj.nVariants()
        sumProbability = landObj.sumProbability()
        print(f"nVariants={nVariants}, sumProbability={sumProbability}")

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

    def generateObjVariant(self, landObj, objModelName):
        variantIdx = self._chooseObjVariant(landObj)
        variant = landObj.variants[variantIdx]
        self.generate(variant.size, objModelName, variant.modelName)

#TODO: move to some library
def genRandomObjPlace(landLotRect, objSize):
        x = randrange(landLotRect.pt.x, landLotRect.pt.x + landLotRect.sz.w - objSize.w)
        y = randrange(landLotRect.pt.y, landLotRect.pt.y + landLotRect.sz.h - objSize.h)
        return Point(x, y)
