from modules.GeneratorPluginBase import *

from random import randrange, random

from modules.GeometryPrimitives import *
from modules.Terrain.MapEditHelper import *
from modules.Terrain.TerrainGeneratorSettings import *

TypeLandLot  = "LandLot"
TypeForest   = "Forest"
TypeGrass    = "Grass"

class ForestGenerator(GeneratorPluginBase):
    def __init__(self, mapModel):
        super().__init__(mapModel)

    def generate(self):
        print("Generating landLot Forest")
        forestProbability = float(self.settings['forestProbability'])

        landLots = self.mapModel.getAllObjectOfType(TypeLandLot)
        print("    found " + str(len(landLots)) + " land lots")
        for lot in landLots:
            startPt = Point(lot.x, lot.y)
            size    = AreaSize(lot.w, lot.h)
            generator = ForestGeneratorHelper(self.mapModel, startPt, size)
            generator.findAllOccupiedSquares()
            generator.generate(forestProbability)

        self.mapModel.updateEntireMap()

        print("Done " + str(self.generatedModel))
        
    def clear_generated(self):
        print("Deleting forest...")
        landLots = self.mapModel.getAllObjectOfType(TypeLandLot)

        for lot in landLots:
            startPt = Point(lot.x, lot.y)
            size    = AreaSize(lot.w, lot.h)
            zLevel = 0
            selectionRange = SelectionRange.fromStartPointAndSize(startPt, size, zLevel)
            # Forest -> Grass
            self.mapModel.setGroupProperty(selectionRange, TypeForest, "model", TypeGrass)

class ForestGeneratorHelper():
    def __init__(self, model, startPt, size):
        #self.generatedModel = 'landLotContent'
        self.model = model
        self.editor = MapEditHelper(model)
        self.startPt = startPt
        self.size = size
        self.zLevel = 0

        self.occupiedSquares = []

    def findAllOccupiedSquares(self):
        selectionRange = SelectionRange.fromStartPointAndSize(self.startPt, self.size, 0)
        objects = self.model.getAllObjectOfType(None, selectionRange)
        
        for obj in objects:
            if obj.properties.get('model') != TypeGrass:
                for x in range(obj.x, obj.x + obj.w):
                    for y in range(obj.y, obj.y + obj.h):
                        self.occupiedSquares.append(Point(x, y))

    def generate(self, forestProbability):
        for x in range(self.startPt.x, self.startPt.x + self.size.w):
            for y in range(self.startPt.y, self.startPt.y + self.size.h):
                if Point(x, y) not in self.occupiedSquares:
                    generateTree = (random() < forestProbability)
                    if generateTree:
                        obj = self.model.createObjectAt(x, y, self.zLevel)
                        obj.setModel(TypeForest)
                        
