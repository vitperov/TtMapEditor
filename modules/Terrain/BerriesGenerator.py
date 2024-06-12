from modules.Terrain.TerrainMapModel import *

from random import random

TypeGrass  = "Grass"

class BerriesGenerator():
    def __init__(self, model, objModelName):
        self.model = model
        self.berriesModel = objModelName


    def generate(self, probability):
        def isGrassSquare(row, col):
            if row < 0:
                return False
            if row >= self.model.height:
                return False
            if col < 0:
                return False
            if col >= self.model.width:
                return False

            square = self.model.getSquare(col, row)
            sqType = square.getProperty('type')
            
            return sqType == TypeGrass
            
            
        #FIXME: we can reduce available area excuding forest border
        for col in range(self.model.width):
            for row in range(self.model.height):
                if isGrassSquare(row, col):
                    generate = (random() < probability)
                    if generate:
                        self.placeBerries(row,col)
                    
                    
    def placeBerries(self, row, col):
        obj = MapObjectModelGeneral()
        obj.init(col, row, self.berriesModel)
        self.model.addMapObject(obj)

