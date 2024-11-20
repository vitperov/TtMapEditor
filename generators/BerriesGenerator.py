from modules.GeneratorPluginBase import *

from random import random

TypeGrass  = "Grass"
TypeBerries = 'Berries'

class BerriesGenerator(GeneratorPluginBase):
    def __init__(self, mapModel):
        super().__init__(mapModel)

    def generate(self):
        print("Generating berries")
        probability = float(self.settings['probability'])
        def isGrassSquare(row, col):
            if row < 0:
                return False
            if row >= self.mapModel.height:
                return False
            if col < 0:
                return False
            if col >= self.mapModel.width:
                return False

            square = self.mapModel.getSquare(col, row)
            sqType = square.getProperty('model')

            return sqType == TypeGrass

        for col in range(self.mapModel.width):
            for row in range(self.mapModel.height):
                if isGrassSquare(row, col):
                    generate = (random() < probability)
                    if generate:
                        self._placeBerries(row,col)

        self.mapModel.updateEntireMap()

        
    def clear_generated(self):
        zLevel = 0
        allSquares = self.mapModel.getAllSquares(zLevel)
        for square in allSquares:
            if square.getModel() == TypeBerries:
                self.mapModel.deleteSquareById(square.id)

        self.mapModel.updateEntireMap()

    def _placeBerries(self, row, col):
        obj = MapObjectModelGeneral()
        obj.init(col, row, model = TypeBerries)
        self.mapModel.addMapObject(obj)
