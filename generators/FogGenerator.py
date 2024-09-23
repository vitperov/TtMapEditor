from modules.GeneratorPluginBase import *

from random import random

TypeGrass  = "Grass"

class FogGenerator(GeneratorPluginBase):
    def __init__(self, mapModel):
        super().__init__(mapModel)
        self.fogModel = 'Fog'


    def generate(self):
        print("Generating fog")
        interval = int(self.settings['intervalSquares'])

        for col in range(0, self.mapModel.width, interval):
            for row in range(0, self.mapModel.height, interval):
                self._placeFog(row,col)

        self.mapModel.updateEntireMap()

        print("Done")

    def clear_generated(self):
        print("Clear generated Fog")
        print("Done nothing TODO")

    def _placeFog(self, row, col):
        obj = MapObjectModelGeneral()
        obj.init(col, row, self.fogModel)
        self.mapModel.addMapObject(obj)
