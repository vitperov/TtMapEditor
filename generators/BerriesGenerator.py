from modules.GeneratorPluginBase import *

from random import random

TypeGrass  = "Grass"

class BerriesGenerator(GeneratorPluginBase):
    def __init__(self, mapModel):
        super().__init__(mapModel)
        self.berriesModel = 'Berries'


    def generate(self, settings):
        print("Generating berries")
        probability = 0.1
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


    def _placeBerries(self, row, col):
        obj = MapObjectModelGeneral()
        obj.init(col, row, self.berriesModel)
        self.mapModel.addMapObject(obj)
